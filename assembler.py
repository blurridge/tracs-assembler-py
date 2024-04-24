def assemble_to_c(lines: list) -> list:
    starting_address, lines = get_starting_address(lines)
    assembled_lines = list()
    for line in lines:
        


def get_starting_address(lines: list) -> tuple[int, list]:
    for i, line in enumerate(lines):
        if "ORG" in line:
            lines.pop(i)
            return (int(line.split(" ")[1], 16), lines)
    return (0, lines)
