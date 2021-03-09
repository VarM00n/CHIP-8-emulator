import random


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
    stack = []
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
        for i in range(0, 32):
            self.monitor.append([])
            for j in range(0, 64):
                self.monitor[i].append(0)
        self.pc = 0x200
        f = open("Chip8_Picture.ch8", "rb")
        content = f.read()
        for i in range(0, len(content)):
            self.memory[i + self.pc] = content[i]

    def play(self):
        while self.memory[self.pc] + self.memory[self.pc + 1] != 0:
            opcode = (self.memory[self.pc] << 8) + self.memory[self.pc + 1]
            self.interpreter(opcode)

    def interpreter(self, opcode):
        operation = (opcode & 0xF000) >> 12
        if operation == 0x0:
            sub_operation = (opcode & 0x00FF)
            if sub_operation == 0xE0:  # clear the screen
                for i in range(0, 31):
                    for j in range(0, 63):
                        self.monitor[i][j] = 0
            if sub_operation == 0xEE:  # return from subroutine
                self.pc = self.stack.pop()
        if operation == 0x1:  # jump to the address at NNN
            self.pc = opcode & 0x0FFF
        if operation == 0x2:  # calls a subroutine at NNN
            self.stack.append(self.pc)
            self.pc = opcode & 0x0FFF
        if operation == 0x3:  # jumps to another opcode if v_i[x_n] == nn
            x_n = (opcode & 0x0F00) >> 8
            nn = (opcode & 0x00FF) >> 4
            if self.v_i[x_n] == nn:
                self.pc += 2
        if operation == 0x4:  # jumps to another opcode if v_i[x_n] != nn
            x_n = (opcode & 0x0F00) >> 8
            nn = (opcode & 0x00FF) >> 4
            if self.v_i[x_n] != nn:
                self.pc += 2
        if operation == 0x5:  # jumps to the next opcode if v_i[x_x] == v_i[x_y]
            x_x = (opcode & 0x0F00) >> 8
            x_y = (opcode & 0x00F0) >> 4
            if self.v_i[x_x] == self.v_i[x_y]:
                self.pc += 2
        if operation == 0x6:  # sets v_i[x_x] to nn
            x_x = (opcode & 0x0F00) >> 8
            nn = (opcode & 0x00FF)
            self.v_i[x_x] = nn
        if operation == 0x7:  # adds nn to v_i[x_x]
            x_x = (opcode & 0x0F00) >> 8
            nn = (opcode & 0x00FF)
            self.v_i[x_x] += nn
        if operation == 0x8:  # logic
            sub_operation = (opcode & 0x000F)
            if sub_operation == 0x0:
                x_x = (opcode & 0x0F00) >> 8
                x_y = (opcode & 0x00F0) >> 4
                self.v_i[x_x] = self.v_i[x_y]
            if sub_operation == 0x1:
                x_x = (opcode & 0x0F00) >> 8
                x_y = (opcode & 0x00F0) >> 4
                self.v_i[x_x] = self.v_i[x_x] | self.v_i[x_y]
            if sub_operation == 0x2:
                x_x = (opcode & 0x0F00) >> 8
                x_y = (opcode & 0x00F0) >> 4
                self.v_i[x_x] = self.v_i[x_x] & self.v_i[x_y]
            if sub_operation == 0x3:
                x_x = (opcode & 0x0F00) >> 8
                x_y = (opcode & 0x00F0) >> 4
                self.v_i[x_x] = self.v_i[x_x] ^ self.v_i[x_y]
            if sub_operation == 0x4:
                x_x = (opcode & 0x0F00) >> 8
                x_y = (opcode & 0x00F0) >> 4
                self.v_i[x_x] = self.v_i[x_x] + self.v_i[x_y]
            if sub_operation == 0x5:
                x_x = (opcode & 0x0F00) >> 8
                x_y = (opcode & 0x00F0) >> 4
                self.v_i[x_x] = self.v_i[x_x] - self.v_i[x_y]
            if sub_operation == 0x6:
                x_x = (opcode & 0x0F00) >> 8
                x_y = (opcode & 0x00F0) >> 4
                self.v_i[x_x] = self.v_i[x_y]
                self.v_i[15] = self.v_i[x_x] & 0b00000001
                self.v_i[x_x] = self.v_i[x_x] >> 1
            if sub_operation == 0x7:
                x_x = (opcode & 0x0F00) >> 8
                x_y = (opcode & 0x00F0) >> 4
                self.v_i[x_x] = self.v_i[x_y] - self.v_i[x_x]
            if sub_operation == 0xE:
                x_x = (opcode & 0x0F00) >> 8
                x_y = (opcode & 0x00F0) >> 4
                self.v_i[x_x] = self.v_i[x_y]
                self.v_i[15] = self.v_i[x_x] & 0b00000001
                self.v_i[x_x] = self.v_i[x_x] << 1
        if operation == 0x9:
            x_x = (opcode & 0x0F00) >> 8
            x_y = (opcode & 0x00F0) >> 4
            if self.v_i[x_x] != self.v_i[x_y]:
                self.pc += 2
        if operation == 0xA:
            nnn = opcode & 0x0FFF
            self.I_address_register = nnn
        if operation == 0xB:
            nnn = opcode & 0x0FFF
            self.pc = self.v_i[0] + nnn
        if operation == 0xC:
            x_x = (opcode & 0x0F00) >> 8
            nn = (opcode & 0x00FF)
            self.v_i[x_x] = random.randint(0, 255) & nn
        if operation == 0xD:
            x_x = (opcode & 0x0F00) >> 8
            x_y = (opcode & 0x00F0) >> 4
            n = opcode & 0x000F
            self.v_i[0xF] = 0
            for i in range(0, int(n)):
                row = self.memory[self.I_address_register + i]
                arr = []
                while row != 0:
                    arr.append(int(row % 2))
                    row = int(row / 2)
                while len(arr) != 8:
                    arr.append(0)
                arr = arr[::-1]
                for j in range(0, 7):
                    if self.monitor[(self.v_i[x_x] + i) % 32][(self.v_i[x_y] + j) % 64] == 1 and arr[j] == 0:
                        self.v_i[0xF] = 1
                    self.monitor[(self.v_i[x_x] + i) % 32][(self.v_i[x_y] + j) % 64] = arr[j]
        if operation == 0xE:
            pass
        if operation == 0xF:
            pass
        self.pc += 2


chip = CHIP8()
chip.play()
print("Yeeey")

