import base64
import requests
import gradio as gr

URL = "http://127.0.0.1:7860"


def base64_to_image(base64_string, save_path='output_image.png'):
    with open(save_path, 'wb') as f:
        f.write(base64.b64decode(base64_string))


def text_to_image(prompt, width, height):
    payload = {
        "prompt": prompt,
        "negative_prompt": "worst quality, low quality, watermark, text, error, blurry, jpeg artifacts, cropped, jpeg artifacts, signature, watermark, username, artist name, bad anatomy",
        "steps": 25,
        "cfg_scale": 7.5,
        "width": width,
        "height": height,
    }

    response = requests.post(f"{URL}/sdapi/v1/txt2img", json=payload)
    resp_json = response.json()
    for i, img in enumerate(resp_json['images']):
        base64_to_image(img, f"output_image_{i}.png")
        return f"output_image_{i}.png"

with gr.Blocks() as demo:
    gr.Markdown("SD WebUI API")
    with gr.Row():
        with gr.Column():
            with gr.Row():
                prompt = gr.Textbox(label="Prompt")
            with gr.Row():
                width = gr.Slider(label="Width", minimum=64, maximum=1024, step=64, value=512)
            with gr.Row():
                height = gr.Slider(label="Height", minimum=64, maximum=1024, step=64, value=512)  
            with gr.Row():
                btn = gr.Button("Generate")
        with gr.Column():
            output_image = gr.Image(label="Output Image")

    btn.click(text_to_image, inputs=[prompt, width, height], outputs=output_image)

demo.launch()