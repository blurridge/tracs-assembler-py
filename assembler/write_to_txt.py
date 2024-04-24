import os

OUTPUT_PATH = "./output"


def write_to_txt(original_file_name: str, assembled_lines: list) -> None:
    with open(
        os.path.join(OUTPUT_PATH, f"{original_file_name}_assembled.txt"), "w"
    ) as current_txt_file:
        for line in assembled_lines:
            current_txt_file.write(f"{line}\n")
