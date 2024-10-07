import os

class CreateZNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"tooltip": "The path where the folder will be created."}),
                "folder_name": ("STRING", {"tooltip": "The name of the folder to create."}),
            }
        }

    RETURN_TYPES = ()  # No hay salidas explícitas
    FUNCTION = "create_folder"
    CATEGORY = "file_operations"
    OUTPUT_NODE = True

    def create_folder(self, path, folder_name):
        # Validación de inputs
        if not os.path.exists(path):
            print(f"Error: The path {path} does not exist.")
            return None

        # Construir la ruta final para la nueva carpeta
        folder_path = os.path.join(path, folder_name)

        # Crear la carpeta si no existe
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_name}' created at {folder_path}")
        else:
            print(f"Folder '{folder_name}' already exists at {folder_path}")

        return ()  # No hay salidas necesarias
