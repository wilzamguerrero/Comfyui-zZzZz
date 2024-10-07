from .DownloadFileNode import DownloadFileNode
from .CompressFolderNode import CompressFolderNode
from .MoveZNode import MoveZNode
from .DeleteZNode import DeleteZNode  # Importa el nodo Delete
from .RenameZNode import RenameZNode  # Importa el nodo Rename

NODE_CLASS_MAPPINGS = {
    "DownloadFileNode": DownloadFileNode,
    "CompressFolderNode": CompressFolderNode,
    "MoveZNode": MoveZNode,
    "DeleteZNode": DeleteZNode,  # Agrega el nodo Delete
    "RenameZNode": RenameZNode,  # Agrega el nodo Rename
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DownloadFileNode": "Download Z",
    "CompressFolderNode": "Compress Z",
    "MoveZNode": "Move Z",
    "DeleteZNode": "Delete Z",  # Agrega el nombre del nodo Delete para la UI
    "RenameZNode": "Rename Z"   # Agrega el nombre del nodo Rename para la UI
}
