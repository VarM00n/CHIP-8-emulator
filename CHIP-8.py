

class CHIP8:
    # Memory
    memory = []
    # Registers
    v_i = []
    I_address_register = 0
    pc = 0x200
    # Timer & sound
    delayTimer = 0
    soundTimer = 0
    # Stack
    stack = 0
    sp = 0
    # Screen
    monitor = []
    # Input
    keyboard = []
    # Font
    font = [0x60, 0x90, 0x90, 0x90, 0x60,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0x60, 0x90, 0x20, 0x40, 0xF0,  # 2
            0x60, 0x90, 0x20, 0x90, 0x60,  # 3
            0x60, 0xA0, 0xA0, 0xF0, 0x20,  # 4
            0xF0, 0x80, 0xE0, 0x10, 0xE0,  # 5
            0x70, 0x80, 0xE0, 0x90, 0x60,  # 6
            0xE0, 0x10, 0x20, 0x40, 0x80,  # 7
            0x60, 0x90, 0x60, 0x90, 0x60,  # 8
            0x60, 0x90, 0x70, 0x10, 0xE0,  # 9
            0x60, 0x90, 0x90, 0xF0, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0x70, 0x80, 0x80, 0x80, 0x70,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0x70, 0x80, 0xE0, 0x80, 0x70,  # E
            0x70, 0x80, 0xE0, 0x80, 0x80   # F
            ]

    def __init__(self):
        # assigning memory
        for i in range(0, 4096):
            self.memory.append(0)
        # assigning font into memory
        for i in range(0, 80):
            self.memory[i] = self.font[i]
        # assigning v_i
        for i in range(0, 16):
            self.v_i.append(0)
            self.keyboard.append(0)
        for i in range(0, 64*32):
            self.monitor.append(0)

    def interpreter(self, opcode):
        operation = (opcode & 0xF000) >> 12
        if operation == 0x0:
            suboperation = (opcode & 0x00FF) >> 8
            if suboperation == 0xE0: # clear the screen
                for i in range(0, 64*32):
                    self.monitor[i] = 0
            if suboperation == 0xEE: # return from subroutine
                pass
            




chip = CHIP8()
chip.interpreter(0xA0E0)
