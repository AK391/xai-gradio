import gradio as gr
import xai_gradio

gr.load(
    name='grok-beta',
    src=xai_gradio.registry,
).launch()