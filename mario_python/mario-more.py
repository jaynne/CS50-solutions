from cs50 import get_int
height = get_int('Height: ')
while (height < 1 or height > 8):
    height = int(input('Height: '))
spaces = height
i = 1
#height = height - 1
while(height > 0):
        spaces = height - 1
        print(" " * (spaces) + "#" * i + "  " + "#" * i)
        i = i + 1
        height = height - 1
