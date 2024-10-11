import subprocess
import webbrowser
import os
import platform

class InfiniteZNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "port": ("STRING", {"default": "7888"}),
                "tunnel_url": ("STRING", {"default": ""}),  # Nueva opción para la URL del túnel
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "execute_infinite_browser"
    CATEGORY = "zZzZz"
    OUTPUT_NODE = True

    def execute_infinite_browser(self, port, tunnel_url=""):
        try:
            # Ruta al archivo app.py
            node_path = os.path.dirname(os.path.abspath(__file__))
            root_path = os.path.abspath(os.path.join(node_path, "..", "..", ".."))  # Subir tres niveles
            app_py_path = os.path.join(root_path, "app.py")

            if not os.path.exists(app_py_path):
                print(f"Error: {app_py_path} no existe.")
                return ()

            python_command = "python" if platform.system() == "Windows" else "python3"

            # Ejecutar app.py desde la raíz
            subprocess.Popen([python_command, app_py_path, f"--port={port}"], cwd=root_path)

            # Si se proporcionó una URL de túnel, usarla
            if tunnel_url:
                webbrowser.open_new_tab(f"{tunnel_url}")
            else:
                webbrowser.open_new_tab(f"http://localhost:{port}")

            return ()
        except Exception as e:
            print(f"Error: {e}")
            return ()
