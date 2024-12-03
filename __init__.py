
import os
import importlib.util
import subprocess
import sys
import filecmp
import shutil
import __main__
import re

python = sys.executable

# User extension files in custom_nodes
extension_folder = os.path.dirname(os.path.realpath(__file__))

# ComfyUI folders web
folder_web = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)), "web")
folder_web_extensions = os.path.join(folder_web, "extensions")
folder_web_lib = os.path.join(folder_web, 'lib')
js_source_folder = os.path.join(extension_folder, "js")  # Carpeta de origen para archivos JS
extension_dirs = ["FISH_EasyCapture",]
#
DEBUG = False
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
humanReadableTextReg = re.compile('(?<=[a-z])([A-Z])|(?<=[A-Z])([A-Z][a-z]+)')
module_name_cut_version = re.compile("[>=<]")

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


def log(*text):
    if DEBUG:
        print(''.join(map(str, text)))


def check_is_installed(module_name):
    try:
        module_name_cut_index = module_name_cut_version.search(module_name).start()
        mod = importlib.util.find_spec(module_name[:module_name_cut_index])
    except ModuleNotFoundError:
        return False
    except AttributeError:
        # En caso de que no se encuentre ningún operador de versión
        mod = importlib.util.find_spec(module_name)
    
    return mod is not None


def module_install(module_name, action='install'):
    if not module_name and not action:
        log(f'    [!] Action, module_name arguments is not corrects!')
        return
    
    command = f'"{python}" -m pip {action} {module_name}'
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=os.environ )
    action_capitalize = action.capitalize()

    if result.returncode != 0:
        log(f'    [E] {action_capitalize} module {module_name} is fail! Error code: {result.returncode}')
        return  # Agregar un return para evitar el log de éxito en caso de error

    log(f'    [*] {action_capitalize} module "{module_name}" successful')


def checkModules(nodeElement):
    file_requir = os.path.join(extension_folder, f"{nodeElement}.txt")  # Asumiendo requirements específicas por nodo
    if os.path.exists(file_requir):
        log("  -> File 'requirements.txt' found!")
        with open(file_requir, 'r', encoding="utf-8") as r:
            for m in r.readlines():
                m = m.strip()
                
                if m.startswith("#") or not m:
                    log(f"    [!] Found comment or empty line, skipping: '{m}'")
                    continue
                
                log(f"    [*] Check installed module '{m}'...")
                check_m = check_is_installed(m)
                if not check_m:
                    module_install(m)
                else:
                    log(f"    [*] Module '{m}' is installed!")                  


def addFilesToFolder(folderSrc, folderDst, files_to_add):
    if os.path.exists(folderSrc):
        log(f"  -> Find files in '{os.path.basename(folderSrc)}' folder...")
        find_files = filecmp.dircmp(folderSrc, folderDst)
        if find_files.left_only or find_files.diff_files:
            listFiles = list(find_files.left_only)
            listFiles.extend(f for f in find_files.diff_files if f not in listFiles)

            log(f"    [*] Found files to add/update: {', '.join(listFiles)}")
            for f in listFiles:
                src_f = os.path.join(folderSrc, f)
                dst_f = os.path.join(folderDst, f)
                if os.path.exists(dst_f):
                    os.remove(dst_f)
                shutil.copy(src_f, dst_f)


def removeFilesOldFolder(folderSrc, folderDst):
    if os.path.exists(folderDst):
        log(f"  -> Find old files in '{os.path.basename(folderDst)}' folder and remove them if not present in source.")
        find_files = filecmp.dircmp(folderSrc, folderDst)
        if find_files.common_files:
            listFiles = list(find_files.common_files)
            log(f"    [*] Found old files to remove: {', '.join(listFiles)}")
            for f in listFiles:              
                dst_f = os.path.join(folderDst, f)
                if os.path.exists(dst_f):
                    log(f"    [*] File '{f}' is removed.")
                    os.remove(dst_f)


def addComfyUINodesToMapping(nodeElement):
    log(f"  -> Find class execute node <{nodeElement}>, add NODE_CLASS_MAPPINGS ...")
    node_file = os.path.join(extension_folder, f"{nodeElement}.py")
    if not os.path.isfile(node_file):
        log(f"    [!] Node file '{node_file}' does not exist.")
        return
    
    # Import module
    spec = importlib.util.spec_from_file_location(nodeElement, node_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    classes_names = list(filter(lambda p: callable(getattr(module, p)) and p.find('Node') != -1, dir(module)))
    for class_module_name in classes_names:
        # Check module 
        if class_module_name and class_module_name not in NODE_CLASS_MAPPINGS.keys():
            log(f"    [*] Class node found '{class_module_name}' add to NODE_CLASS_MAPPINGS...")
            NODE_CLASS_MAPPINGS.update({
                class_module_name: getattr(module, class_module_name)
            })
            NODE_DISPLAY_NAME_MAPPINGS.update({
                class_module_name: humanReadableTextReg.sub(" \\1\\2", class_module_name)
            })


def checkFolderIsset():
    log(f"*  Check and make sure directories exist...")
    for d in extension_dirs:
        dir_ = os.path.join(folder_web_extensions, d)
        if not os.path.exists(dir_):
            log(f"* Dir <{d}> is not found, creating...")
            os.mkdir(dir_)
            log(f"* Dir <{d}> created!")
   

def installNodes():
    log(f"\n-------> Easy Node Installing [DEBUG] <-------")
    checkFolderIsset()   
    web_extensions_dir = os.path.join(folder_web_extensions, extension_dirs[0])
    
    # Iterar sobre archivos Python que representan nodos
    for file in os.listdir(extension_folder):
        if file.startswith('__') or not file.endswith('_node.py'):
            continue  # Ignorar archivos que no son nodos
        
        nodeElement = file[:-3]  # Remover la extensión '.py' para obtener el nombre del nodo
        log(f"* Node <{nodeElement}> is found, installing...")
        
        # Manejo de archivos JS
        js_file_name = f"{nodeElement}.js"
        src_js_file = os.path.join(js_source_folder, js_file_name)
        dst_js_file = os.path.join(web_extensions_dir, js_file_name)
        
        if os.path.exists(src_js_file):
            if not os.path.exists(web_extensions_dir):
                os.makedirs(web_extensions_dir)
                log(f"    [*] Created directory '{web_extensions_dir}' for JS files.")
            
            if not os.path.exists(dst_js_file) or not filecmp.cmp(src_js_file, dst_js_file, shallow=False):
                shutil.copy(src_js_file, dst_js_file)
                log(f"    [*] Copied/Updated JS file '{js_file_name}' to '{web_extensions_dir}'.")
            else:
                log(f"    [*] JS file '{js_file_name}' is already up to date.")
        else:
            log(f"    [!] JS file '{js_file_name}' not found in '{js_source_folder}'. Skipping JS copy.")
        
        # Manejo de archivos Lib si es necesario
        # Si tienes una carpeta 'lib' a nivel de extensión, puedes manejarla de manera similar
        # Por ejemplo:
        # lib_src_folder = os.path.join(extension_folder, "lib")
        # lib_dst_folder = folder_web_lib
        # addFilesToFolder(lib_src_folder, lib_dst_folder, nodeElement)
        
        # Verificar e instalar dependencias
        checkModules(nodeElement)
        
        # Agregar al mapeo de nodos
        addComfyUINodesToMapping(nodeElement)
                

installNodes()

__version__ = VERSION

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

def install_nodes():
    js_folder = os.path.join(HOME_PATH, "js")
    install_folder = os.path.join(COMFY_WEB_EXTENSIONS_PATH, ADDON_NAME)

    checkDir(install_folder)
    addFilesToDir(js_folder, install_folder)
    
load_config()
install_nodes()
