# per Beej Jorgensen - Lambda CS Instructor
# Why does bitwise NOT (~) give me negative numbers in Python?
"""
Why does bitwise NOT (~) produce negative numbers?

It has to do with how negative numbers are represented in memory. It's done
with something called _2's Complement_.

For this week, we've been assuming all numbers are unsigned, i.e. only
positive.

Which means that an 8 bit 255 is 0b11111111. And 0 is 0b00000000.

But there's no room there for negatives.

So 2's complement was created. It uses the same bit patterns for positive
numbers, but reserves others for negatives.

Notably, any number with a 1 bit for the high (left) bit is a negative number.

The output of this program is:

    Signed:

      8 0b00001000
      7 0b00000111
      6 0b00000110
      5 0b00000101
      4 0b00000100
      3 0b00000011
      2 0b00000010
      1 0b00000001
      0 0b00000000
     -1 0b11111111
     -2 0b11111110
     -3 0b11111101
     -4 0b11111100
     -5 0b11111011
     -6 0b11111010
     -7 0b11111001
     -8 0b11111000

    Unsigned:

      8 0b00001000
      7 0b00000111
      6 0b00000110
      5 0b00000101
      4 0b00000100
      3 0b00000011
      2 0b00000010
      1 0b00000001
      0 0b00000000
    255 0b11111111
    254 0b11111110
    253 0b11111101
    252 0b11111100
    251 0b11111011
    250 0b11111010
    249 0b11111001
    248 0b11111000

Notice how the bit pattern for 255 is exactly the same as the bit pattern for
-1!

So the NOT is working... it's taking 0b00000000 and turning it into 0b11111111.
And that _would_ be 255 unsigned.

However, Python prints things out as _signed_ by default, so your 0b11111111
becomes -1.

You can override this behavior by bitwise ANDing the number with a mask to
force it positive, like the bin8() function does, below.

"""

def bin8(v):
    #             AND with 0b11111111
    #                vvv
    return f'0b{v & 0xff:08b}'
    #                    ^^^
    #     Print binary with field width 8 and pad with leading zeros

print("Signed:\n")

for i in range(8, -9, -1):
    print(f'{i:3} {bin8(i)}')

print("\nUnsigned:\n")

for i in range(8, -1, -1):
    print(f'{i:3} {bin8(i)}')
for i in range(255, 247, -1):
    print(f'{i:3} {bin8(i)}')