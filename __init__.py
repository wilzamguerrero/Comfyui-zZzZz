from .DownloadFileNode import DownloadFileNode
from .CompressFolderNode import CompressFolderNode  # Importa el nuevo nodo

NODE_CLASS_MAPPINGS = {
    "DownloadFileNode": DownloadFileNode,
    "CompressFolderNode": CompressFolderNode  # Agrega el nuevo nodo
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DownloadFileNode": "Download Z",
    "CompressFolderNode": "Compress Z"  # Agrega el nombre del nuevo nodo para la UI
}
