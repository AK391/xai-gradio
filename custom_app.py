import gradio as gr
import xai_gradio

gr.load(
    name='grok-beta',
    src=xai_gradio.registry,
    title='X.AI-Gradio Integration',
    description="Chat with grok-beta model.",
    examples=["Explain quantum gravity to a 5-year old.", "How many R are there in the word Strawberry?"]
).launch()