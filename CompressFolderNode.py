import os
import zipfile
import webbrowser

class CompressFolderNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"tooltip": "The path of the folder or file to compress."}),
            }
        }

    RETURN_TYPES = ()  # Sin salidas explícitas ya que solo comprimimos la carpeta o archivo
    FUNCTION = "compress_folder_or_file"
    CATEGORY = "compression"
    OUTPUT_NODE = True

    def compress_folder_or_file(self, path):
        # Validación de inputs
        if path is None:
            print("Error: Path is None. Please provide a valid folder or file path.")
            return None

        if not isinstance(path, str):
            print("Error: Path must be a string.")
            return None

        # Verificar si el path existe
        if not os.path.exists(path):
            print(f"Error: The path {path} does not exist.")
            return None

        try:
            # Si es un archivo, lo comprimimos directamente
            if os.path.isfile(path):
                # Crear el nombre del archivo ZIP basado en el nombre del archivo
                zip_filename = os.path.basename(path) + ".zip"
                zip_filepath = os.path.join(os.path.dirname(path), zip_filename)

                # Comprimir el archivo en un ZIP
                with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(path, os.path.basename(path))

                print(f"File compressed successfully to {zip_filepath}")

            # Si es una carpeta, comprimimos su contenido
            elif os.path.isdir(path):
                # Crear el nombre del archivo ZIP basado en el nombre de la carpeta
                zip_filename = os.path.basename(path) + ".zip"
                zip_filepath = os.path.join(os.path.dirname(path), zip_filename)

                # Crear el archivo ZIP
                with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.relpath(file_path, path))

                print(f"Folder compressed successfully to {zip_filepath}")

            else:
                print(f"Error: The path {path} is neither a file nor a folder.")
                return None

            # Abrir el archivo ZIP en el navegador para descargar
            webbrowser.open(f"file://{os.path.abspath(zip_filepath)}")

            return ()  # No necesitamos retornar nada

        except Exception as e:
            print(f"Error while compressing the folder or file: {e}")
            return ()  # Devuelve un tuple vacío en caso de error
