import gradio as gr
import xai_gradio

gr.load(
    name='grok-vision-beta',
    src=xai_gradio.registry,
).launch()