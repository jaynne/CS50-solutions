#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
char ALPHABET[26] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};

int compute_score(string word);
int sum;
//int i;
int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner
    if (score1 == score2)
    {
        printf("Tie!");
    }
    else if (score1 > score2)
    {
        printf("Player 1 wins!");
    }
    else 
    {
        printf("Player 2 wins!");
    }
}

int compute_score(string word)
{
    // TODO: Compute and return score for string
    // ASSIGN EACH LETTER OF ALPHABET TO A POINTS VALUE -->
    sum = 0;
    
    for (int i = 0; i < strlen(word); i++)
    {
        //PRIMEIRO CONVERTE PARA LOWERCASE
        if (isupper(word[i]))
        {
            word[i] = tolower(word[i]);
        }
        
        //CHECA PARA CADA LETRA DO ALFABETO ATÉ ENCONTRAR A LETRA CORRESPONDENTE
        for (int n = 0; n < 26; n++)
        {
            //CASO A LETRA FOR CORRESPONDENTE, ATRIBUI O VALOR DA PONTUAÇÃO
            if (word[i] == ALPHABET[n])
            {
                //printf(" letter %c = %i\n", (char) word[i], POINTS[n]);
                sum += POINTS[n];
            }
            //CASO A LETRA NÃO SEJA CORRESPONDENTE, CONTINUA O LOOP ATÉ ENCONTRAR
            // PS: ISSO TAMBÉM AJUDA A NÃO ATRIBUIR PONTOS A CARACTERES DIFERENTES DE LETRAS
        }
    }
    //printf("%i\n", sum);
    return sum;
    
}
