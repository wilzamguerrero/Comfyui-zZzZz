import os

class RenameZNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "source_path": ("STRING", {"tooltip": "The path of the file or folder to rename."}),
                "new_name": ("STRING", {"tooltip": "The new name for the file or folder."}),
            }
        }

    RETURN_TYPES = ()  # Sin salidas explícitas, ya que solo renombramos archivos o carpetas
    FUNCTION = "rename_file_or_folder"
    CATEGORY = "zZzZz"
    OUTPUT_NODE = True

    def rename_file_or_folder(self, source_path, new_name):
        # Validación de inputs
        if not os.path.exists(source_path):
            print(f"Error: The path {source_path} does not exist.")
            return None

        # Obtener la ruta del directorio del archivo/carpeta
        directory = os.path.dirname(source_path)
        destination = os.path.join(directory, new_name)

        try:
            # Renombrar archivo o carpeta
            os.rename(source_path, destination)
            print(f"Renamed {source_path} to {destination}")
            return ()  # No necesitamos retornar nada
        except Exception as e:
            print(f"Error renaming file or folder: {e}")
            return ()  # Devuelve un tuple vacío en caso de error
