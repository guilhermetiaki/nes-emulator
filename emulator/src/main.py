import argparse

from emulator.cartridge import Cartridge
from emulator.cpu import CPU, CPUState, StatusRegisterFlags
from emulator.memory import Memory
from emulator.opcodes.jump import BRK
from emulator.opcodes.opcodes import OpCodes


def main(args):
    emulate(args.file)


# https://stackoverflow.com/questions/45305891/6502-cycle-timing-per-instruction
# http://nesdev.com/6502_cpu.txt (6510 Instruction Timing)
def emulate(file_path):
    nestest_log_format = args.nestest
    running = True
    file_contents = read_file(file_path)
    cartridge = Cartridge.from_bytes(file_contents)
    memory = Memory(cartridge.prg_rom)
    cpu = CPU(log_compatible_mode=nestest_log_format)

    if nestest_log_format:
        # hack for Nintendulator nestest log comparison
        cpu.sp -= 2

    while running:
        try:
            previous_state = CPUState(pc=cpu.pc, sp=cpu.sp, a=cpu.a, x=cpu.x, y=cpu.y, p=StatusRegisterFlags(int_value=cpu.flags), addr=cpu.addr, data=cpu.data,
                                      cycle=cpu.cycle, log_compatible_mode=nestest_log_format)
            decoded = cpu.exec_in_cycle(fetch_and_decode_instruction, cpu, memory)  # fetching and decoding a instruction always take 1 cycle
            if decoded:
                decoded.exec(cpu, memory)
                # TODO: proper execution abortion, this is probably wrong
                if isinstance(decoded, BRK):
                    running = False
                    break
                print_debug_line(cpu, previous_state, decoded, nestest_log_format)
                cpu.clear_state_mem()
        except IndexError as e:
            # we've reached a program counter that is not within memory bounds
            print(e)
            running = False
        except KeyError as e:
            # print("Can't find instruction by code {}".format(e))
            cpu.inc_pc_by(1)
        except Exception as e:
            print(e)
            cpu.inc_pc_by(1)


def fetch_and_decode_instruction(cpu, memory):
    instruction = memory.fetch(cpu.pc)
    decoded = decode_instruction(instruction)
    cpu.inc_pc_by(1)
    return decoded


def read_file(file_path):
    with open(file_path, mode='rb') as file:
        return file.read()


def decode_instruction(instruction):
    decoded = OpCodes.all[instruction]
    if not decoded:
        print("Can't find instruction 0x{:02X}".format(instruction))
    return decoded


def print_debug_line(cpu, previous, instruction, nestest):
    if nestest:
        print("%04X  %s  %s  CYC:%s" % (previous.pc, instruction, previous, previous.cycle + 7))
    else:
        print(cpu)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("file", help="NES Cartridge file path")
    parser.add_argument("--nestest", action="store_true")

    args = parser.parse_args()
    main(args)
