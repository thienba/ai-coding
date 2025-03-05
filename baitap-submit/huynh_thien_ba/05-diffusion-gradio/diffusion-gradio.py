import gradio as gr
from diffusers import DiffusionPipeline
import torch
import psutil
import gc

model_cache = {}

def get_available_memory():
    if torch.cuda.is_available():
        return torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated()
    else:
        return psutil.virtual_memory().available

def load_model(model_name):
    required_memory = 7 * 1024 * 1024 * 1024  
    
    if model_name not in model_cache:
        available_memory = get_available_memory()
        
        if available_memory < required_memory:
            for cached_model in list(model_cache.keys()):
                if cached_model != model_name:
                    if torch.cuda.is_available():
                        model_cache[cached_model].to('cpu')
                    del model_cache[cached_model]
                    gc.collect()
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
        
        pipeline = DiffusionPipeline.from_pretrained(model_name, use_safetensors=True, safety_checker=None, requires_safety_checker=False)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        device = "mps" if torch.backends.mps.is_available() else device
        pipeline.to(device)
        model_cache[model_name] = pipeline
    return model_cache[model_name]

current_model = "sd-legacy/stable-diffusion-v1-5"
model_cache[current_model] = load_model(current_model)

def generate_image(prompt, negative_prompt, model_name, seed, num_inference_steps, guidance_scale):
    pipeline = load_model(model_name)
    image = pipeline(prompt, negative_prompt=negative_prompt, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale, seed=seed).images[0]
    return image

with gr.Blocks() as demo:
    gr.Markdown("## Diffusion Gradio")
    with gr.Row():
        with gr.Column():
            prompt = gr.Textbox(label="Prompt")
            negative_prompt = gr.Textbox(label="Negative Prompt")
            model_name = gr.Dropdown(
                choices=["sd-legacy/stable-diffusion-v1-5", "stablediffusionapi/anything-v5"],
                value="sd-legacy/stable-diffusion-v1-5",
                label="Model"
            )
            seed = gr.Slider(label="Seed", minimum=-1, maximum=1000000, step=1, value=-1)
            num_inference_steps = gr.Slider(label="Number of Inference Steps", minimum=1, maximum=100, step=1, value=25)
            guidance_scale = gr.Slider(label="Guidance Scale", minimum=0, maximum=20, step=0.5, value=7.5)
            btn_generate = gr.Button("Generate")
        with gr.Column():
            image = gr.Image(label="Generated Image")
            
    btn_generate.click(generate_image, inputs=[prompt, negative_prompt, model_name, seed, num_inference_steps, guidance_scale], outputs=image)

demo.launch()