# Opening the CSV file and reading the rows and columns
import csv
import sys

# Example below should return Lavender
# python dna.py databases/large.csv sequences/5.txt
# name,AGATC,TTTTTTCT,AATG,TCTAG,GATA,TATC,GAAA,TCTG
# 22,33,43,12,26,18,47,41

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
                if data not in STR:
                    STR.append(data)  # Assim evitamos uma lista repetida
                person[data] = int(person[data])
                people.append(person)

oc_list = []  # lista que contém o dicionário abaixo
ocurrences = {}
count = 0
maxcount = 0
j = 0

# Dois valores p ocorrência = STR_oc e STR_max
# STR_oc vai ser o "buffer", consideraremos apenas STR_max
# na lista final

for n in range(len(STR)):
    ocurrences[STR[n]] = 0

# Vamos criar uma lista com os maxcounts
dna = (open(sys.argv[2], "r")).read()
maxcount = 0
STRcount = []
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
                count = count + 1
                cursor = cursor + len(cSTR)
                if count > maxcount:
                    maxcount = count
                    ocurrences[cSTR] = maxcount
    STRcount.append(ocurrences[cSTR])

# Se temos todos os itens iguals, i.e len(STR), temos a correspondência

name = 'No match'
for person in people:
    count = 0
    # Checa a correspondência com cada pessoa
    for data in person:  # Pula a parte dos nomes
        if data != 'name':
            if person[data] == ocurrences[data]:
                count = count + 1
            if count == len(STR):
                name = person['name']
print(name)
