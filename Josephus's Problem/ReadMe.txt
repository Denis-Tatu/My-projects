The Josephus problem is a theoretical problem in mathematics and computer science where a group of people stand in a circle, and a step count (usually called k) is used to eliminate every k-th person around the circle until only one person remains. The challenge is to determine the position of the last survivor.

This program can be seen as an implementation of the Josephus problem, but with a practical twist — it involves user-defined inputs and outputs the elimination order step-by-step. It follows the fundamental mechanics of the Josephus problem by repeatedly eliminating players until only one remains in a circular structure.

Players in a Circle: In this code, players are arranged in a circular linked list (Player *next). This mirrors the circle of people in the Josephus problem.

Elimination Process: The elimination process is driven by the function Elimination(), where every k-th player is eliminated based on the value of k. The game continues until only one player is left, similar to how in the Josephus problem every k-th person is removed until only one person survives.

Circular Structure: The fact that pl->next points back to first ensures that the player list forms a circular structure, mimicking the continuous circle in the Josephus problem.

Determining the Survivor: Once all players except one are eliminated, the winner() function identifies and prints the remaining player, just like determining the "safe position" in the Josephus problem.

Input Handling: The program reads user input for the number of players and their names, along with a command for elimination based on either a number or a phrase.

Output: The program writes all relevant information (players, elimination order, winner) to an output file called "output.txt".
