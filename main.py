import os
from assembler import assemble_to_c

DATA_PATH = "./data"


def main():
    for filename in os.listdir(DATA_PATH):
        with open(os.path.join(DATA_PATH, filename), "r") as current_file:
            lines = [line.rstrip("\n") for line in current_file if line is not None]
            assemble_to_c(lines)


if __name__ == "__main__":
    main()
