import gradio as gr
import weaviate
from weaviate.embedded import EmbeddedOptions

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

# Cấu hình tên collection
COLLECTION_NAME = "BookCollection"

def search_book(query):
    book_collection = vector_db_client.collections.get(COLLECTION_NAME)
    response = book_collection.query.near_text(query=query, limit=10, distance=True)
    results = []
    html_results = []
    for book in response.objects:
        # Create HTML formatted string for each book
        html_result = f"""
        <div style='margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px;'>
            <h3 style='color: #2c3e50; margin-bottom: 10px;'>{book.properties['title']}</h3>
            <p style='color: #34495e;'>{book.properties['description']}</p>
        </div>
        """
        html_results.append(html_result)
    return "\n".join(html_results)

with gr.Blocks(title="Weaviate Search") as interface:
    gr.Markdown("Enter a search query:")
    query = gr.Textbox(label="Search Query")
    search = gr.Button("Search")
    # Replace Gallery with HTML output
    results_html = gr.HTML(label="Search Results")
    search.click(fn=search_book, inputs=query, outputs=results_html)

interface.queue().launch()

vector_db_client.close()