
import cv2

from core.State import State
from core.Logger import Logger
from core.ADBDevice import ADBDevice

from utils.opencvUtil import OpenCVUtil

from core.GameData import GameData

# the init state of FGO
class LobbyState(State):
    
    def __init__(self, gameData: GameData) -> None:
        super().__init__('Lobby')
        self.m_data = gameData
        self.m_annImage = cv2.imread('.//assets//fgo//stateDetect//lobby.png')

    def goback(self):
        Logger.warn('The lobby state is the init state, cant go back')

    def enter(self):
        Logger.warn('Maybe future will implement this function')

    def detect(self):

        screenshot = ADBDevice.getScreenshot()

        result = OpenCVUtil.match(screenshot[0:100, 0:400], self.m_annImage)

        if (result['max_val'] > 0.93):
            Logger.info('Is in lobby')
            return True
        

        return False

    def getParentName(self):
        return 'None'


