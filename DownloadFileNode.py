import os
import requests
import zipfile

class DownloadFileNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "url": ("STRING", {"tooltip": "The URL of the file to download."}),
                "path": ("STRING", {"tooltip": "The path where the file will be saved."}),
            },
            "optional": {
                "custom_name": ("STRING", {"tooltip": "Custom name for the downloaded file (optional). If not provided, the original file name will be used."}),
            }
        }

    RETURN_TYPES = ()  # Asegúrate de que no haya RETURN_TYPES si no hay outputs
    FUNCTION = "download_file"
    CATEGORY = "download"
    OUTPUT_NODE = True

    def download_file(self, url, path, custom_name=None):
        # Validación de inputs
        if url is None or path is None:
            print("Error: URL or path is None. Please check the inputs.")
            return None  # Devuelve None explícitamente si hay un error

        if not isinstance(url, str) or not isinstance(path, str):
            print("Error: URL and path must be strings.")
            return None  # Devuelve None explícitamente si hay un error

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Obtener el nombre del archivo de la URL
            filename = custom_name if custom_name else os.path.basename(url)
            filepath = os.path.join(path, filename)

            # Verificar si el directorio existe
            if not os.path.exists(path):
                os.makedirs(path)

            # Descargar el archivo
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"File downloaded successfully to {filepath}")

            # Verificar si el archivo descargado es un archivo ZIP
            if zipfile.is_zipfile(filepath):
                print(f"The file {filename} is a ZIP file, extracting...")

                # Crear una carpeta con el mismo nombre que el archivo ZIP (sin la extensión .zip)
                extract_dir = os.path.join(path, os.path.splitext(filename)[0])
                if not os.path.exists(extract_dir):
                    os.makedirs(extract_dir)

                # Descomprimir el archivo ZIP en la carpeta creada
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)

                print(f"File extracted successfully to {extract_dir}")

            return ()  # Devuelve un tuple vacío para evitar el error de longitud

        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")
            return ()  # Devuelve un tuple vacío para evitar el error de longitud

        except zipfile.BadZipFile as e:
            print(f"Error: The file {filename} is not a valid ZIP file or is corrupted: {e}")
            return ()  # Devuelve un tuple vacío en caso de error con el archivo ZIP
