from twisted.internet.protocol import *
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from time import sleep
from twisted.python import log
import sys
from twisted.internet.defer import DeferredQueue
from twisted.internet.endpoints import TCP4ClientEndpoint
import billiards

class Player_Handler(Protocol):
    def __init__(self,player):
        self.open = False
        self.player = player
    
    def connectionMade(self):
        self.open = True
        self.player.connected = True
        self.player.connection = self
    
    def dataReceived(self,data):
        self.player.moveReceived(data)
    
    def connectionLost(self,reason):
        self.player.connected = False
        reactor.stop()

class Player_Handler_Factory(Factory):
    def __init__(self,player):
        self.player = player
    
    def buildProtocol(self,addr):
        return Player_Handler(self.player)
    
class Client():
    def __init__(self,player,dict):
        self.player = player
        self.dataDict = dict
    
    def startConnection(self):
        log.startLogging(sys.stdout)
        lc = LoopingCall(billiards.game_loop,self.dataDict)
        ret = lc.start(1/60)
        ret.addCallback(billiards.quit)
        
        dataEndpoint = TCP4ClientEndpoint(reactor,self.player.addr,self.player.port)
        dataEndpoint.connect(Player_Handler_Factory(self.player))
        reactor.run()

