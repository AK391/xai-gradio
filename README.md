# `xai-gradio`

is a Python package that makes it very easy for developers to create machine learning apps that are powered by various AI model providers' APIs.

# Installation

You can install `xai-gradio` directly using pip:

```bash
pip install xai-gradio
```

That's it! 

# Basic Usage

Just like if you were to use the provider's API directly, you should first save your API key to the appropriate environment variable:

```bash
# For OpenAI
export OPENAI_API_KEY=<your token>
# For Anthropic
export ANTHROPIC_API_KEY=<your token>
# For other providers...
```

Then in a Python file, write:

```python
import gradio as gr
import xai_gradio

gr.load(
    name='gpt-4-turbo',  # or 'claude-3-opus', etc.
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
    name='gpt-4-turbo',
    src=xai_gradio.registry,
    title='OpenAI-Gradio Integration',
    description="Chat with GPT-4-turbo model.",
    examples=["Explain quantum gravity to a 5-year old.", "How many R are there in the word Strawberry?"]
).launch()
```
![ChatInterface with customizations](chatinterface_with_customization.png)

# Composition

Or use your loaded Interface within larger Gradio Web UIs, e.g.

```python
import gradio as gr
import xai_gradio

with gr.Blocks() as demo:
    with gr.Tab("GPT-4-turbo"):
        gr.load('gpt-4-turbo', src=xai_gradio.registry)
    with gr.Tab("GPT-3.5-turbo"):
        gr.load('gpt-3.5-turbo', src=xai_gradio.registry)

demo.launch()
```

# Under the Hood

The `xai-gradio` Python library supports multiple AI providers through their respective Python SDKs. It defines a "registry" function `xai_gradio.registry`, which takes in a model name and returns a Gradio app.

# Supported Models and Providers

The following AI providers and their models are currently supported:

- OpenAI (GPT-4, GPT-3.5, etc.)
- Anthropic (Claude 3, etc.)
- [List other supported providers]

For a comprehensive list of available models and their specifications, please refer to each provider's documentation:
- [OpenAI Models](https://platform.openai.com/docs/models)
- [Anthropic Models](https://docs.anthropic.com/claude/docs/models-overview)
- [Other provider docs...]

-------

Note: if you are getting authentication errors, ensure you have set the correct environment variable for your chosen provider. You can also set them in your Python session:

```python
import os

# For OpenAI
os.environ["OPENAI_API_KEY"] = ...
# For Anthropic
os.environ["ANTHROPIC_API_KEY"] = ...
```