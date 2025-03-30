import pandas as pd
import weaviate
from weaviate.embedded import EmbeddedOptions
from weaviate.classes.config import Configure, Property, DataType, Tokenization


embedded_options = EmbeddedOptions(
    additional_env_vars={
        "ENABLE_MODULES": "backup-filesystem,text2vec-transformers",
        "BACKUP_FILESYSTEM_PATH": "/tmp/backups",
        "LOG_LEVEL": "panic",
        "TRANSFORMERS_INFERENCE_API": "http://localhost:8000"
    },
    persistence_data_path="data",
)

vector_db_client = weaviate.WeaviateClient(
    embedded_options=embedded_options
)
vector_db_client.connect()

COLLECTION_NAME = 'BookCollection'

def create_collection():
    movie_collection = vector_db_client.collections.create(
        name=COLLECTION_NAME,
        vectorizer_config=Configure.Vectorizer.text2vec_transformers(),
        properties=[
            Property(name="title", data_type=DataType.TEXT,
                     vectorize_property_name=True, tokenization=Tokenization.LOWERCASE),
            Property(name="author", data_type=DataType.TEXT,
                    vectorize_property_name=True, tokenization=Tokenization.LOWERCASE),
            Property(name="description", data_type=DataType.TEXT,
                    tokenization=Tokenization.WORD),
            Property(name="grade", data_type=DataType.TEXT,
                    skip_vectorization=True),
            Property(name="genre", data_type=DataType.TEXT_ARRAY,
                    tokenization=Tokenization.WORD),
            Property(name="lexile", data_type=DataType.TEXT,
                    skip_vectorization=True),
            Property(name="path", data_type=DataType.TEXT,
                    skip_vectorization=True),
            Property(name="is_prose", data_type=DataType.BOOL,
                    skip_vectorization=True),
            Property(name="date", data_type=DataType.TEXT,
                    skip_vectorization=True),
            Property(name="intro", data_type=DataType.TEXT,
                    tokenization=Tokenization.WORD),
            Property(name="excerpt", data_type=DataType.TEXT,
                    tokenization=Tokenization.WORD),
            Property(name="license", data_type=DataType.TEXT,
                    skip_vectorization=True),
            Property(name="notes", data_type=DataType.TEXT,
                    tokenization=Tokenization.WORD),
            Property(name="extract", data_type=DataType.TEXT, tokenization=Tokenization.WHITESPACE),
            Property(name="cast", data_type=DataType.TEXT_ARRAY, tokenization=Tokenization.WORD),
            Property(name="genres", data_type=DataType.TEXT_ARRAY, tokenization=Tokenization.WORD),
            Property(name="thumbnail", data_type=DataType.TEXT, skip_vectorization=True),
            Property(name="href", data_type=DataType.TEXT, skip_vectorization=True),
        ]
    )

    data = pd.read_csv('commonlit_texts.csv')
    
    # Convert data types before creating records
    data['grade'] = data['grade'].astype(str)
    data['lexile'] = data['lexile'].astype(str)
    data['is_prose'] = data['is_prose'].astype(bool)
    # Convert genre string to array (assuming genres are comma-separated)
    data['genre'] = data['genre'].str.split(',')
    
    sent_to_vector_db = data.to_dict(orient='records')
    total_records = len(sent_to_vector_db)
    print(f"Inserting data to Vector DB. Total records: {total_records}")

    with movie_collection.batch.dynamic() as batch:
        for data_row in sent_to_vector_db:
            print(f"Inserting: {data_row['title']}")
            batch.add_object(properties=data_row)

    print("Data saved to Vector DB")


if vector_db_client.collections.exists(COLLECTION_NAME):
    print("Collection {} already exists".format(COLLECTION_NAME))
else:
    create_collection()

vector_db_client.close()