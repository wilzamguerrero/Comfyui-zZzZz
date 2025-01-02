import subprocess
import os
import platform
import threading
import socket
import time
import re
import urllib.request
import atexit
import requests
from random import randint
from threading import Timer
from queue import Queue
from multiprocessing import Process

# Detección automática del entorno
if 'COLAB_GPU' in os.environ:  # Google Colab
    base_path = "/content"
    print("Entorno detectado: Google Colab")
elif os.path.exists('/kaggle'):  # Kaggle
    base_path = "/kaggle/working"
    print("Entorno detectado: Kaggle")
elif os.path.exists('/teamspace'):  # Lightning AI
    base_path = "/teamspace/studios/this_studio"
    print("Entorno detectado: Lightning")
else:
    print("Entorno no detectado, seleccionando Google Colab por defecto.")
    base_path = "/content"

sdzc_path = os.path.join(base_path, "SDZC")

class InfiniteZNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "port": ("INT", {
                    "default": 8001,  
                    "min": 1000,      
                    "max": 999999,      
                    "step": 1,        
                    "display": "number"  
                }),
                "tunnel_option": (["LocalPort", "LocalTunnel", "Serveo", "Cloudfl", "Zrok","Pinggy"], {"default": "LocalPort"})
            }
        }

    RETURN_TYPES = ("STRING",)  
    RETURN_NAMES = ("public_info",)
    FUNCTION = "execute_infinite_browser"
    CATEGORY = "zZzZz"
    OUTPUT_NODE = False

    def execute_infinite_browser(self, port, tunnel_option="LocalTunnel"):
        try:
            node_path = os.path.dirname(os.path.abspath(__file__))
            root_path = os.path.abspath(os.path.join(node_path, "..", ".."))
            app_py_path = os.path.join(root_path, "app.py")

            if not os.path.exists(app_py_path):
                error_message = f"Error: {app_py_path} no existe."
                print(error_message)
                return (error_message,)

            python_command = "python" if platform.system() == "Windows" else "python3"
            subprocess.Popen([python_command, app_py_path, f"--port={port}"], cwd=root_path)

            if tunnel_option == "LocalTunnel":
                return self.local_tunnel(port)
            elif tunnel_option == "Serveo":
                return self.serveo_tunnel(port)
            elif tunnel_option == "Cloudfl":
                return self.cloudfl_tunnel(port)
            elif tunnel_option == "Zrok":
                return self.zrok_tunnel(port)
            elif tunnel_option == "Pinggy":
                return self.pinggy_tunnel(port)
            elif tunnel_option == "LocalPort":
                return self.localhost_tunnel(port)  
            else:
                error_message = "Opción de túnel inválida."
                print(error_message)
                return (error_message,)
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            return (error_message,)

    def localhost_tunnel(self, port):
        local_url = f"http://127.0.0.1:{port}"
        print(f"Host Local: {local_url}")
        return (f"Host Local: {local_url}",)


    def local_tunnel(self, port):
        def iframe_thread(port, url_container):
            while True:
                time.sleep(0.5)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('127.0.0.1', int(port)))
                if result == 0:
                    break
                sock.close()

            password = urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip("\n")
            print("La contraseña de LocalTunnel es:", password) 

            p = subprocess.Popen(["lt", "--port", "{}".format(port)], stdout=subprocess.PIPE)
            for line in p.stdout:
                decoded_line = line.decode()
                if "https://" in decoded_line:
                    url_container.append(decoded_line.strip())
                    break

            return password

        url_container = []
        password = iframe_thread(port, url_container)
        public_url = url_container[0] if url_container else "Error: URL no generada."

        print(f"URL Pública de LocalTunnel: {public_url}")

        return (f"URL: {public_url}, Contraseña: {password}",)

    def serveo_tunnel(self, port):
        def serveo_thread(url_container):
            p = subprocess.Popen(
                ["ssh", "-o", "StrictHostKeyChecking=no", "-R", f"80:localhost:{port}", "serveo.net"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            for line in p.stdout:
                if "Forwarding HTTP traffic from" in line:
                    url_container.append(line.split(' ')[-1].strip())
                    break

        url_container = []
        thread = threading.Thread(target=serveo_thread, daemon=True, args=(url_container,))
        thread.start()
        thread.join()
        public_url = url_container[0] if url_container else "Error: URL no generada."

        print(f"URL Pública de Serveo: {public_url}")

        return (f"URL: {public_url}",)


    def cloudfl_tunnel(self, port):
        def run_cloudfl(port, metrics_port, output_queue):
          
            atexit.register(lambda p: p.terminate(), subprocess.Popen(
                [f'{sdzc_path}/cf', 'tunnel', '--url', f'http://127.0.0.1:{port}', '--metrics', f'127.0.0.1:{metrics_port}'],
                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            ))
            attempts, tunnel_url = 0, None
            while attempts < 10 and not tunnel_url:
                attempts += 1
                time.sleep(3)
                try:
                    metrics = requests.get(f'http://127.0.0.1:{metrics_port}/metrics').text
                    tunnel_url = re.search(r"(?P<url>https?:\/\/[^\s]+.trycloudflare.com)", metrics).group("url")
                except Exception as e:
                    print(f"Intento {attempts}: no se pudo obtener la URL - {e}")
                    pass

            if not tunnel_url:
                raise Exception("No se pudo conectar a Cloudflare Edge")
            output_queue.put(tunnel_url)

        output_queue = Queue()
        metrics_port = randint(8100, 9000) 
        thread = Timer(2, run_cloudfl, args=(port, metrics_port, output_queue))
        thread.start()
        thread.join()
        tunnel_url = output_queue.get()

        print(f"URL Pública de Cloudflare: {tunnel_url}")
        return (f"URL: {tunnel_url}",)

    def zrok_tunnel(self, port):
        try:
            os.chdir(sdzc_path)
            command = f'python {os.path.join(sdzc_path, "app.py")} '
            os.chmod(os.path.join(sdzc_path, 'zrok'), 0o777)
            cmd = f'{command} & {os.path.join(sdzc_path, "zrok share public http://localhost:{port} --headless")} '
            subprocess.Popen(cmd, shell=True)
        
            return ("Revisa el output para la URL de Zrok",)

        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            return (error_message,)


    def pinggy_tunnel(self, port):
        try:
            log_file = 'log.txt'
            open(log_file, 'w').close()

            def run_app():
                cmd = f"python {os.path.join(sdzc_path, 'app.py')} & ssh -o StrictHostKeyChecking=no -p 80 -R0:localhost:{port} a.pinggy.io"
                with open(log_file, 'w') as log:
                    process = subprocess.Popen(cmd, shell=True, stdout=log, stderr=subprocess.STDOUT)
                    process.wait()
                    
            def print_url():
                time.sleep(2)
                
                found = False
                while not found:
                    with open(log_file, 'r') as file:
                        end_word = '.pinggy.link'
                        for line in file:
                            start_index = line.find("http:")
                            if start_index != -1:
                                end_index = line.find(end_word, start_index)
                                if end_index != -1:
                                    url = line[start_index:end_index + len(end_word)]
                                    print(f"URL de Pinggy: {url}")
                                    found = True
                    if not found:
                        time.sleep(2)
                    
            p_app = Process(target=run_app)
            p_url = Process(target=print_url)

            p_app.start()
            p_url.start()

            return ("Revisa el output para la URL de Pinggy",)

        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            return (error_message,)
