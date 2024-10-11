import os
import shutil

class DeleteZNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "target_path": ("STRING", {"tooltip": "The path of the file or folder to delete."}),
            }
        }

    RETURN_TYPES = ()  # Sin salidas explícitas, ya que solo eliminamos archivos o carpetas
    FUNCTION = "delete_file_or_folder"
    CATEGORY = "zZzZz"
    OUTPUT_NODE = True

    def delete_file_or_folder(self, target_path):
        # Validación de inputs
        if not os.path.exists(target_path):
            print(f"Error: The path {target_path} does not exist.")
            return None

        try:
            # Verificar si es un archivo o carpeta y eliminar en consecuencia
            if os.path.isfile(target_path):
                os.remove(target_path)
                print(f"File {target_path} deleted successfully.")
            elif os.path.isdir(target_path):
                shutil.rmtree(target_path)
                print(f"Folder {target_path} and its contents deleted successfully.")
            return ()  # No necesitamos retornar nada
        except Exception as e:
            print(f"Error deleting file or folder: {e}")
            return ()  # Devuelve un tuple vacío en caso de error
