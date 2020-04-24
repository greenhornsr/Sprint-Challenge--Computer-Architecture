"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        ## Step 1: Add the constructor to `cpu.py`
        # Add list properties to the `CPU` class to hold 256 bytes of memory and 8 general-purpose registers.
        self.reg = [0] * 8  # 8 bytes that will each have an 8 bit value.  00000000 for a max of 8 registers
        self.ram = [0] * 256 # since each 0 in self.reg is a bit and each self.reg contains eight 0, that is equal to 1 byte.  so the ram should only be permitted a max of 256 bytes by doing self.reg * 256??? 
        # Internal Registers
        self.pc = 0  ##* Program Counter, address of the currently executing instruction.  what do i initialize this to? 
        self.ir = self.ram[self.pc]  ##* Instruction Register, contains a copy of the currently executing instruction
        
        # line tracker for the executing program within examples directory
        self.address = 0

        self.FL = 0b00000000

        # Stack Pointer
        self.sp = 7  # Used to refer to Register 7
        # Starting ram index per spec, 244
        self.sp_mem_index = 0xF4
        # Register 7        assigned to STARTING memory[index] 244(0xF4) for STACK processes PUSH/POP
        self.reg[self.sp] = self.ram[self.sp_mem_index]

        # Dispatch Table - Beautifying RUN  # likely a better way to dynamically do this.
        # K:V is machine_code: handle_method
        self.dispatchtable = {
            0b10000010 : self.handle_LDI,
            0b01000101 : self.handle_PUSH,
            0b01000110 : self.handle_POP,
            0b01010000 : self.handle_CALL,
            0b00010001 : self.handle_RET,
            0b01000111 : self.handle_PRN,
            0b10100000 : self.handle_ADD,
            0b10100010 : self.handle_MUL,
            0b00000001 : self.handle_HLT,
            0b10100111 : self.handle_CMP,
            0b01010100 : self.handle_JMP,
            0b01010101 : self.handle_JEQ,
            0b01010110 : self.handle_JNE
        }

    # MAR is Memory Address Register; holds the memory address we're reading or writing.
    # MDR is Memory Data Register, holds the value to write or the value just read. 

    # ram_read()
    def ram_read(self, MAR):
        return self.ram[MAR]
    
    # ram_write()
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, program_file):
        """Load a program into memory."""
        with open(program_file) as pf:
            for line in pf:
                line = line.split('#')
                line = line[0].strip()
                if line == '':
                    continue
                self.ram[self.address] = int(line, base=2)
                # print(type(int(line, base=2)))
                self.address +=1

    # The computer's ALU is responsible for processing mathematical calculations.
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            # v1 that simply assigns
            self.reg[reg_a] += self.reg[reg_b]

            # v2.  manages the bounds of the result to maintain the result under 8 bits (i.e. 00000000)
            # self.reg[reg_a] = (self.reg[reg_a] + self.reg[reg_b]) & 0xFF

        elif op == "MUL": 
            # print(f"multiplying {self.reg[reg_a]} x {self.reg[reg_b]} which equals {self.reg[reg_a] * self.reg[reg_b]}")
            self.reg[reg_a] *= self.reg[reg_b]
            # self.reg[reg_a] = (self.reg[reg_a] * self.reg[reg_b]) & 0xFF
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # ************** Beauty OP Functions **************
    # LDI 82/130 (hex/dec)
    def handle_LDI(self, increment, opa, opb):
        self.reg[opa] = opb   
        self.pc += increment

    # PUSH 45 (hex)
    def handle_PUSH(self, increment, opa):
        self.sp_mem_index -= 1
        self.ram[self.sp_mem_index] = self.reg[opa]  

        self.pc += increment

    # POP 46 (hex)
    def handle_POP(self, increment, opa):
        self.reg[opa] = self.ram[self.sp_mem_index]
        
        self.sp_mem_index += 1
        self.pc += increment

    # CALL 50 (hex)
    def handle_CALL(self, increment, opa):
        next_instruct = (self.pc + increment)

        # decrement memory stack location, add next instruct to stack
        self.sp_mem_index -= 1
        self.ram[self.sp_mem_index] = next_instruct
        # reassign self.pc to value in given register 
        # print(f"reg[opa]: {self.reg[opa]}")
        self.pc = self.reg[opa]

    # RET 11 (hex)
    def handle_RET(self):
        # pop return address from top of stack
        ret_address = self.ram[self.sp_mem_index]
        self.sp_mem_index +=1

        self.pc = ret_address

    # PRN 47 (hex)
    def handle_PRN(self, increment, opa):
        # print(f"Register[{opa}]!!!: ", hex(self.reg[opa]).lstrip("0x"))
        print(f"Register[{opa}]: {self.reg[opa]}\n")
        self.pc += increment

    # MUL A2 (hex)
    def handle_MUL(self, increment, opa, opb):
        self.alu("MUL", opa, opb)
        self.pc += increment

    # ADD A0 (hex)
    def handle_ADD(self, increment, opa, opb):
        self.alu("ADD", opa, opb)
        self.pc += increment

    # HLT 01 (hex)
    def handle_HLT(self):
        sys.exit("EXITING!")

    # CMP A7 (hex)  # MC = 0b00000LGE
    def handle_CMP(self, increment, opa, opb):
        # 0b00000100 Register A Less Than Register B
        rega = self.reg[opa]
        regb = self.reg[opb]
        result = ""
        if rega < regb:
            result = f"Register A: {opa} is LESS than Register B: {opb}! "
            self.FL = 0b00000100
        # 0b00000100 Register A Greater Than Register B
        elif rega > regb:
            result = f"Register A: {opa} is GREATER than Register B: {opb}!"
            self.FL = 0b00000010
        elif (rega ^ regb) == 0:
            result = f"Register A: {opa} is EQUAL to Register B: {opb}!"
            self.FL = 0b00000001
        self.pc += increment
        # print(result)
        
    # JMP 54(hex) 
    def handle_JMP(self, increment, opa):
        # print(f"{opa}, {self.reg[opa]}")
        # print("address: ", self.address)
        self.address = self.reg[opa]
        # print("address: ", self.address)
        # print("PC: ", self.pc)
        self.pc = self.address
        # print("PC: ", self.pc)
    
    # JEQ 55(hex)
    def handle_JEQ(self, increment, opa):
        even_flag = ((self.FL ^ 0b00000001))
        # print(f"even FL?: {even_flag}")
        # test = format(self.FL,'#010b')
        # print(f"JEQ - self.FL: {test}")
        if even_flag == 0:
            self.handle_JMP(increment, opa)
        else:
            self.pc += increment
    
    # JNE 56(hex)
    def handle_JNE(self, increment, opa):
        even_flag = ((self.FL ^ 0b00000001))
        # test = format(self.FL,'#010b')
        # print(f"JNE - self.FL: {test}")
        if even_flag != 0:
            self.handle_JMP(increment, opa)
        else:
            self.pc += increment




    # ************** END Beauty Functions **************

    def run(self):
        """Run the CPU."""

        while True: 
            # self.trace()
            self.ir = self.ram_read(self.pc)  # address 0
            operand_a = self.ram_read(self.pc +1)  # address 1   # R0
            operand_b = self.ram_read(self.pc +2)  # address 2   # 8
            ## Track the instruction length to increment self.pc dynamically.
            # 1. `AND` the Instruction against binary isolator
                #   Binary Isolator uses a 1 in the location of what you want to keep 
                    # i.e. if instruction or self.ir in this case is 01000111, the 01 at the beginning of the binary value tells us how many arguments and operand values follow in the instruction file(see .ls8 file). So we would use 11000000 then do (01000111 & 11000000) to get the result 0f 01000000 then do step 2
            # 2. `>>` Right Shift the result of the `&` operation.
            # 3. Increment 1 to move to the NEXT instruction
            len_instruct = ((self.ir & 11000000) >> 6) + 1
            

            # Branchtable/Dispatchtable example version...?  Not working as expected.
            if len_instruct == 3:
                self.dispatchtable[self.ir](len_instruct, operand_a, operand_b)
            elif len_instruct == 2:
                self.dispatchtable[self.ir](len_instruct, operand_a) 
            elif len_instruct == 1: 
                self.dispatchtable[self.ir]()
            else: 
                print("Unknown Instruction")




