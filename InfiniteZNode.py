import subprocess
import webbrowser
import os
import platform

class InfiniteZNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "port": ("STRING", {"default": "8080"}),  # Cambia el puerto para el nodo Infinite
                "tunnel_url": ("STRING", {"default": "http://localhost"})  # El mismo túnel de ComfyUI
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "execute_infinite_browser"
    CATEGORY = "zZzZz"
    OUTPUT_NODE = True

    def execute_infinite_browser(self, port, tunnel_url="http://localhost"):
        try:
            # Definir la ruta del nodo y subir dos niveles
            node_path = os.path.dirname(os.path.abspath(__file__))
            root_path = os.path.abspath(os.path.join(node_path, "..", ".."))
            app_py_path = os.path.join(root_path, "app.py")

            if not os.path.exists(app_py_path):
                print(f"Error: {app_py_path} no existe.")
                return ()

            python_command = "python" if platform.system() == "Windows" else "python3"

            # Ejecutar app.py desde la raíz
            subprocess.Popen([python_command, app_py_path, f"--port={port}"], cwd=root_path)
            
            # Abrir el sublink generado por el túnel pero con el puerto del nodo Infinite
            webbrowser.open_new_tab(f"{tunnel_url}:{port}")
            return ()
        except Exception as e:
            print(f"Error: {e}")
            return ()
