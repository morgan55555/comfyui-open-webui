# ComfyUI Open WebUI

Custom [ComfyUI](https://github.com/comfyanonymous/ComfyUI) Nodes for interacting with [Open WebUI](https://openwebui.com/).

Integrate the power of LLMs into ComfyUI workflows easily or just experiment with LLM inference.

To use this properly, you would need a running OpenWebUI server reachable from the host that is running ComfyUI.

## Installation

Install OpenWebUI server on the desired host

<a href="https://docs.openwebui.com/getting-started/quick-start">OpenWebUI quick start</a>

Use the [comfyui manager](https://github.com/ltdrdata/ComfyUI-Manager) "Custom Node Manager":

Search `open-webui` and select the one by `morgan55555`

**Or**

1. git clone into the ```custom_nodes``` folder inside your ComfyUI installation or download as zip and unzip the contents to ```custom_nodes/comfyui-open-webui```.
2. Start/restart ComfyUI

## Settings

1. Use "OPENWEBUI_URL" environment variable for set OpenWebUI url.
2. Use "OPENWEBUI_KEY" environment variable for set OpenWebUI key.

### Nodes

### OpenwebuiVision

A node that gives an ability to query input images. 

A model name should be model with Vision abilities, for example: https://ollama.com/library/llava.

### OpenwebuiGenerate

A node that gives an ability to query an LLM via given prompt. 

## Usage Example

Consider the following workflow of vision an image, and perform additional text processing with desired LLM. In the OpenwebuiGenerate node set the prompt as input.
