# Opening the CSV file and reading the rows and columns
import csv
import sys

# Criamos listas com os STRs do csv escolhido e uma lista de 
# pessoas (sendo cada uma um dicionário)

STR = []
people = []
if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py FILENAME")

with open(sys.argv[1], "r") as file:
    reader = csv.DictReader(file)
    # Primeiro: transformar os valores de str p int
    for row in reader:
        person = row
        for data in person:
            # Item é o nome da chave do dicionário
            if data != 'name':
                if data not in STR:  # Assim evitamos uma lista repetida
                    STR.append(data)
                person[data] = int(person[data])
                people.append(person)

ocurrences = {}
count = 0
maxcount = 0
j = 0

# Count armazena temporariamente o valor das repetições.
# consideraremos apenas maxcount no dicionário

for n in range(len(STR)):
    ocurrences[STR[n]] = 0

# Vamos criar uma lista com os maxcounts
dna = (open(sys.argv[2], "r")).read()
maxcount = 0
for n in range(len(STR)):
    # Zeramos maxcount p cada STR
    maxcount = 0
    cSTR = STR[n]
    for i in range(len(dna)):
        count = 0
        # Checamos quando começa uma repetição
        if dna[i:(i + len(cSTR))] == cSTR:
            cursor = 0
            while dna[i + cursor:(i + cursor + len(cSTR))] == cSTR:
                count += 1
                cursor = cursor + len(cSTR)
                if count > maxcount:
                    maxcount = count
                    ocurrences[cSTR] = maxcount

# Se temos todos os itens iguals, i.e len(STR), temos a correspondência
name = 'No match' # Caso nenhum nome seja encontrado, esse é o default
for person in people:
    count = 0
    # Checa a correspondência com cada pessoa
    for data in person:  # Pula a parte dos nomes
        if data != 'name':
            if person[data] == ocurrences[data]:
                count += 1
            if count == len(STR):
                name = person['name']
print(name)
