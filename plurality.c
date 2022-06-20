#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    /*na linha acima conta a quantidade de argumentos da string, q é o número de candidatos. 
    Exclui o primeiro argumento que é o nome do programa, logo temos argc - 1*/
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    { 
        /*Vc declra os nomes das pessoas qnd executa o programa
        aqui, atribuímos os nomes à cada elemento da string. Novamente, exceto o primeiro.*/
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i].name) == 0)
            {
                candidates[i].votes = candidates[i].votes + 1;
                return true;
            }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // TODO
    int max_votes = 0;
    //Essa int vai sendo atualizada a cada vez que rodamos o loop. Primeiro,
    //ela começa sendo menor que 0, já que é o primeiro número e ele sempre vai ser o maior
    //depois, 
    
    //n precisamos sortir (como no runoff), apenas achar o maior valor (ou os amiores valores)
    
    /* não podemos usar o voter_count porque ele não é uma 
    variável global (está contido em void), logo precisamos
    achar o número máximo nessa função*/
    for (int i = 0; i < candidate_count; i++)
    {
        //Esse if só é true caso o valor atual seja menor que o anterior. Assim, conseguimos o manter atualizado.
        if (candidates[i].votes > max_votes)
        {
            max_votes = candidates[i].votes;
        }
    }
    for (int j = 0; j < candidate_count; j++)
    {
        if (candidates[j].votes == max_votes)
        {
        printf("%s\n", candidates[j].name);
        }
    }
    return;
}

