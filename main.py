import os
from assembler import assemble_to_c, write_to_txt

DATA_PATH = "./data"


def main():
    for filename in os.listdir(DATA_PATH):
        with open(os.path.join(DATA_PATH, filename), "r") as current_file:
            lines = [line.rstrip("\n") for line in current_file if line is not None]
            assembled_lines = assemble_to_c(lines)
            if assembled_lines:
                write_to_txt(filename, assembled_lines)
            else:
                print(f"[ERROR] Cancelling assembly for {filename}.")


if __name__ == "__main__":
    main()
