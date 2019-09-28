from more_itertools import flatten

from emulator.adressing import Immediate, ZeroPage, Absolute, ZeroPageY, AbsoluteY, IndirectY, ZeroPageX, AbsoluteX, IndirectX
from emulator.constants import NEGATIVE_BIT, LOW_BITS_MASK
from emulator.cpu import StatusRegisterFlags
from emulator.opcodes.base import OpCode


def unofficial_opcode_str(self, name=None):
    if name == None:
        name = type(self).__name__

    def __str_addr():
        if self.addressing_mode is not None:
            if self.addressing_mode.low is not None and self.addressing_mode.high is not None:
                return "{:02X} {:02X}".format(self.addressing_mode.low, (self.addressing_mode.high >> 8))
            elif self.addressing_mode.low is not None:
                return "{:02X}".format(self.addressing_mode.low)
        return ""

    def __str_addr_2():
        if self.addressing_mode is not None:
            if self.addressing_mode.addr is not None and self.addressing_mode.data is not None:
                return "*{} {} {}".format(name, self.addressing_mode.addr, self.addressing_mode.data)
            elif self.addressing_mode.addr is not None:
                return "*{} {}".format(name, self.addressing_mode.addr)
        return "*{}".format(name)
    with_space = "{:02X} {:<6}{:<30} ".format(
        self.id, __str_addr(), __str_addr_2())
    without_space = "{:02X} {:<6}{:<30}".format(
        self.id, __str_addr(), __str_addr_2())

    if len(with_space) > 40:
        return without_space
    else:
        return with_space


class IGN(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0x0C, Absolute, 4),
                      (0x04, ZeroPage, 3,),
                      (0x44, ZeroPage, 3,),
                      (0x64, ZeroPage, 3,),
                      (0x14, ZeroPageX, 4),
                      (0x34, ZeroPageX, 4),
                      (0x54, ZeroPageX, 4),
                      (0x74, ZeroPageX, 4),
                      (0xD4, ZeroPageX, 4),
                      (0xF4, ZeroPageX, 4),
                      (0x1C, AbsoluteX, 4),
                      (0x3C, AbsoluteX, 4),
                      (0x5C, AbsoluteX, 4),
                      (0x7C, AbsoluteX, 4),
                      (0xDC, AbsoluteX, 4),
                      (0xFC, AbsoluteX, 4)]
        return map(cls.create_dict_entry, variations)

    def exec(self, cpu, memory):
        def _cycle():
            if self.addressing_mode:
                address = self.addressing_mode.fetch_address(cpu, memory)
                value = self.addressing_mode.read_from(cpu, memory, address)
                if self.addressing_mode != Immediate:
                    self.addressing_mode.data = "= %02X" % memory.fetch(
                        address)
                    cpu.addr = address
                    cpu.data = value
        _cycle()

    def __str__(self):
        return unofficial_opcode_str(self, "NOP")


class SKB(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0x80, Immediate, 2),
                      (0x82, Immediate, 2,),
                      (0x89, Immediate, 2,),
                      (0xC2, Immediate, 2,),
                      (0xE2, Immediate, 2)]
        return map(cls.create_dict_entry, variations)

    def exec(self, cpu, memory):
        _address = self.addressing_mode.fetch_address(cpu, memory)

    def __str__(self):
        return unofficial_opcode_str(self, "NOP")


class NOP(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0x1A, None, 2),
                      (0x3A, None, 2),
                      (0x5A, None, 2),
                      (0x7A, None, 2),
                      (0xDA, None, 2),
                      (0xFA, None, 2)]
        return map(cls.create_dict_entry, variations)

    def exec(self, cpu, memory):
        def _stall():
            pass

        cpu.exec_in_cycle(_stall)

    def __str__(self):
        return unofficial_opcode_str(self)


class LAX(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [
            (0xA3, IndirectX, 6),
            (0xA7, ZeroPage, 3),
            (0xAF, Absolute, 4),
            (0xB3, IndirectY, 5),
            (0xB7, ZeroPageY, 4),
            (0xBF, AbsoluteY, 4)]
        return map(cls.create_dict_entry, variations)

    def exec(self, cpu, memory):
        def _lda():
            if self.addressing_mode:
                address = self.addressing_mode.fetch_address(cpu, memory)
                value = self.addressing_mode.read_from(cpu, memory, address)
                if self.addressing_mode != Immediate:
                    self.addressing_mode.data = "= %02X" % memory.fetch(
                        address)
                    cpu.addr = address
                    cpu.data = value

                cpu.a = value
                cpu.zero = cpu.a == 0
                cpu.negative = (cpu.a & 0b10000000) > 0

        def _tax():
            cpu.x = cpu.a
            cpu.zero = cpu.x == 0
            cpu.negative = (cpu.x & 0b10000000) > 0

        _lda()
        _tax()

    def __str__(self):
        return unofficial_opcode_str(self)

# SAX (d,X) ($83 dd; 6 cycles)
# SAX d ($87 dd; 3 cycles)
# SAX a ($8F aa aa; 4 cycles)
# SAX d,Y ($97 dd; 4 cycles)
class SAX(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0x83, IndirectX, 6),
                      (0x87, ZeroPage, 3),
                      (0x8F, Absolute, 4),
                      (0x97, ZeroPageY, 4)]
        return map(cls.create_dict_entry, variations)

    def exec(self, cpu, memory):
        def _stall():
            pass

        def cycle_sta():
            if self.addressing_mode:
                address = self.addressing_mode.fetch_address(cpu, memory)
                cpu.addr = address
                cpu.data = cpu.a & cpu.x
                self.addressing_mode.data = "= %02X" % memory.fetch(address)
                self.addressing_mode.write_to(cpu, memory, address, cpu.a & cpu.x)

        cycle_sta()

    def __str__(self):
        return unofficial_opcode_str(self)

class SBC(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0xEB, Immediate, 2,)]
        return map(cls.create_dict_entry, variations)

    def exec(self, cpu, memory):
        def _cycle():
            def wrap_sub(a, b):
                return (a - b) % 0x100

            address = self.addressing_mode.fetch_address(cpu, memory)
            subtrahend = self.addressing_mode.read_from(cpu, memory, address)
            minuend = cpu.a
            if self.addressing_mode != Immediate:
                cpu.addr = address
                cpu.data = subtrahend
                self.addressing_mode.data = "= %02X" % memory.fetch(address)

            new_a = (wrap_sub(wrap_sub(minuend, subtrahend), (0 if cpu.carry else 1)))
            cpu.carry = (new_a & 0b01111111) == new_a
            cpu.overflow = ((cpu.a ^ subtrahend) & NEGATIVE_BIT > 0) and (((cpu.a ^ new_a) & LOW_BITS_MASK) & NEGATIVE_BIT > 0)
            cpu.a = new_a
            cpu.a &= 0xFF
            cpu.zero = cpu.a == 0
            cpu.negative = cpu.a >> 7 == 1

        _cycle()
        
    def __str__(self):
        return unofficial_opcode_str(self)


class UnofficialOpcodes:
    opcodes = [
        IGN,
        NOP,
        SKB,
        LAX,
        SAX,
        SBC
    ]

    @staticmethod
    def all_commands():
        return flatten(
            map(lambda x: list(x.create_variations()), UnofficialOpcodes.opcodes)
        )