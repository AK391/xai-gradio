import gradio as gr
import xai_gradio

with gr.Blocks() as demo:
    with gr.Tab("grok-beta"):
        gr.load('grok-beta', src=xai_gradio.registry)

demo.launch()