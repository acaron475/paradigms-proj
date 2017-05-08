from twisted.internet import reactor
from time import sleep
from twisted.python import log
import sys
from twisted.internet.defer import DeferredQueue
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import *

player1_port = 40129
player2_port = 41129
observer_port = 42129

class Player1_Handler(Protocol):
    def __init__(self):
        self.num = 1
        self.queue = DeferredQueue()
        self.open = False
    
    def dataReceived(self,data): 
        self.queue.put(data)
        print(data)

    def connectionMade(self):
        self.open = True
        startPlayer2Connection(self)
    
    def connectionLost(self,reason):
        if self.open == True:
            self.open = False
            closeConnections(self)
    
    def forwardData(self,data):
        self.otherPlayer.transport.write(data)
        self.queue.get().addCallback(self.forwardData)
    
    def startForwarding(self):
        self.queue.get().addCallback(self.forwardData)

class Player1_Handler_Factory(Factory):
    def buildProtocol(self,addr):
        return Player1_Handler()
    
class Player2_Handler(Protocol):
    def __init__(self,otherPlayer):
        self.num = 2
        self.otherPlayer = otherPlayer
        self.open = False
        self.otherPlayer.otherPlayer = self
    
    def dataReceived(self,data):
        print(data)
        self.otherPlayer.transport.write(data)
    
    def connectionMade(self):
        self.open = True
        self.otherPlayer.startForwarding()
        print("CONNECTION MADE")
#        startObserverConnection(self)
    
    def connectionLost(self,reason):
        if self.open == True:
            self.open = False
            closeConnections(self)
    
    def forwardData(self,data):
        self.queue.get().addCallback(self.forwardData)
        

class Player2_Handler_Factory(Factory):
    def __init__(self,connection):
        self.connection = connection
    
    def buildProtocol(self,addr):
        return Player2_Handler(self.connection)

def startPlayer2Connection(player1):
    dataEndpoint = TCP4ServerEndpoint(reactor,player2_port)
    dataEndpoint.listen(Player2_Handler_Factory(player1))

def closeConnections(connection):
    connection.otherPlayer.open = False
    connection.otherPlayer.transport.loseConnection()
    reactor.stop()

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    dataEndpoint = TCP4ServerEndpoint(reactor,player1_port)
    dataEndpoint.listen(Player1_Handler_Factory())
    reactor.run()
    
    
