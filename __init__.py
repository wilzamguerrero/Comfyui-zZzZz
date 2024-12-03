import os
from .utils_video import installNodes, NODE_CLASS_MAPPINGS as VIDEO_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as VIDEO_NODE_DISPLAY_NAME_MAPPINGS
from .utils import VERSION, ADDON_NAME, HOME_PATH, COMFY_WEB_EXTENSIONS_PATH, printColor, checkDir, addFilesToDir, load_config

from .DownloadFileNode import DownloadFileNode
from .CompressFolderNode import CompressFolderNode
from .MoveZNode import MoveZNode
from .DeleteZNode import DeleteZNode
from .RenameZNode import RenameZNode
from .CreateZNode import CreateZNode
from .InfiniteZNode import InfiniteZNode
from .share_screen import ZFShareScreen


NODE_CLASS_MAPPINGS = {
    "DownloadFileNode": DownloadFileNode,
    "CompressFolderNode": CompressFolderNode,
    "MoveZNode": MoveZNode,
    "DeleteZNode": DeleteZNode,
    "RenameZNode": RenameZNode,
    "CreateZNode": CreateZNode,
    "InfiniteZNode": InfiniteZNode,
    "ZFShareScreen": ZFShareScreen,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DownloadFileNode": "Download Z",
    "CompressFolderNode": "Compress Z",
    "MoveZNode": "Move Z",
    "DeleteZNode": "Delete Z",
    "RenameZNode": "Rename Z",
    "CreateZNode": "Create Z",
    "InfiniteZNode": "Infinite Z",
    "ZFShareScreen": "Share Screen Z",
}


__version__ = VERSION

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

def install_nodes():
    js_folder = os.path.join(HOME_PATH, "js")
    install_folder = os.path.join(COMFY_WEB_EXTENSIONS_PATH, ADDON_NAME)

    checkDir(install_folder)
    addFilesToDir(js_folder, install_folder)
    
load_config()
install_nodes()

