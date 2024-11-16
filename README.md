# `xai-gradio`

is a Python package that makes it very easy for developers to create machine learning apps that are powered by XAI API.

# Installation

You can install `xai-gradio` directly using pip:

```bash
pip install xai-gradio
```

That's it! 

# Basic Usage

You'll need to save your xAI API key to the appropriate environment variable:

```bash
export XAI_API_KEY=<your token>
```

Then in a Python file, write:

```python
import gradio as gr
import xai_gradio

gr.load(
    name='grok-beta',
    src=xai_gradio.registry,
).launch()
```

Run the Python file, and you should see a Gradio Interface connected to your chosen model!

![ChatInterface](chatinterface.png)

# Customization 

Once you can create a Gradio UI from an OpenAI endpoint, you can customize it by setting your own input and output components, or any other arguments to `gr.Interface`. For example, the screenshot below was generated with:

```py
import gradio as gr
import xai_gradio

gr.load(
    name='grok-beta',
    src=xai_gradio.registry,
    title='X.AI-Gradio Integration',
    description="Chat with grok-beta model.",
    examples=["Explain quantum gravity to a 5-year old.", "How many R are there in the word Strawberry?"]
).launch()
```
![ChatInterface with customizations](xai-gradio-custom.png)

# Composition

Or use your loaded Interface within larger Gradio Web UIs, e.g.

```python
import gradio as gr
import xai_gradio

with gr.Blocks() as demo:
    with gr.Tab("grok-beta"):
        gr.load('grok-beta', src=xai_gradio.registry)

demo.launch()
```

# Under the Hood

The xai-gradio Python library has two dependencies: openai and gradio. It defines a "registry" function xai_gradio.registry, 
which takes in a model name and returns a Gradio app.

# Supported Models and Providers

The following AI models are currently supported:

- xAI (Grok-beta)

For a comprehensive list of available models and their specifications, please refer to:
- [xAI Models](https://console.xai.com/models)

-------

Note: if you are getting authentication errors, ensure you have set the correct environment variable. You can also set it in your Python session:

```python
import os
os.environ["XAI_API_KEY"] = ...
```