from aiofile import AIOFile

async def obtain_text_file_as_string(file_path: str) -> str:
    """
    This function reads a text file from the given path and returns it as a string

    Parameters:
    file_path(str): The path where the file is located

    Returns:
    str: The file as a string
    """
    async with AIOFile(file_path, 'r') as text_file:
        text_string = await text_file.read()
        return text_string