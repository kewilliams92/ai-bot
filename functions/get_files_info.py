import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    target_path = os.path.abspath(full_path)

    abs_path = os.path.abspath(working_directory)

    if os.path.commonpath([abs_path, target_path]) != abs_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif os.path.isdir(target_path):
        try:
            metadata = []
            contents = os.listdir(target_path)
            contents.sort()
            for name in contents:
                combined_list = os.path.join(target_path, name)
                if os.path.isdir(combined_list) or os.path.isfile(combined_list):
                    metadata.append(f"- {name}: file_size={os.path.getsize(combined_list)} bytes, is_dir={os.path.isdir(combined_list)}")
            return "\n".join(metadata)
        except Exception as e:
            return f"Error listing files: {e}"
    else:
        return f'Error: "{directory}" is not a directory'
