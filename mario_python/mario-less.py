from cs50 import get_int
#height = int(input('Height: ')) #with this built-in function we don't have how to reject alpha inputs
height = get_int('Height: ')
while (height < 1 or height > 8):
    height = int(input('Height: '))
spaces = height
line = '#'
for i in range (1, height + 1):
    for s in range (spaces):
        print(" ", end='')
    for j in range(i):
        print("#", end='')
        #line = str(line + '#')
        #print((line).rstrip)
    print("")
    spaces = spaces - 1