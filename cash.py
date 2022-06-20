from cs50 import get_float
change = get_float('Change owed: ')
while(change < 0):
    change = get_float('Change owed: ')
change = round(change * 100)
coins = 0
#Coins: 25, 10, 5, 1
while(change >= 25):
    change = change - 25
    coins = coins + 1
while(change >= 10):
    change = change - 10
    coins = coins + 1
while(change >= 5):
    change = change - 5
    coins = coins + 1
while(change >= 1):
    change = change - 1
    coins = coins + 1

print(f"{coins}")