import random

from requests import post, get
import numpy as np
import base64
from io import BytesIO
from server import PromptServer
from aiohttp import web
from PIL import Image
import os

@PromptServer.instance.routes.get("/openwebui/get_models")
async def get_models_endpoint(request):
    api_url = os.environ['OPENWEBUI_URL']
    api_key = os.environ['OPENWEBUI_KEY']

    url = f'{api_url}/api/models'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    try:
        response = get(url, headers=headers)

        if response.ok:
            data = response.json()
            models = data.get("data", [])
            models = [model['id'] for model in models]
            return web.json_response(models)

    except Exception as e:
        return web.json_response([])



class OpenwebuiVision:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        seed = random.randint(1, 2 ** 31)
        return {
            "required": {
                "images": ("IMAGE",),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "describe the image"
                }),
                "model": ((), {}),
                "format": (["text", "json",''],),
                "seed": ("INT", {"default": seed, "min": 0, "max": 2 ** 31, "step": 1}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("description",)
    FUNCTION = "openwebui_vision"
    CATEGORY = "OpenWebUI"

    def openwebui_vision(self, images, prompt, model, seed, format):
        images_b64 = []

        if format == "text":
            format = ''

        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_bytes = base64.b64encode(buffered.getvalue())
            images_b64.append(str(img_bytes, 'utf-8'))

        api_url = os.environ['OPENWEBUI_URL']
        api_key = os.environ['OPENWEBUI_KEY']

        url = f'{api_url}/api/chat/completions'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'images': images_b64,
            'options': {},
            'format': format,
            'seed': seed,
        }

        response = post(url, headers=headers, json=payload)
        if response.ok:
            data = response.json()
            choices = data.get('choices', [])
            choice = choices[0] if len(choices) > 0 else None
            message = choice.get('message') if choice is not None else None

            if message:
                return (message.get('content',""),)

        return ("",)



class OpenwebuiGenerate:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        seed = random.randint(1, 2 ** 31)
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "What is Art?"
                }),
                "model": ((), {}),
                "format": (["text", "json",''],),
                "seed": ("INT", {"default": seed, "min": 0, "max": 2 ** 31, "step": 1}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "openwebui_generate"
    CATEGORY = "OpenWebUI"

    def openwebui_generate(self, prompt, model, seed, format):

        api_url = os.environ['OPENWEBUI_URL']
        api_key = os.environ['OPENWEBUI_KEY']

        url = f'{api_url}/api/chat/completions'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'options': {'seed': seed},
            'format': format,
            'seed': seed,
        }

        response = post(url, headers=headers, json=payload)
        if response.ok:
            data = response.json()
            choices = data.get('choices', [])
            choice = choices[0] if len(choices) > 0 else None
            message = choice.get('message') if choice is not None else None

            if message:
                return (message.get('content',""),)

        return ("",)



NODE_CLASS_MAPPINGS = {
    "OpenwebuiVision": OpenwebuiVision,
    "OpenwebuiGenerate": OpenwebuiGenerate,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OpenwebuiVision": "OpenWebUI Vision",
    "OpenwebuiGenerate": "OpenWebUI Generate",
}
