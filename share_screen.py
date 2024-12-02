from PIL import Image
from .utils import base642pil, pil2tensor

class ZFShareScreen:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_base64": ("BASE64",),
            },
            "optional": {
                "RGBA": ([False, True], {"default": False}),
            },
        }

    CATEGORY = "zZzZz"
    OUTPUT_NODE = True

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "doit"

    def doit(self, image_base64, RGBA=False):
        if isinstance(image_base64, str):
            image = base642pil(image_base64)
        else:
            image = None

        if image is None:
            # Crear una imagen vacía como predeterminada
            if RGBA:
                image = Image.new(mode='RGBA', size=(512, 512), color=(0, 0, 0, 0))
            else:
                image = Image.new(mode='RGB', size=(512, 512), color=(0, 0, 0))

        image = pil2tensor(image.convert('RGBA' if RGBA else 'RGB'))
        return (image,)
