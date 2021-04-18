from binaryninja.architecture import Architecture
from binaryninja.architecture import Architecture
from binaryninja.function import RegisterInfo, InstructionInfo, InstructionTextToken
from binaryninja.enums import InstructionTextTokenType, BranchType

class Kata(Architecture):
    name = 'Kata'
    address_size = 4
    default_int_size = 4
    instr_alignment = 1
    max_instr_length = 15
    regs = {
        'r0': RegisterInfo("r0", 4),
        'r1': RegisterInfo("r1", 4),
        'r2': RegisterInfo("r2", 4),
        'r3': RegisterInfo("r3", 4),
        'fail': RegisterInfo("fail", 1)
    }

    def get_instruction_info(self, data, addr):
        result = InstructionInfo()
        opcode = data[0]
        if opcode == 0x00:
            result.length = 1
            result.add_branch(BranchType.FunctionReturn)
            return result

        byte1 = data[1]
        if opcode == 0xf6:
            if byte1 & 3 == 0:
                result.length = 5
            elif byte1 & 3 == 2:
                result.length = 6
        elif opcode == 0xaa:
            if byte1 & 3 == 0:
                result.length = 3
            elif byte1 & 3 == 2:
                result.length = 8
        elif opcode == 0xef:
            if byte1 & 3 == 2:
                result.length = 3
            elif byte1 & 3 == 3:
                result.length = 5
            elif byte1 & 3 == 1:
                result.length = 4
            else:
                result.length = 9
        elif opcode == 0x4a:
            if byte1 & 3 == 0:
                result.length = 2
            elif byte1 & 3 == 2:
                result.length = 7
        elif opcode == 0x8b:
            if byte1 & 3 == 0:
                result.length = 3
            elif byte1 & 3 == 2:
                result.length = 6
        elif opcode == 0x5d:
            if byte1 & 3 == 0:
                result.length = 3
            elif byte1 & 3 == 2:
                result.length = 8
        elif opcode == 0x7c:
            if byte1 & 3 == 0:
                result.length = 4
            elif byte1 & 3 == 2:
                result.length = 7  
        elif opcode == 0xb1:
            if byte1 & 3 == 0:
                result.length = 3
            elif byte1 & 3 == 2:
                result.length = 6
        elif opcode == 0xd5:
            if byte1 & 3 == 2:
                result.length = 5
            elif byte1 & 3 == 3:
                result.length = 9
            elif byte1 & 3 == 1:
                result.length = 3
            else:
                result.length = 4
        elif opcode == 0x1e:
            if byte1 & 3 == 2:
                result.length = 9
            elif byte1 & 3 == 3:
                result.length = 0xa
            elif byte1 & 3 == 1:
                result.length = 8
            else:
                result.length = 3
        elif opcode == 0xc3:
            if byte1 & 3 == 0:
                result.length = 4
            elif byte1 & 3 == 2:
                result.length = 7

        return result

    def get_instruction_text(self, data, addr):
        instrLen = 0
        tokens = []
        opcode = data[0]
        if opcode == 0x00:
            instrLen = 1
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'ret'))
            return tokens, instrLen

        byte1 = data[1]
        if opcode == 0xf6:
            if byte1 & 3 == 0:
                instrLen = 5
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'mov'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                reg1 = (byte1 >> 6) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg1))
            elif byte1 & 3 == 2:
                instrLen = 6
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'mov'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                int0 = int.from_bytes(data[2:6], byteorder='little')
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, '0x%x' % int0, int0))

        elif opcode == 0xaa:
            if byte1 & 3 == 0:
                instrLen = 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'sub'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                reg1 = (byte1 >> 6) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg1))
            elif byte1 & 3 == 2:
                instrLen = 8
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'sub'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                int0 = int.from_bytes(data[2:6], byteorder='little')
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, '0x%x' % int0, int(int0)))

        elif opcode == 0xef:
            if byte1 & 3 == 2:
                instrLen = 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'write'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '('))
                reg0 = (byte1 >> 4) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                byte2 = data[2]
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '\'%s\'' % chr(byte2)))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ')'))
            elif byte1 & 3 == 3:
                instrLen = 5
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'write'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '('))
                byte3 = data[3]
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, '0x%x' % byte3, int(byte3)))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                byte2 = data[2]
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '\'%s\'' % chr(byte2)))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ')'))
            elif byte1 & 3 == 1:
                instrLen = 4
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'write'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '('))
                byte2 = data[2]
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, '0x%x' % byte2, int(byte2)))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 6) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '.b'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ')'))
            else:
                instrLen = 9
                reg0 = (byte1 >> 4) & 3
                reg1 = (byte1 >> 6) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'write'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '('))
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))

                byte2 = data[2]
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, '0x%x' % byte2, int(byte2)))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))

                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg1))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '.b'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ')'))

        elif opcode == 0x4a:
            if byte1 & 3 == 0:
                instrLen = 2
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'add'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                reg1 = (byte1 >> 6) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg1))
            elif byte1 & 3 == 2:
                instrLen = 7
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'add'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                int0 = int.from_bytes(data[2:6], byteorder='little')
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, '0x%x' % int0, int0))

        elif opcode == 0x8b:
            if byte1 & 3 == 0:
                instrLen = 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'xor'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                reg1 = (byte1 >> 6) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg1))
            elif byte1 & 3 == 2:
                instrLen = 6
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'xor'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                int0 = int.from_bytes(data[2:6], byteorder='little')
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, '0x%x' % int0, int0))

        elif opcode == 0x5d:
            if byte1 & 3 == 0:
                instrLen = 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'read'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '('))
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, '0x0', 0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '&'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg1 = (byte1 >> 6) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg1))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ')'))
            elif byte1 & 3 == 2:
                instrLen = 8
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'read'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '('))
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, '0x0', 0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '&'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                int0 = int.from_bytes(data[2:6], byteorder='little')
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, '0x%x' % int0, int0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ')'))

        elif opcode == 0x7c:
            if byte1 & 3 == 0:
                instrLen = 4
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'shl'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                reg1 = (byte1 >> 6) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg1))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '.b'))
            elif byte1 & 3 == 2:
                instrLen = 7
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'shl'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                int0 = int.from_bytes(data[2:3], byteorder='little')
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, '0x%x' % int0, int0))

        elif opcode == 0xb1:
            if byte1 & 3 == 0:
                instrLen = 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'shr'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                reg1 = (byte1 >> 6) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg1))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '.b'))
            elif byte1 & 3 == 2:
                instrLen = 6
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'shr'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                int0 = int.from_bytes(data[2:3], byteorder='little')
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, '0x%x' % int0, int0))

        elif opcode == 0xd5:
            if byte1 & 3 == 2:
                instrLen = 5
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'rol'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                int0 = int.from_bytes(data[2:6], byteorder='little')
                int0 = ((~int0) & 7) + 1
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, '0x%x' % int0, int0))
            elif byte1 & 3 == 3:
                instrLen = 9
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'ror'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                int0 = int.from_bytes(data[2:6], byteorder='little')
                int0 = ((~int0) & 7) + 1
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, '0x%x' % int0, int0))
            elif byte1 & 3 == 1:
                instrLen = 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'memcpy 3'))
            else:
                instrLen = 4
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'memcpy 4'))

        elif opcode == 0x1e:
            if byte1 & 3 == 2:
                instrLen = 9
            elif byte1 & 3 == 3:
                instrLen = 10
            elif byte1 & 3 == 1:
                instrLen = 8
            else:
                instrLen = 3

            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'swap registers'))

        elif opcode == 0xc3:
            if byte1 & 3 == 0:
                instrLen = 4
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'cmp'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                reg1 = (byte1 >> 6) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg1))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'fail'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '= 0x1'))

            elif byte1 & 3 == 2:
                instrLen = 7
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, 'cmp'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                reg0 = (byte1 >> 4) & 3
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'r%d' % reg0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                int0 = int.from_bytes(data[2:6], byteorder='little')
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, '0x%x' % int0, int0))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ','))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, 'fail'))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, '= 0x1'))

        return tokens, instrLen
         
    def get_instruction_low_level_il(self, data, addr, il):
        return None

Kata.register()
