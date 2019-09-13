from more_itertools import flatten

from constants import AddressingMode
from opcodes.base import OpCode


class BIT(OpCode):
    """
    A & M, N = M7, V = M6
    This instruction is used to test if one or more bits are set in a target memory location.
    The mask pattern in A is ANDed with the value in memory to set or clear the zero flag, but the result is not kept.
    Bits 7 and 6 of the value from memory are copied into the N and V flags.
    """

    @classmethod
    def create_variations(cls):
        variations = [(0x24, AddressingMode.ZERO_PAGE, 3,),
                      (0x2C, AddressingMode.ABSOLUTE, 4,)]
        return map(lambda x: tuple((x[0], cls(*x))), variations)


class CLC(OpCode):
    """
    C = 0
    Set the carry flag to zero.
    """

    @classmethod
    def create_variations(cls):
        variations = [(0x18, None, 2,)]
        return map(lambda x: tuple((x[0], cls(*x))), variations)

    @classmethod
    def exec(cls, cpu_state, memory):
        cpu_state.p.carry = False


class SEC(OpCode):
    """
    C = 1
    Set the carry flag to one.
    """

    @classmethod
    def create_variations(cls):
        variations = [(0x38, None, 2,)]
        return map(lambda x: tuple((x[0], cls(*x))), variations)

    @classmethod
    def exec(cls, cpu_state, memory):
        cpu_state.p.carry = True


class CLD(OpCode):
    """
    D = 0
    Sets the decimal mode flag to zero.
    """

    @classmethod
    def create_variations(cls):
        variations = [(0xD8, None, 2,)]
        return map(lambda x: tuple((x[0], cls(*x))), variations)

    @classmethod
    def exec(cls, cpu_state, memory):
        cpu_state.p.decimal = False


class SED(OpCode):
    """
    D = 1
    Set the decimal mode flag to one.
    """

    @classmethod
    def create_variations(cls):
        variations = [(0xF8, None, 2,)]
        return map(lambda x: tuple((x[0], cls(*x))), variations)

    @classmethod
    def exec(cls, cpu_state, memory):
        cpu_state.p.decimal = True


class CLI(OpCode):
    """
    I = 0
    Clears the interrupt disable flag allowing normal interrupt requests to be serviced.
    """

    @classmethod
    def create_variations(cls):
        variations = [(0x58, None, 2,)]
        return map(lambda x: tuple((x[0], cls(*x))), variations)

    @classmethod
    def exec(cls, cpu_state, memory):
        cpu_state.p.interrupts_disabled = False


class SEI(OpCode):
    """
    I = 1
    Set the interrupt disable flag to one.
    """

    @classmethod
    def create_variations(cls):
        variations = [(0x78, None, 2,)]
        return map(lambda x: tuple((x[0], cls(*x))), variations)

    @classmethod
    def exec(cls, cpu_state, memory):
        cpu_state.p.interrupts_disabled = True


class CLV(OpCode):
    """
    V = 0
    Clears the overflow flag.
    """

    @classmethod
    def create_variations(cls):
        variations = [(0xB8, None, 2,)]
        return map(lambda x: tuple((x[0], cls(*x))), variations)

    @classmethod
    def exec(cls, cpu_state, memory):
        cpu_state.p.overflow = False


class NOP(OpCode):
    @classmethod
    def create_variations(cls):
        variations = [(0xEA, None, 2)]
        return map(lambda x: tuple((x[0], cls(*x))), variations)

    @classmethod
    def exec(cls, cpu_state, memory):
        pass


class FlagOpCodes:
    opcodes = [
        BIT,
        CLC,
        SEC,
        CLD,
        SED,
        CLI,
        SEI,
        CLV,
        NOP
    ]

    @staticmethod
    def all_commands():
        return flatten(
            map(lambda x: list(x.create_variations()), FlagOpCodes.opcodes)
        )