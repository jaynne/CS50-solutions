from cs50 import get_string
text = get_string("Text: ")

# Criaremos uma lista com cada palavra e então calcularemos a extensão de cada uma dessas palavras

wordList = text.split()
wlist = []

for word in wordList:
    if ',' in word:
        word = word.replace(",", "")
        wlist.append(word)
    elif '.' in word:
        word = word.replace(".", "")
        wlist.append(word)
    elif '!' in word:
        word = word.replace("!", "")
        wlist.append(word)
    elif '?' in word:
        word = word.replace("?", "")
        wlist.append(word)
    elif '\'' in word:
        word = word.replace("\'", "")
        wlist.append(word)
    else:
        wlist.append(word)

w_length = [len(x) for x in wlist]
sum_letters = sum(w_length)

sentences = 0

# Podemos dividir o número de palavras pelo número de sentenças e dividir por 100

for c in text:
    if (c == '!' or c == '.' or c == '?'):
        sentences = sentences + 1

L = (sum_letters / len(wlist)) * 100
S = (sentences / len(wlist)) * 100

index = round(0.0588 * L - 0.296 * S - 15.8)

if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
#print(f"{index}")