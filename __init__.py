from .DownloadFileNode import DownloadFileNode
from .CompressFolderNode import CompressFolderNode
from .MoveZNode import MoveZNode
from .DeleteZNode import DeleteZNode  
from .RenameZNode import RenameZNode  
from .CreateZNode import CreateZNode  
from .InfiniteZNode import InfiniteZNode


NODE_CLASS_MAPPINGS = {
    "DownloadFileNode": DownloadFileNode,
    "CompressFolderNode": CompressFolderNode,
    "MoveZNode": MoveZNode,
    "DeleteZNode": DeleteZNode,
    "RenameZNode": RenameZNode,
    "CreateZNode": CreateZNode,
    "InfiniteZNode": InfiniteZNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DownloadFileNode": "Download Z",
    "CompressFolderNode": "Compress Z",
    "MoveZNode": "Move Z",
    "DeleteZNode": "Delete Z",
    "RenameZNode": "Rename Z",
    "CreateZNode": "Create Z",
    "InfiniteZNode": "Infinite Z",
}
