import subprocess
import webbrowser
import os
import platform

class InfiniteZNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "port": ("STRING", {"default": "7888"})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "execute_infinite_browser"
    CATEGORY = "zZzZz"
    OUTPUT_NODE = True

    def execute_infinite_browser(self, port):
        try:
            # Definir la ruta del nodo y subir dos niveles
            node_path = os.path.dirname(os.path.abspath(__file__))
            root_path = os.path.abspath(os.path.join(node_path, "..", ".."))  # Subir dos niveles
            app_py_path = os.path.join(root_path, "app.py")  # app.py en la raíz

            if not os.path.exists(app_py_path):
                print(f"Error: {app_py_path} no existe.")
                return ()

            python_command = "python" if platform.system() == "Windows" else "python3"

            # Ejecutar app.py desde la raíz
            subprocess.Popen([python_command, app_py_path, f"--port={port}"], cwd=root_path)
            webbrowser.open_new_tab(f"http://localhost:{port}")
            return ()
        except Exception as e:
            print(f"Error: {e}")
            return ()
