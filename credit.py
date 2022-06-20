from cs50 import get_int

i = 0
count = 0
digit = 0
uneven = 0
even = 0
sum_uneven = 0
sum_even = 0
digit2 = 0
card2 = 0
x = 0
# Ps: a bandeira só será verificada caso o cartão seja válido

card = get_int("Number: ")
if (card < 0):
    card = get_int("Number: ")
n = card
card2 = card
while n > 1:
    n = n // 10
    i = i + 1
count = i

if (count == 15 or count == 13):
    # Caso o número de dígitos seja ímpar
    while count > 0:
        digit = card % 10
        card = (card - digit)//10
        if (count % 2 != 0):
            uneven = digit
            sum_uneven = sum_uneven + uneven
        else:
            even = digit
            even = (digit * 2)
            if even >= 10:
                even = (1 + even % 10)
            sum_even = sum_even + even
        count = count - 1
elif count == 16:
    # Caso o número de dígitos seja par
    while count > 0:
        digit = card % 10
        card = (card - digit)//10
        if (count % 2 != 0):
            even = (digit * 2)
            if even >= 10:
                even = (1 + even % 10)
            sum_even = sum_even + even
        else:
            uneven = digit
            sum_uneven = sum_uneven + uneven
        count = count - 1
else:
    print("INVALID")

total_sum = sum_uneven + sum_even
if (total_sum % 10 == 0):
    while (x < (i - 2)):
        digit2 = card2 % 10
        card2 = (card2 - digit2)//10
        x = x + 1

    second_last = card2 % 10
    last = (card2 - second_last) // 10 % 10
    if ((last == 3 and second_last == 4) or (last == 3 and second_last == 7)):
        print("AMEX")
    elif (last == 4):
        print("VISA")
    elif (last == 5 and second_last >= 1 and second_last <= 5):
        print("MASTERCARD")
    else:
        print("INVALID")
else:
    print("INVALID")
