import os


def delete_files_in_folder(folder_path):
    """
    Delete all files within a specified folder path.

    Parameters:
    folder_path (str): Path to the folder containing files to be deleted.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

