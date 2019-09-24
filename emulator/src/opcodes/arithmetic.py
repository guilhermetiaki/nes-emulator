from more_itertools import flatten

from constants import AddressingMode
from opcodes.base import OpCode


class ORA(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0x01, AddressingMode.INDIRECT_X, 6,),
                      (0x05, AddressingMode.ZERO_PAGE, 3,),
                      (0x09, AddressingMode.IMMEDIATE, 2,),
                      (0x0D, AddressingMode.ABSOLUTE, 4,),
                      (0x11, AddressingMode.INDIRECT_Y, 5,),
                      (0x15, AddressingMode.ZERO_PAGE_X, 4,),
                      (0x19, AddressingMode.ABSOLUTE_Y, 4,),
                      (0x1D, AddressingMode.ABSOLUTE_X, 4,)]
        return map(cls.create_dict_entry, variations)
    def exec(cls, cpu, memory):
        opcode = memory.fetch(cpu.pc-1)
        if opcode == 0x01:
            cpu.a = cpu.a | memory.fetch(memory.fetch(memory.fetch(cpu.pc) + memory.fetch(cpu.x)))
            cpu.pc += 1
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x05:
            cpu.a = cpu.a | memory.fetch(memory.fetch(cpu.pc))
            cpu.pc += 1
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x09:
            cpu.a = cpu.a | memory.fetch(cpu.pc)
            cpu.pc += 1
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
        elif opcode == 0x0D:
            cpu.a = cpu.a | memory.fetch(memory.fetch(cpu.pc+1) << 8 | memory.fetch(cpu.pc)) 
            cpu.pc += 2
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x11:
            baseAddr = memory.fetch(memory.fetch(cpu.pc))
            indexAddr = memory.fetch(cpu.y) 
            cpu.a = cpu.a | memory.fetch(baseAddr + indexAddr) 
            cpu.pc += 1
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            # Page boundary crossed
            if (baseAddr + indexAddr >> 8) != (baseAddr >> 8):
                cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x15:
            cpu.a = cpu.a | memory.fetch(memory.fetch(cpu.pc) + memory.fetch(cpu.x))
            cpu.pc += 1
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x19:
            baseAddr = (memory.fetch(cpu.pc+1) << 8 | memory.fetch(cpu.pc)) 
            indexAddr = memory.fetch(cpu.y)
            cpu.a = cpu.a | memory.fetch(baseAddr + indexAddr) 
            cpu.pc += 2
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            # Page boundary crossed
            if (baseAddr + indexAddr >> 8) != (baseAddr >> 8):
                cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x1D:
            baseAddr = (memory.fetch(cpu.pc+1) << 8 | memory.fetch(cpu.pc))
            indexAddr = memory.fetch(cpu.x)
            cpu.a = cpu.a | memory.fetch(baseAddr + indexAddr) 
            cpu.pc += 2
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            # Page boundary crossed
            if (baseAddr + indexAddr >> 8) != (baseAddr >> 8):
                cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()

class AND(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0x21, AddressingMode.INDIRECT_X, 6,),
                      (0x25, AddressingMode.ZERO_PAGE, 3,),
                      (0x29, AddressingMode.IMMEDIATE, 2,),
                      (0x2D, AddressingMode.ABSOLUTE, 4,),
                      (0x31, AddressingMode.INDIRECT_Y, 5,),
                      (0x35, AddressingMode.ZERO_PAGE_X, 4,),
                      (0x39, AddressingMode.ABSOLUTE_Y, 4,),
                      (0x3D, AddressingMode.ABSOLUTE_X, 4,)]
        return map(cls.create_dict_entry, variations)
    def exec(cls, cpu, memory):
        opcode = memory.fetch(cpu.pc-1)
        if opcode == 0x21:
            cpu.a = cpu.a & memory.fetch(memory.fetch(memory.fetch(cpu.pc) + memory.fetch(cpu.x)))
            cpu.pc += 1
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x25:
            cpu.a = cpu.a & memory.fetch(memory.fetch(cpu.pc))
            cpu.pc += 1
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x29:
            cpu.a = cpu.a & memory.fetch(cpu.pc)
            cpu.pc += 1
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
        elif opcode == 0x2D:
            cpu.a = cpu.a & memory.fetch(memory.fetch(cpu.pc+1) << 8 | memory.fetch(cpu.pc)) 
            cpu.pc += 2
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x31:
            baseAddr = memory.fetch(memory.fetch(cpu.pc))
            indexAddr = memory.fetch(cpu.y) 
            cpu.a = cpu.a & memory.fetch(baseAddr + indexAddr) 
            cpu.pc += 1
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            # Page boundary crossed
            if (baseAddr + indexAddr >> 8) != (baseAddr >> 8):
                cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x35:
            cpu.a = cpu.a & memory.fetch(memory.fetch(cpu.pc) + memory.fetch(cpu.x))
            cpu.pc += 1
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x39:
            baseAddr = (memory.fetch(cpu.pc+1) << 8 | memory.fetch(cpu.pc)) 
            indexAddr = memory.fetch(cpu.y)
            cpu.a = cpu.a & memory.fetch(baseAddr + indexAddr) 
            cpu.pc += 2
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            # Page boundary crossed
            if (baseAddr + indexAddr >> 8) != (baseAddr >> 8):
                cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x3D:
            baseAddr = (memory.fetch(cpu.pc+1) << 8 | memory.fetch(cpu.pc))
            indexAddr = memory.fetch(cpu.x)
            cpu.a = cpu.a & memory.fetch(baseAddr + indexAddr) 
            cpu.pc += 2
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            # Page boundary crossed
            if (baseAddr + indexAddr >> 8) != (baseAddr >> 8):
                cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()

class EOR(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0x41, AddressingMode.INDIRECT_X, 6,),
                      (0x45, AddressingMode.ZERO_PAGE, 3,),
                      (0x49, AddressingMode.IMMEDIATE, 2,),
                      (0x4D, AddressingMode.ABSOLUTE, 4,),
                      (0x51, AddressingMode.INDIRECT_Y, 5,),
                      (0x55, AddressingMode.ZERO_PAGE_X, 4,),
                      (0x59, AddressingMode.ABSOLUTE_Y, 4,),
                      (0x5D, AddressingMode.ABSOLUTE_X, 4,)]
        return map(cls.create_dict_entry, variations)
    def exec(cls, cpu, memory):
        opcode = memory.fetch(cpu.pc-1)
        if opcode == 0x41:
            cpu.a = cpu.a ^ memory.fetch(memory.fetch(memory.fetch(cpu.pc) + memory.fetch(cpu.x)))
            cpu.pc += 1
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x45:
            cpu.a = cpu.a ^ memory.fetch(memory.fetch(cpu.pc))
            cpu.pc += 1
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x49:
            cpu.a = cpu.a ^ memory.fetch(cpu.pc)
            cpu.pc += 1
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
        elif opcode == 0x4D:
            cpu.a = cpu.a ^ memory.fetch(memory.fetch(cpu.pc+1) << 8 | memory.fetch(cpu.pc)) 
            cpu.pc += 2
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x51:
            baseAddr = memory.fetch(memory.fetch(cpu.pc))
            indexAddr = memory.fetch(cpu.y) 
            cpu.a = cpu.a ^ memory.fetch(baseAddr + indexAddr) 
            cpu.pc += 1
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            # Page boundary crossed
            if (baseAddr + indexAddr >> 8) != (baseAddr >> 8):
                cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x55:
            cpu.a = cpu.a ^ memory.fetch(memory.fetch(cpu.pc) + memory.fetch(cpu.x))
            cpu.pc += 1
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x59:
            baseAddr = (memory.fetch(cpu.pc+1) << 8 | memory.fetch(cpu.pc)) 
            indexAddr = memory.fetch(cpu.y)
            cpu.a = cpu.a ^ memory.fetch(baseAddr + indexAddr) 
            cpu.pc += 2
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            # Page boundary crossed
            if (baseAddr + indexAddr >> 8) != (baseAddr >> 8):
                cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x5D:
            baseAddr = (memory.fetch(cpu.pc+1) << 8 | memory.fetch(cpu.pc))
            indexAddr = memory.fetch(cpu.x)
            cpu.a = cpu.a ^ memory.fetch(baseAddr + indexAddr) 
            cpu.pc += 2
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            # Page boundary crossed
            if (baseAddr + indexAddr >> 8) != (baseAddr >> 8):
                cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()

class ADC(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0x61, AddressingMode.INDIRECT_X, 6,),
                      (0x65, AddressingMode.ZERO_PAGE, 3,),
                      (0x69, AddressingMode.IMMEDIATE, 2,),
                      (0x6D, AddressingMode.ABSOLUTE, 4,),
                      (0x71, AddressingMode.INDIRECT_Y, 5,),
                      (0x75, AddressingMode.ZERO_PAGE_X, 4,),
                      (0x79, AddressingMode.ABSOLUTE_Y, 4,),
                      (0x7D, AddressingMode.ABSOLUTE_X, 4,)]
        return map(cls.create_dict_entry, variations)
    def exec(cls, cpu, memory):
        opcode = memory.fetch(cpu.pc-1)
        if opcode == 0x61:
            addend1 = cpu.a
            addend2 = memory.fetch(memory.fetch(memory.fetch(cpu.pc) + memory.fetch(cpu.x)))
            cpu.a = addend1 + addend2 + cpu.carry
            cpu.pc += 1
            cpu.carry = (cpu.a >> 8) != 0
            cpu.a &= 0xff
            cpu.overflow = addend1 >> 7 == addend2 >> 7 and addend1 >> 7 != cpu.a >> 7
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x65:
            addend1 = cpu.a
            addend2 = memory.fetch(memory.fetch(cpu.pc))
            cpu.a = addend1 + addend2 + cpu.carry
            cpu.pc += 1
            cpu.carry = (cpu.a >> 8) != 0
            cpu.a &= 0xff
            cpu.overflow = addend1 >> 7 == addend2 >> 7 and addend1 >> 7 != cpu.a >> 7
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x69:
            addend1 = cpu.a
            addend2 = memory.fetch(cpu.pc)
            cpu.a = addend1 + addend2 + cpu.carry
            cpu.pc += 1
            cpu.carry = (cpu.a >> 8) != 0
            cpu.a &= 0xff
            cpu.overflow = addend1 >> 7 == addend2 >> 7 and addend1 >> 7 != cpu.a >> 7
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
        elif opcode == 0x6D:
            addend1 = cpu.a
            addend2 = memory.fetch(memory.fetch(cpu.pc+1) << 8 | memory.fetch(cpu.pc)) 
            cpu.a = addend1 + addend2 + cpu.carry
            cpu.pc += 2
            cpu.carry = (cpu.a >> 8) != 0
            cpu.a &= 0xff
            cpu.overflow = addend1 >> 7 == addend2 >> 7 and addend1 >> 7 != cpu.a >> 7
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x71:
            baseAddr = memory.fetch(memory.fetch(cpu.pc))
            indexAddr = memory.fetch(cpu.y) 
            addend1 = cpu.a
            addend2 = memory.fetch(baseAddr + indexAddr)
            cpu.a = addend1 + addend2 + cpu.carry
            cpu.pc += 1
            cpu.carry = (cpu.a >> 8) != 0
            cpu.a &= 0xff
            cpu.overflow = addend1 >> 7 == addend2 >> 7 and addend1 >> 7 != cpu.a >> 7
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            # Page boundary crossed
            if (baseAddr + indexAddr >> 8) != (baseAddr >> 8):
                cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x75:
            addend1 = cpu.a
            addend2 = memory.fetch(memory.fetch(cpu.pc) + memory.fetch(cpu.x))
            cpu.a = addend1 + addend2 + cpu.carry
            cpu.pc += 1
            cpu.carry = (cpu.a >> 8) != 0
            cpu.a &= 0xff
            cpu.overflow = addend1 >> 7 == addend2 >> 7 and addend1 >> 7 != cpu.a >> 7
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x79:
            baseAddr = (memory.fetch(cpu.pc+1) << 8 | memory.fetch(cpu.pc)) 
            indexAddr = memory.fetch(cpu.y)
            addend1 = cpu.a
            addend2 = memory.fetch(baseAddr + indexAddr)
            cpu.a = addend1 + addend2 + cpu.carry
            cpu.pc += 2
            cpu.carry = (cpu.a >> 8) != 0
            cpu.a &= 0xff
            cpu.overflow = addend1 >> 7 == addend2 >> 7 and addend1 >> 7 != cpu.a >> 7
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            # Page boundary crossed
            if (baseAddr + indexAddr >> 8) != (baseAddr >> 8):
                cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0x7D:
            baseAddr = (memory.fetch(cpu.pc+1) << 8 | memory.fetch(cpu.pc))
            indexAddr = memory.fetch(cpu.x)
            addend1 = cpu.a
            addend2 = memory.fetch(baseAddr + indexAddr)
            cpu.a = addend1 + addend2 + cpu.carry
            cpu.pc += 2
            cpu.carry = (cpu.a >> 8) != 0
            cpu.a &= 0xff
            cpu.overflow = addend1 >> 7 == addend2 >> 7 and addend1 >> 7 != cpu.a >> 7
            cpu.negative = cpu.a >> 7 == 1
            cpu.zero = cpu.a == 0
            # Page boundary crossed
            if (baseAddr + indexAddr >> 8) != (baseAddr >> 8):
                cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()

class SBC(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0xE1, AddressingMode.INDIRECT_X, 6),
                      (0xE5, AddressingMode.ZERO_PAGE, 3,),
                      (0xE9, AddressingMode.IMMEDIATE, 2,),
                      (0xED, AddressingMode.ABSOLUTE, 4,),
                      (0xF1, AddressingMode.INDIRECT_Y, 5,),
                      (0xF5, AddressingMode.ZERO_PAGE_X, 4,),
                      (0xF9, AddressingMode.ABSOLUTE_Y, 4,),
                      (0xFD, AddressingMode.ABSOLUTE_X, 4,)]
        return map(cls.create_dict_entry, variations)
    def exec(cls, cpu, memory):
        opcode = memory.fetch(cpu.pc-1)
        if opcode == 0xE1:
            minuend = cpu.a
            subtrahend = memory.fetch(memory.fetch(memory.fetch(cpu.pc) + memory.fetch(cpu.x)))
            cpu.pc += 1
            # One's complement
            subtrahend = abs(~subtrahend-1 ^ 0xFF)
            cpu.a = minuend + subtrahend + cpu.carry
            if cpu.a < 0:
                cpu.a = ~cpu.a ^ 0xFF & 0xFF
            else:
                cpu.a = cpu.a & 0xFF
            cpu.carry = cpu.a >> 7 == 0
            cpu.overflow = minuend >> 7 == subtrahend >> 7 and minuend >> 7 != cpu.a >> 7
            cpu.zero = cpu.a == 0
            cpu.negative = cpu.a >> 7 == 1
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0xE5:
            minuend = cpu.a
            subtrahend = memory.fetch(memory.fetch(cpu.pc))
            cpu.pc += 1
            # One's complement
            subtrahend = abs(~subtrahend-1 ^ 0xFF)
            cpu.a = minuend + subtrahend + cpu.carry
            if cpu.a < 0:
                cpu.a = ~cpu.a ^ 0xFF & 0xFF
            else:
                cpu.a = cpu.a & 0xFF
            cpu.carry = cpu.a >> 7 == 0
            cpu.overflow = minuend >> 7 == subtrahend >> 7 and minuend >> 7 != cpu.a >> 7
            cpu.zero = cpu.a == 0
            cpu.negative = cpu.a >> 7 == 1
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0xE9:
            minuend = cpu.a
            subtrahend = memory.fetch(cpu.pc)
            cpu.pc += 1
            # One's complement
            subtrahend = abs(~subtrahend-1 ^ 0xFF)
            cpu.a = minuend + subtrahend + cpu.carry
            if cpu.a < 0:
                cpu.a = ~cpu.a ^ 0xFF & 0xFF
            else:
                cpu.a = cpu.a & 0xFF
            cpu.carry = cpu.a >> 7 == 0
            cpu.overflow = minuend >> 7 == subtrahend >> 7 and minuend >> 7 != cpu.a >> 7
            cpu.zero = cpu.a == 0
            cpu.negative = cpu.a >> 7 == 1
            cpu.inc_cycle()
        elif opcode == 0xED:
            minuend = cpu.a
            subtrahend = memory.fetch(memory.fetch(cpu.pc+1) << 8 | memory.fetch(cpu.pc)) 
            cpu.pc += 2
            # One's complement
            subtrahend = abs(~subtrahend-1 ^ 0xFF)
            cpu.a = minuend + subtrahend + cpu.carry
            if cpu.a < 0:
                cpu.a = ~cpu.a ^ 0xFF & 0xFF
            else:
                cpu.a = cpu.a & 0xFF
            cpu.carry = cpu.a >> 7 == 0
            cpu.overflow = minuend >> 7 == subtrahend >> 7 and minuend >> 7 != cpu.a >> 7
            cpu.zero = cpu.a == 0
            cpu.negative = cpu.a >> 7 == 1
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0xF1:
            baseAddr = memory.fetch(memory.fetch(cpu.pc))
            indexAddr = memory.fetch(cpu.y) 
            cpu.pc += 1
            minuend = cpu.a
            subtrahend = memory.fetch(baseAddr + indexAddr)
            # One's complement
            subtrahend = abs(~subtrahend-1 ^ 0xFF)
            cpu.a = minuend + subtrahend + cpu.carry
            if cpu.a < 0:
                cpu.a = ~cpu.a ^ 0xFF & 0xFF
            else:
                cpu.a = cpu.a & 0xFF
            cpu.carry = cpu.a >> 7 == 0
            cpu.overflow = minuend >> 7 == subtrahend >> 7 and minuend >> 7 != cpu.a >> 7
            cpu.zero = cpu.a == 0
            cpu.negative = cpu.a >> 7 == 1
            # Page boundary crossed
            if (baseAddr + indexAddr >> 8) != (baseAddr >> 8):
                cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0xF5:
            minuend = cpu.a
            subtrahend = memory.fetch(memory.fetch(cpu.pc) + memory.fetch(cpu.x))
            cpu.pc += 1
            cpu.a = addend1 + addend2 + cpu.carry
            # One's complement
            subtrahend = abs(~subtrahend-1 ^ 0xFF)
            cpu.a = minuend + subtrahend + cpu.carry
            if cpu.a < 0:
                cpu.a = ~cpu.a ^ 0xFF & 0xFF
            else:
                cpu.a = cpu.a & 0xFF
            cpu.carry = cpu.a >> 7 == 0
            cpu.overflow = minuend >> 7 == subtrahend >> 7 and minuend >> 7 != cpu.a >> 7
            cpu.zero = cpu.a == 0
            cpu.negative = cpu.a >> 7 == 1
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0xF9:
            baseAddr = (memory.fetch(cpu.pc+1) << 8 | memory.fetch(cpu.pc)) 
            indexAddr = memory.fetch(cpu.y)
            cpu.pc += 2
            minuend = cpu.a
            subtrahend = memory.fetch(baseAddr + indexAddr)
            # One's complement
            subtrahend = abs(~subtrahend-1 ^ 0xFF)
            cpu.a = minuend + subtrahend + cpu.carry
            if cpu.a < 0:
                cpu.a = ~cpu.a ^ 0xFF & 0xFF
            else:
                cpu.a = cpu.a & 0xFF
            cpu.carry = cpu.a >> 7 == 0
            cpu.overflow = minuend >> 7 == subtrahend >> 7 and minuend >> 7 != cpu.a >> 7
            cpu.zero = cpu.a == 0
            cpu.negative = cpu.a >> 7 == 1
            # Page boundary crossed
            if (baseAddr + indexAddr >> 8) != (baseAddr >> 8):
                cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
        elif opcode == 0xF9D:
            baseAddr = (memory.fetch(cpu.pc+1) << 8 | memory.fetch(cpu.pc))
            indexAddr = memory.fetch(cpu.x)
            cpu.pc += 2
            minuend = cpu.a
            subtrahend = memory.fetch(baseAddr + indexAddr)
            # One's complement
            subtrahend = abs(~subtrahend-1 ^ 0xFF)
            cpu.a = minuend + subtrahend + cpu.carry
            if cpu.a < 0:
                cpu.a = ~cpu.a ^ 0xFF & 0xFF
            else:
                cpu.a = cpu.a & 0xFF
            cpu.carry = cpu.a >> 7 == 0
            cpu.overflow = minuend >> 7 == subtrahend >> 7 and minuend >> 7 != cpu.a >> 7
            cpu.zero = cpu.a == 0
            cpu.negative = cpu.a >> 7 == 1
            # Page boundary crossed
            if (baseAddr + indexAddr >> 8) != (baseAddr >> 8):
                cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()
            cpu.inc_cycle()

class CMP(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0xC1, AddressingMode.INDIRECT_X, 6,),
                      (0xC5, AddressingMode.ZERO_PAGE, 3,),
                      (0xC9, AddressingMode.IMMEDIATE, 2,),
                      (0xCD, AddressingMode.ABSOLUTE, 4,),
                      (0xD1, AddressingMode.INDIRECT_Y, 5,),
                      (0xD5, AddressingMode.ZERO_PAGE_X, 4,),
                      (0xD9, AddressingMode.ABSOLUTE_Y, 4,),
                      (0xDD, AddressingMode.ABSOLUTE_X, 4,)]
        return map(cls.create_dict_entry, variations)


class CPX(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0xE0, AddressingMode.IMMEDIATE, 2,),
                      (0xE4, AddressingMode.ZERO_PAGE, 3,),
                      (0xEC, AddressingMode.ABSOLUTE, 4,)]
        return map(cls.create_dict_entry, variations)


class CPY(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0xC0, AddressingMode.IMMEDIATE, 2,),
                      (0xC4, AddressingMode.ZERO_PAGE, 3,),
                      (0xCC, AddressingMode.ABSOLUTE, 4,)]
        return map(cls.create_dict_entry, variations)


class DEC(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0xC6, AddressingMode.ZERO_PAGE, 5,),
                      (0xCE, AddressingMode.ABSOLUTE, 6,),
                      (0xD6, AddressingMode.ZERO_PAGE_X, 6,),
                      (0xDE, AddressingMode.ABSOLUTE_X, 7,)]
        return map(cls.create_dict_entry, variations)


class DEX(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0xCA, None, 2,)]
        return map(cls.create_dict_entry, variations)


class DEY(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0x88, None, 2,)]
        return map(cls.create_dict_entry, variations)


class INC(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0xE6, AddressingMode.ZERO_PAGE, 5,),
                      (0xEE, AddressingMode.ABSOLUTE, 6,),
                      (0xF6, AddressingMode.ZERO_PAGE_X, 6,),
                      (0xFE, AddressingMode.ABSOLUTE_X, 7,)]
        return map(cls.create_dict_entry, variations)


class INX(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0xE8, None, 2,)]
        return map(cls.create_dict_entry, variations)


class INY(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0xC8, None, 2,)]
        return map(cls.create_dict_entry, variations)


class ASL(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0x06, AddressingMode.ZERO_PAGE, 5,),
                      (0x0A, AddressingMode.ACCUMULATOR, 2,),
                      (0x0E, AddressingMode.ABSOLUTE, 6,),
                      (0x16, AddressingMode.ZERO_PAGE_X, 6,),
                      (0x1E, AddressingMode.ABSOLUTE_X, 7,)]
        return map(cls.create_dict_entry, variations)


class ROL(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0x26, AddressingMode.ZERO_PAGE, 5,),
                      (0x2A, AddressingMode.ACCUMULATOR, 2,),
                      (0x2E, AddressingMode.ABSOLUTE, 6,),
                      (0x36, AddressingMode.ZERO_PAGE_X, 6,),
                      (0x3E, AddressingMode.ABSOLUTE_X, 7,)]
        return map(cls.create_dict_entry, variations)


class LSR(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0x46, AddressingMode.ZERO_PAGE, 5,),
                      (0x4A, AddressingMode.ACCUMULATOR, 2,),
                      (0x4E, AddressingMode.ABSOLUTE, 6,),
                      (0x56, AddressingMode.ZERO_PAGE_X, 6,),
                      (0x5E, AddressingMode.ABSOLUTE_X, 7,)]
        return map(cls.create_dict_entry, variations)


class ROR(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0x66, AddressingMode.ZERO_PAGE, 5,),
                      (0x6A, AddressingMode.ACCUMULATOR, 2,),
                      (0x6E, AddressingMode.ABSOLUTE, 6,),
                      (0x76, AddressingMode.ZERO_PAGE_X, 6,),
                      (0x7E, AddressingMode.ABSOLUTE_X, 7,)]
        return map(cls.create_dict_entry, variations)


class ArithmeticAndLogicalOpCodes:
    opcodes = [
        ORA,
        AND,
        EOR,
        ADC,
        SBC,
        CMP,
        CPX,
        CPY,
        DEC,
        DEX,
        DEY,
        INC,
        INX,
        INY,
        ASL,
        ROL,
        LSR,
        ROR
    ]

    @staticmethod
    def all_commands():
        return flatten(
            map(lambda x: list(x.create_variations()), ArithmeticAndLogicalOpCodes.opcodes)
        )