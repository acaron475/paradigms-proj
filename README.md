# paradigms-proj

## Program Summary
This project is a billiards game played between 2 different people over the internet.  A server is launched that handles data relaying between the 2 clients.

## Launching the Program
###### Client
1. Ensure client.py, billiards.py, and classes.py files are present
2. Run "python billiards.py <server address> <port>"
3. Python version used must be 3.4+
4. <server address> is the internet address of the server
5. <port> is either 40129 if this is the first client session or 41129 if this is the second client session

###### Server
1. Ensure server.py file is present
2. Run "python server.py"
3. Python version used must be 3.4+