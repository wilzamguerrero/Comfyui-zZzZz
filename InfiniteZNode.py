import subprocess
import webbrowser
import os
import platform
import threading
import socket
import time

class InfiniteZNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "port": ("STRING", {"default": "8188"}),
                "tunnel_option": ("STRING", {"default": "LocalTunnel", "choices": ["LocalTunnel", "Serveo", "Pinggy"]})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "execute_infinite_browser"
    CATEGORY = "zZzZz"
    OUTPUT_NODE = True

    def execute_infinite_browser(self, port, tunnel_option="LocalTunnel"):
        try:
            node_path = os.path.dirname(os.path.abspath(__file__))
            root_path = os.path.abspath(os.path.join(node_path, "..", ".."))
            app_py_path = os.path.join(root_path, "app.py")

            if not os.path.exists(app_py_path):
                print(f"Error: {app_py_path} no existe.")
                return ()

            python_command = "python" if platform.system() == "Windows" else "python3"
            subprocess.Popen([python_command, app_py_path, f"--port={port}"], cwd=root_path)

            if tunnel_option == "LocalTunnel":
                self.local_tunnel(port)
            elif tunnel_option == "Serveo":
                self.serveo_tunnel(port)
            elif tunnel_option == "Pinggy":
                self.pinggy_tunnel(port)
            else:
                print("Opción de túnel inválida.")
            
            return ()
        except Exception as e:
            print(f"Error: {e}")
            return ()

    def local_tunnel(self, port):
        def iframe_thread(port):
            while True:
                time.sleep(0.5)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('127.0.0.1', port))
                if result == 0:
                    break
                sock.close()

            p = subprocess.Popen(["lt", "--port", "{}".format(port)], stdout=subprocess.PIPE)
            for line in p.stdout:
                print(line.decode(), end='')

        threading.Thread(target=iframe_thread, daemon=True, args=(port,)).start()

    def serveo_tunnel(self, port):
        def serveo_thread():
            p = subprocess.Popen(
                ["ssh", "-o", "StrictHostKeyChecking=no", "-R", f"80:localhost:{port}", "serveo.net"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            for line in p.stdout:
                if "Forwarding HTTP traffic from" in line:
                    print(line.split(' ')[-1].strip())

        threading.Thread(target=serveo_thread, daemon=True).start()

    def pinggy_tunnel(self, port):
        from multiprocessing import Process

        def run_app():
            cmd = f"ssh -o StrictHostKeyChecking=no -p 80 -R0:localhost:{port} a.pinggy.io > log.txt"
            subprocess.call(cmd, shell=True)

        def print_url():
            time.sleep(2)
            found = False
            with open('log.txt', 'r') as file:
                for line in file:
                    if '.pinggy.link' in line:
                        url = line.strip()
                        print(f"Pinggy URL: {url}")
                        found = True
            if not found:
                print_url()

        p_app = Process(target=run_app)
        p_url = Process(target=print_url)
        p_app.start()
        p_url.start()
        p_app.join()
        p_url.join()
