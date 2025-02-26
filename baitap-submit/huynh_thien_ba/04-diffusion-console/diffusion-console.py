from diffusers import DiffusionPipeline, EulerDiscreteScheduler, DDIMScheduler, DPMSolverMultistepScheduler
import torch

pipeline = DiffusionPipeline.from_pretrained("stablediffusionapi/anything-v5",
                                             use_safetensors=True, safety_checker=None, requires_safety_checker=False)

device = "cuda" if torch.cuda.is_available() else "cpu"
pipeline.to(device)

def get_non_empty_input(prompt_text):
    value = input(prompt_text)
    while not value.strip():
        print("This field is required.")
        value = input(prompt_text)
    return value

def get_valid_dimension(prompt_text):
    while True:
        try:
            value = int(get_non_empty_input(prompt_text))
            if value % 8 != 0:
                raise ValueError(f"{prompt_text} must be divisible by 8.")
            return value
        except ValueError as e:
            print(e)

prompt = get_non_empty_input("Enter prompt: ")
width = get_valid_dimension("Enter width: ")
height = get_valid_dimension("Enter height: ")

image = pipeline(
    prompt,
    height=height,
    width=width,
    guidance_scale=6.5,
    num_inference_steps=24,
    negative_prompt="ugly, deformed, disfigured, low quality, worst quality",
    generator=torch.Generator(device=device).manual_seed(6969),
).images[0]

image.save("output.png")