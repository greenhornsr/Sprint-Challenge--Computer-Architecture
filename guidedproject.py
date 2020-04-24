# Write a program in Python that runs programs.

import sys

# CLI TO RUN THIS FILE - `python3 guidedproject.py <nameoftextfilewithinstructions>`.  in this sample case, `python3 guidedproject.py printbeej.txt`

# parse the command line
print(sys.argv)
program_filename = sys.argv[1]
print(program_filename)

PRINT_BEEJ = 1
HALT = 2
SAVE_REGISTER = 3 # Store a value in a register (in the LS8 called LDI)
PRINT_REGISTER = 4 # Corresponds to PRN in the LS8
PUSH = 5
POP = 6
CALL = 7
RET = 8

# STORE INSTRUCTIONS IN LIST
# memory = [
#     PRINT_BEEJ,
#     SAVE_REGISTER,  # Save R0,37     # Store 37 in R0    # this is the OP Code
#     0, #R0      # This is the ("argument")
#     37, #37     # This is the Operand
#     PRINT_BEEJ,

#     PRINT_REGISTER,  # PRINT_REGISTER R0
#     0, #R0  

#     HALT
# ]
memory = [0] * 256

register = [0] * 8 # like variables limited to R0-R7(8 total registers); aka variables at our disposal.  Is based on the computer spec.  If computer only has 8 registers, you can only make a register array with 8...

# Register[7] is our Stack Pointer (SP)
SP = 7
register[SP] = 0xF4

# load program into memory
address = 0
with open(program_filename) as f:   
    for line in f:
        line = line.split('#')
        line = line[0].strip()

        if line == '':
            continue
        # print(line, end="")
        memory[address] = int(line)

        address +=1

# sys.exit()  


pc = 0 # PROGRAM COUNTER, the address of the current instruction
running = True

while running:
    inst = memory[pc]

    if inst == PRINT_BEEJ:
        print('Beej!')
        pc += 1

    elif inst == SAVE_REGISTER:
        reg_num = memory[pc+1]
        value = memory[pc+2]
        register[reg_num] = value
        pc+=3
    
    elif inst == PRINT_REGISTER:
        reg_num = memory[pc+1]
        value = register[reg_num]
        print(value)
        pc+=2

    elif inst == PUSH:
        #decrement the Stack Pointer(SP)
        register[SP] -=1
        # copy value from register into memory
        reg_num = memory[pc+1]
        value = register[reg_num]  # this is what we want to push
        # reassign address to be the value in register 7(which is our Stack Pointer)
        address = register[SP]
        memory[address] = value

        pc+=2
    
    elif inst == CALL: 
        # Compute return address
        return_address = pc +2
        # Decrement the stack pointer, push onto the stack
        register[SP] -=1
        memory[register[SP]] = return_address

        # Set the PC to the value in the given register
        reg_num = memory[pc+1]  # equivelant to opa
        dest_address = register[reg_num]

        pc = dest_address

    elif inst == RET:
        # pop return address from top of stack
        return_address = memory[register[SP]]
        register[SP] +=1

        # set the pc
        pc = return_address

    elif inst == HALT:
        running = False

    else: 
        print(f"Unknown Instruction")
        running = False