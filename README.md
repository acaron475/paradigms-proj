# paradigms-proj

## Program Summary
This project is a billiards game played between 2 different people over the internet.  A server is launched that handles data relaying between the 2 clients.

## Launching the Program
###### Mandatory Launch Order
1. Server
2. Client 1
3. Client 2

###### Client
1. Ensure client.py, billiards.py, and classes.py files are present
2. Run "python billiards.py \<server address> \<port>"
3. Python version used must be 3.4+
4. \<server address> is the internet address of the server
5. \<port> is either 40129 if this is the first client session or 41129 if this is the second client session

###### Server
1. Ensure server.py file is present
2. Run "python server.py"
3. Python version used must be 3.4+
4. Ports 40129 and 41129 must be open and unused on this machine!

## Playing the Game
###### Summary
The rules of the game follow those for a standard game of 8-ball pool/billiards.  There are two players with each one playing on a separate client program.  Players will take turns hitting the cueball to try and knock in the balls for their team.  The teams (stripes or solids) are determined by whichever ball is knocked in first with the scoring player joining the team of the type of ball knocked in.  When all of the balls of a player's team have been knocked in, that player then must knock in the 8 ball to win the game.  If the 8 ball is scored into a pocket at any time prior to that, the scoring player loses the game.  When a player scores a ball of their team into a pocket, they get to continue shooting until they miss one.  The shooting player will see their shot played out on their screen while the waiting player will see the results when all balls have stopped moving.  If the cueball is knocked in, it will be placed in a reset position, and the shooting player's turn will be over.  The games for both clients will close when either client shuts down.

###### Controls
1. Shooting Player
  * W: Increase power of shot (indicated by how far back the stick is pulled from the cueball)
  * S: Decrease power of shot (indicated by how far back the stick is pulled from the cueball)
  * A: Rotate angle of shot counter-clockwise (indicated by indicator line on cueball)
  * D: Rotate angle of shot clockwise (indicated by indicator line on cueball)
  * Spacebar: Take shot at indicated power and angle
  * ESC: Quit Game

2. Waiting Player
  * ESC: Quit Game

###### Helpful Hints
1. The current status of of the game is shown in the upper right hand corner of the display with one of 3 messages
  * Your Turn: It is currently your turn to shoot
  * Other Player's Turn: It is currently the other player's turn to shoot
  * Waiting for connection: The game is waiting for a connection to the server

2. The upper left hand corner will contain a message indicating which team you are on.  It will only appear when the first ball has been knocked into a pocket which decides teams.
  * Stripes: The striped colored balls numbered 9 through 15
  * Solids: The solid colored balls numbered 1 through 7
