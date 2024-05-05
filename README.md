Janvi Lakhani jlakhani@stevens.edu

# GitHub Repository:

https://github.com/Janvi-Lakhani/Project_Adventure

# Time Spent on the Project:

Estimated hours spent: 15 hours

# Code Testing:

Manual testing

1. Note that case does not matter for any verbs, and arbitrary whitespace is allowed.
2. If there is no exit in that direction, go should give an error message.
3. If Uppercase GO with uppercase direction is given then You go direction in map is given which is the exact item in dictionary.
4. When a player successfully goes to a new room, you should show that room’s description
5. Look is showing the current room.
6. Trying to get things, if that aren’t there in inventory it should produce an error message.
7. Items getting using get verb will be shown in inventory by using inv or inventory verb/command. If inventory is empty it will produce error message.
8. Drop action is working and the transfer of element from inventory to map is working, if no items then give error.
9. Help is giving list of commands.
10. Quit testing with keyboard interruption CTRL+C or by giving quit command.
11. Locked door and Winning condition is also working. Both winning and loosing have been tested.

# Any bugs or issues I could not resolve:

No, There is not any bugs or issues I could not solve.

# Resolved Challenges:

Challenge: Initially, I used a large number of if statements to try to handle various scenarios, but this led to a lot of duplicated code, logical errors, and a more complicated code structure.
Solution: I adopted Python's construct machine to refactor the code, which not only effectively streamlined the code but also reduced the occurrence of errors and made debugging less challenging.

# Implemented Extensions:

A list of the three extensions to implement, with appropriate detail
New verb drop: This will take items from Inventory and put it down in the room.
New verb help: This will tell players what the valid commands are.
New verb locked room and winning condition: There is one room called "Boss Room". In the beginning when the player try to enter in that room the room is locked. For unlock the room and for win the game, player need "sword" and "magic wand" in inventory, otherwise player lose the game.
