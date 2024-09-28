#include <iostream>
#include <limits>
#include <string.h>
#include <fstream>
#include <sstream>

using namespace std;

ofstream fout("output.txt"); // Create an output file stream to write results to "output.txt"
stringstream ss; // String stream for handling string input

// Define a structure to represent a player. With this structure we can create a circular linked list to represent the circle of players.
struct Player
{
    int number;
    char name[20];
    bool elimination = false;
    Player *next=NULL;
};

Player *first=NULL;

void addPlayer(Player *pl,int number,char *name)
{
    Player *player = new Player;
    player->number=number;
    strcpy(player->name,name);
    if(first == NULL) // If list is empty, make the new player the first player
    {
      first=player;
      first->next=first; // Point to itself to make it circular
    }
     else
       {
           while(pl->next != first)
           pl=pl->next;
           pl->next=player;
           player->next=first;
       }
}

void showPlayers(Player *pl)
{
    if(first != NULL) // Check if there are players
    do
    {
        fout << "Player: "<< pl->name<< ", number: " << pl->number + 1 << endl; // Output player details to the file
        pl=pl->next;
    }while(pl != first);
}

int checkGameState(Player *pl,int players) // Function to check the game state and count eliminations
{
    int eliminations=0;
    do{
        if(pl->elimination == true)
          eliminations++;
        pl=pl->next;
    }while(pl != first);
    if(eliminations == players-1)
      return 0;
     else
      return 1;

}

void winner(Player *pl) // Function to determine and display the winner
{
    while(pl->elimination == true)
      pl=pl->next;
    fout << "Player: "<< pl->name<< ", number: " << pl->number + 1;
}

int checkInput(char s[100]) // Function to check if input is a number or a phrase
{
    int i;
    for(i=0;i<(int)strlen(s);i++)
      if(isdigit(s[i]) == 0)
        return 0;
    return 1;
}

int phraseNumbering(char s[100]) // Function to count the number of words in a string
{
    char *p;
    int n=0;
    p=strtok(s," ");
    while(p)
    {
        n++;
        p=strtok(NULL," ");
    }
    return n;
}

// Function to handle player elimination
void Elimination(Player *pl, int k, int n)
{
    int i = 1; // Counter for elimination rounds
    while (pl->next != NULL && checkGameState(first, n) == 1) // Continue until the game is over
    {
        if (i == k && pl->elimination == false) // Check if it's the k-th player
        {
            // Output elimination message
            fout << "Player: " << pl->name << ", number: " << pl->number + 1 << " has been eliminated\n";
            pl->elimination = true; // Mark player as eliminated
            i = 1; // Reset counter
        }
        if (i != k && pl->elimination == false)
            i++; // Increment counter if player is not eliminated
        pl = pl->next; // Move to the next player
    }
}

int main()
{

    int n,i,k;

    do {
           cout << "Number of players to enter the game: ";
           cin >> n;

           if(cin.fail()) {  // Check if the input failed (not a number)
               cin.clear();   // Clear the error flag on cin
               cin.ignore(numeric_limits<streamsize>::max(), '\n');
               cout << "Invalid input. Please enter a number." << endl;
           }
           else {
               break;  // Input is valid, exit the loop
           }
       } while (true); // Loop while input is valid (number)

    for(i=0;i<n;i++)
    {
      char name[20];
      cout << "Player name (" << i + 1 << "): ";
      cin.get();
      cin.get(name,20);
      addPlayer(first,i,name);
    }

    fout << "\nPlayer list :" << endl;
    showPlayers(first);
    fout << endl;

    cout << "Enter a number or a phrase: ";
    char ks[100];
    cin.get();
    cin.get(ks,100);
    // Check if the input is a number or a phrase
    if(checkInput(ks)==1)
     {
         ss << ks; // Store the number in stringstream
         ss >> k; // Extract the number
     }
     else
       k=phraseNumbering(ks);
    fout << "Order of elimination (counter: " << k << "): " << endl;
    Elimination(first,k,n);
    fout << "\nWinner: ";
    winner(first);

    return 0;
}
