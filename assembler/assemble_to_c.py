INSTRUCTION_TO_HEX = {
    "ADD": {"opcode": 0xF0, "needs_adding": False},
    "SUB": {"opcode": 0xE8, "needs_adding": False},
    "MUL": {"opcode": 0xD8, "needs_adding": False},
    "AND": {"opcode": 0xD0, "needs_adding": False},
    "OR": {"opcode": 0xC8, "needs_adding": False},
    "NOT": {"opcode": 0xC0, "needs_adding": False},
    "XOR": {"opcode": 0xB8, "needs_adding": False},
    "SHL": {"opcode": 0xB0, "needs_adding": False},
    "SHR": {"opcode": 0xA8, "needs_adding": False},
    "WM": {"opcode": 0x08, "needs_adding": True},
    "RM": {"opcode": 0x10, "needs_adding": True},
    "RIO": {"opcode": 0x20, "needs_adding": True},
    "WIO": {"opcode": 0x28, "needs_adding": True},
    "WB": {"opcode": 0x30, "needs_adding": False},
    "WIB": {"opcode": 0x38, "needs_adding": False},
    "WACC": {"opcode": 0x48, "needs_adding": False},
    "RACC": {"opcode": 0x58, "needs_adding": False},
    "SWAP": {"opcode": 0x70, "needs_adding": False},
    "BR": {"opcode": 0x18, "needs_adding": True},
    "BRE": {"opcode": 0xA0, "needs_adding": True},
    "BRNE": {"opcode": 0x98, "needs_adding": True},
    "BRGT": {"opcode": 0x90, "needs_adding": True},
    "BRLT": {"opcode": 0x88, "needs_adding": True},
    "EOP": {"opcode": 0xF8, "needs_adding": False},
}


def assemble_to_c(lines: list) -> list:
    """
    Convert assembly language lines to C instructions for processing in memory.

    Parameters:
        lines (list): List of strings, each representing a line of assembly code.

    Returns:
        list: A list of strings formatted as C instructions that simulate writing to memory.
    """
    eop_exists = check_for_eop(lines)
    if eop_exists:
        starting_address, lines = get_starting_address(lines)
        assembled_lines = list()
        branches = get_branches(starting_address, lines)
        for line in lines:
            words = clean_preprocessor_directives(line.split())
            if words[0] in INSTRUCTION_TO_HEX.keys():
                instruction = words[0]
            elif words[1] in INSTRUCTION_TO_HEX.keys():
                instruction = words[1]
            else:
                print(f"[ERROR] Invalid instruction found in {line}.")
                return []
            try:
                operand = int(words[-1], 16) if words[-1] != instruction else 0x00
            except ValueError:
                operand = branches[words[-1]]
            starting_address, instruction_str, operand_str = (
                get_instruction_operand_str(starting_address, instruction, operand)
            )
            assembled_lines.append(instruction_str)
            assembled_lines.append(operand_str)
        return assembled_lines
    else:
        print(f"[ERROR] EOP not found.")
        return []


def get_starting_address(lines: list) -> tuple[int, list]:
    """
    Extracts the starting address from assembly lines that contain the ORG directive.

    Parameters:
        lines (list): List of strings, each representing a line of assembly code.

    Returns:
        tuple: A tuple containing the starting address as an integer and the list of assembly lines without the ORG line.
    """
    for i, line in enumerate(lines):
        if "ORG" in line:
            lines.pop(i)
            return (int(line.split(" ")[1], 16), lines)
    return (0, lines)


def get_instruction_operand_str(
    address: int, instruction: int, operand: int
) -> tuple[int, str, str]:
    """
    Formats the address, instruction, and operand into strings that simulate memory operations.

    Parameters:
        address (int): The current memory address.
        instruction (str): The assembly instruction.
        operand (int): The operand for the instruction.

    Returns:
        tuple: A tuple containing the next address and strings representing the C instructions for instruction and operand.
    """
    if INSTRUCTION_TO_HEX[instruction]["needs_adding"]:
        current_instruction = INSTRUCTION_TO_HEX[instruction]["opcode"]
        opcode = (current_instruction << 8) + operand
        instruction = (opcode >> 8) & 0xFF
        operand = opcode & 0xFF
    else:
        instruction = INSTRUCTION_TO_HEX[instruction]["opcode"]
    instruction_str = f"ADDR=0x{address:02X};BUS=0x{instruction:02X};MainMemory();"
    address += 1
    operand_str = f"ADDR=0x{address:02X};BUS=0x{operand:02X};MainMemory();"
    address += 1
    return (address, instruction_str, operand_str)


def get_branches(address: int, lines: list) -> dict:
    """
    Maps branch labels to addresses based on their occurrence in the list of assembly lines.

    Parameters:
        address (int): Starting address for mapping branches.
        lines (list): List of strings, each representing a line of assembly code.

    Returns:
        dict: A dictionary mapping branch labels to their respective addresses.
    """
    branches = dict()
    for line in lines:
        words = clean_preprocessor_directives(line.split())
        if words[0] not in INSTRUCTION_TO_HEX.keys():
            branches[words[0]] = address
        address += 2
    return branches


def check_for_eop(lines: list) -> bool:
    """
    Checks whether the 'EOP' (End of Program) instruction exists in the assembly lines.

    Parameters:
        lines (list): List of strings, each representing a line of assembly code.

    Returns:
        bool: True if 'EOP' is found in the lines, otherwise False.
    """
    for line in lines:
        if "EOP" in line:
            return True
    return False


def clean_preprocessor_directives(words: list) -> list:
    """
    Removes comments and other preprocessor directives from a list of words.

    Parameters:
        words (list): List of strings, words split from a line of assembly code.

    Returns:
        list: A list of words cleaned of preprocessor directives.
    """
    try:
        preprocessor_start = words.index(";")
        words = words[:preprocessor_start]
    except ValueError:
        pass
    return words
