import os
import base64
from openai import OpenAI
import gradio as gr
from typing import Callable

__version__ = "0.0.1"

def get_image_base64(url: str, ext: str):
    with open(url, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return "data:image/" + ext + ";base64," + encoded_string

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

def handle_user_msg(message: str):
    if type(message) is str:
        return message
    elif type(message) is dict:
        if message["files"] is not None and len(message["files"]) > 0:
            ext = os.path.splitext(message["files"][-1])[1].strip(".")
            if ext.lower() in ["png", "jpg", "jpeg", "gif"]:
                encoded_str = get_image_base64(message["files"][-1], ext)
            else:
                raise NotImplementedError(f"Not supported file type {ext}")
            content = [
                {"type": "text", "text": message["text"]},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": encoded_str,
                    }
                },
            ]
        else:
            content = message["text"]
        return content
    else:
        raise NotImplementedError

def get_interface_args(model_name: str):
    inputs = None
    outputs = None
    
    def preprocess(message, history):
        messages = [{"role": "system", "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."}]
        files = None
        for user_msg, assistant_msg in history:
            if assistant_msg is not None:
                messages.append({"role": "user", "content": handle_user_msg(user_msg)})
                messages.append({"role": "assistant", "content": assistant_msg})
            else:
                files = user_msg
        
        if type(message) is str and files is not None:
            message = {"text": message, "files": files}
        elif type(message) is dict and files is not None:
            if message["files"] is None or len(message["files"]) == 0:
                message["files"] = files
        
        messages.append({"role": "user", "content": handle_user_msg(message)})
        return {"messages": messages}

    postprocess = lambda x: x  # No post-processing needed
    return inputs, outputs, preprocess, postprocess

def registry(name: str = "grok-beta", token: str | None = None, **kwargs):
    """
    Create a Gradio Interface for X.AI's Grok model.

    Parameters:
        - name (str): The name of the model (defaults to "grok-beta" or "grok-vision-beta")
        - token (str, optional): The X.AI API key
    """
    api_key = token or os.environ.get("XAI_API_KEY")
    if not api_key:
        raise ValueError("XAI_API_KEY environment variable is not set.")

    inputs, outputs, preprocess, postprocess = get_interface_args(name)
    fn = get_fn(name, preprocess, postprocess, api_key)
    
    # Always set multimodal=True
    kwargs["multimodal"] = True
    
    interface = gr.ChatInterface(fn=fn, **kwargs)

    return interface
