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
    eop_exists = check_for_eop(lines)
    if eop_exists:
        starting_address, lines = get_starting_address(lines)
        assembled_lines = list()
        branches = get_branches(starting_address, lines)
        print(branches)
        for line in lines:
            words = clean_preprocessor_directives(line.split())
            instruction = words[0] if words[0] in INSTRUCTION_TO_HEX.keys() else words[1]
            try:
                operand = int(words[-1], 16) if words[-1] != instruction else 0x00
            except ValueError:
                operand = branches[words[-1]]
            starting_address, instruction_str, operand_str = get_instruction_operand_str(starting_address, instruction, operand)
            # assembled_lines.append(instruction_str)
            # assembled_lines.append(operand_str)
            print(words)
            print(f"Instruction: {instruction_str}")
            print(f"Operand: {operand_str}")
    else:
        return []

def get_starting_address(lines: list) -> tuple[int, list]:
    for i, line in enumerate(lines):
        if "ORG" in line:
            lines.pop(i)
            return (int(line.split(" ")[1], 16), lines)
    return (0, lines)

def get_instruction_operand_str(address: int, instruction: int, operand: int) -> tuple[int, str, str]:
    if INSTRUCTION_TO_HEX[instruction]['needs_adding']:
        current_instruction = INSTRUCTION_TO_HEX[instruction]['opcode']
        opcode = (current_instruction << 8) + operand
        instruction = (opcode >> 8) & 0xFF
        operand = opcode & 0xFF
    else:
        instruction = INSTRUCTION_TO_HEX[instruction]['opcode']
    instruction_str = f"ADDR={f"0x{address:X}"};BUS={f"0x{instruction:02X}"};MainMemory();"
    address+=1
    operand_str = f"ADDR={f"0x{address:X}"};BUS={f"0x{operand:02X}"};MainMemory();"
    address+=1
    return (address, instruction_str, operand_str)

def get_branches(address: int, lines: list) -> dict:
    branches = dict()
    for line in lines:
        words = clean_preprocessor_directives(line.split())
        if words[0] not in INSTRUCTION_TO_HEX.keys():
            branches[words[0]] = address + 1
        address+=2
    return branches

def check_for_eop(lines: list) -> bool:
    for line in lines:
        if "EOP" in line:
            return True
    return False

def clean_preprocessor_directives(words: list) -> list:
    try:
        preprocessor_start = words.index(";")
        words = words[:preprocessor_start]
    except ValueError:
        pass
    return words