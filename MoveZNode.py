import os
import shutil

class MoveZNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "source": ("STRING", {"tooltip": "The path of the file or folder to move."}),
                "destination": ("STRING", {"tooltip": "The path where the file or folder will be moved."}),
                "folder_name": ("STRING", {"tooltip": "Optional name of a new folder to create at the destination."}),
            }
        }

    RETURN_TYPES = ()  # Sin salidas explícitas, ya que solo movemos archivos o carpetas
    FUNCTION = "move_file_or_folder"
    CATEGORY = "file_operations"
    OUTPUT_NODE = True

    def move_file_or_folder(self, source, destination, folder_name):
        # Validación de inputs
        if not os.path.exists(source):
            print(f"Error: The source path {source} does not exist.")
            return None

        if not os.path.exists(destination):
            print(f"Error: The destination path {destination} does not exist.")
            return None

        # Si se proporciona un nombre de carpeta, creamos esa carpeta en el destino
        if folder_name:
            destination = os.path.join(destination, folder_name)
            if not os.path.exists(destination):
                os.makedirs(destination)
                print(f"Folder {folder_name} created at {destination}")
            else:
                print(f"Folder {folder_name} already exists at {destination}")

        # Construimos la ruta final para mover el archivo o carpeta
        destination_final_path = os.path.join(destination, os.path.basename(source))

        try:
            # Mover archivo o carpeta
            shutil.move(source, destination_final_path)
            print(f"Moved {source} to {destination_final_path}")
            return ()  # No necesitamos retornar nada
        except Exception as e:
            print(f"Error moving file or folder: {e}")
            return ()  # Devuelve un tuple vacío en caso de error
