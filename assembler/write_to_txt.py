import os

OUTPUT_PATH = "./output"


def write_to_txt(original_file_name: str, assembled_lines: list) -> None:
    """
    Writes the provided list of lines to a text file with a modified file name.

    This function creates a text file named `{original_file_name}_assembled.txt`
    in a predetermined output directory. Each line from the list `assembled_lines`
    is written to this file, followed by a newline character.

    Parameters:
        original_file_name (str): The base name of the file to which the lines
                                  will be written, without the file extension.
        assembled_lines (list): A list of strings, each representing a line to
                                be written to the file.

    Returns:
        None
    """
    with open(
        os.path.join(OUTPUT_PATH, f"{original_file_name}_assembled.txt"), "w"
    ) as current_txt_file:
        for line in assembled_lines:
            current_txt_file.write(f"{line}\n")
