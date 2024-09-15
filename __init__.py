from .DownloadFileNode import DownloadFileNode
from .CompressFolderNode import CompressFolderNode
from .MoveZNode import MoveZNode  # Importa el nodo Move Z  # Importa el nuevo nodo

NODE_CLASS_MAPPINGS = {
    "DownloadFileNode": DownloadFileNode,
    "CompressFolderNode": CompressFolderNode,  # Agrega el nuevo nodo
    "MoveZNode": MoveZNode,  # Agrega el nodo Move Z
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DownloadFileNode": "Download Z",
    "CompressFolderNode": "Compress Z",
    "MoveZNode": "Move Z"  # Agrega el nombre del nuevo nodo para la UI
}
