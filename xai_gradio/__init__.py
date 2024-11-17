import os
from openai import OpenAI
import gradio as gr
from typing import Callable

__version__ = "0.0.1"


def get_fn(model_name: str, preprocess: Callable, postprocess: Callable, api_key: str):
    def fn(message, history):
        inputs = preprocess(message, history)
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1",
        )
        completion = client.chat.completions.create(
            model=model_name,
            messages=inputs["messages"],
            stream=True,
        )
        response_text = ""
        for chunk in completion:
            delta = chunk.choices[0].delta.content or ""
            response_text += delta
            yield postprocess(response_text)

    return fn


def get_interface_args():
    inputs = None
    outputs = None

    def preprocess(message, history):
        messages = [{"role": "system", "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."}]
        for user_msg, assistant_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})
        messages.append({"role": "user", "content": message})
        return {"messages": messages}

    postprocess = lambda x: x  # No post-processing needed
    return inputs, outputs, preprocess, postprocess


def registry(name: str = "grok-beta", token: str | None = None, **kwargs):
    """
    Create a Gradio Interface for X.AI's Grok model.

    Parameters:
        - name (str): The name of the model (defaults to "grok-beta")
        - token (str, optional): The X.AI API key
    """
    api_key = token or os.environ.get("XAI_API_KEY")
    if not api_key:
        raise ValueError("XAI_API_KEY environment variable is not set.")

    inputs, outputs, preprocess, postprocess = get_interface_args()
    fn = get_fn(name, preprocess, postprocess, api_key)
    interface = gr.ChatInterface(fn=fn, **kwargs)

    return interface
