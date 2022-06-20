// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include "dictionary.h"

//#define size_buff 1000

int dictionary_size;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in the hash table 
const unsigned int N = 26;


// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    //This node indicates in which position we are in this linked list

    int key = hash(word);
    node *cursor = table[key];

    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    // They key value will be the modulo of sum of ASCII values by N
    long sum = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        //Using lowercase because every word in dictionary is lowercase
        sum += tolower(word[i]);
    }
    // We use the modulo so that the value of the hash key is not greater than N
    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *dictionary_file = fopen(dictionary, "r");
    if (dictionary_file == NULL)
    {
        printf("Could not open dictionary\n");
        return false;
    }

    char buff[LENGTH + 1];

    while (fscanf(dictionary_file, "%s", buff) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            printf("Could not allocate memory\n");
            return false;
        }

        //Copy the content of word buffer into the "word" part of the node

        //buff will correspond to the next word in the linked list

        strcpy(n->word, buff);
        int key = hash(buff);

        n->next = table[key];
        table[key] = n;

        //For each loop, we count one more word to the dictionary size

        dictionary_size++;
    }

    fclose(dictionary_file);
    return true;
    
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return dictionary_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    /*Cursor and temp are just pointers used to point to the current node.
    Without using them, we would lose track of the linked list
    */

    //There are 26 linked lists (one for each bucket of the table). We are 
    //going to search each one completely 

    for (int i = 0; i < N; i++)
    {
        //We have to use a while here to verify each entire linked list
        //tmp is the node before cursor
        node *cursor = table[i];
        node *temp = table[i];
        
        while (cursor != NULL)
        {
            temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
        
    }
    return true;

}

