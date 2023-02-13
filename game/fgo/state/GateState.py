
import cv2
import time

from core.State import State
from core.Logger import Logger
from core.ADBDevice import ADBDevice

from utils.opencvUtil import OpenCVUtil

from core.GameData import GameData

from ..assets import Assets

class GateState(State):

    def __init__(self, gameData: GameData) -> None:
        super().__init__('Gate')
        self.m_data = gameData
        self.m_titleImage = cv2.imread('.//assets//fgo//state//gate//title.png')
        self.m_enterBtnImage = cv2.imread('.//assets//fgo//state//gate//chaldeaGate.png')

    def goback(self):
        Logger.info('Try to go back from gate state')
        # assert is in this state
        if (self.m_data.currentState != self.getName()):
            Logger.warn('Current state not ' + self.getName() + ' cant go back.')
            return False
        
        time.sleep(1)
        ADBDevice.screenshot()
        result = ADBDevice.scan_screenshot(Assets.gobackBtnImage)

        if (result['max_val'] >= 0.95):
            point = OpenCVUtil.calculated(result, Assets.gobackBtnImage.shape)
            ADBDevice.tap(point['x']['center'], point['y']['center'])
            # 沒有改current state是因為上一個state不一定是parent
            return True

        return False

    def detectGateBtnAndClick(self):
        result = ADBDevice.scan_screenshot(self.m_enterBtnImage)

        if (result['max_val'] >= 0.95):
            point = OpenCVUtil.calculated(result, self.m_enterBtnImage.shape)
            ADBDevice.tap(point['x']['center'], point['y']['center'])
            return True

        return False


    def enter(self):
        # assert is in lobby state
        if (self.m_data.currentState != self.getParentName()):
            Logger.warn('Current state not ' + self.getParentName() + ' cant enter.')
            return False
        
        # 往上滑找嘉樂底按鈕
        pressed = False
        for i in range(1, 5):
            ADBDevice.screenshot()
            if (self.detectGateBtnAndClick()):
                pressed = True
                break
            else:
                ADBDevice.swipe(1000, 200, 1000, 500)
                time.sleep(1)
        if not pressed:
            for i in range(1, 10):
                ADBDevice.screenshot()
                if (self.detectGateBtnAndClick()):
                    break
                else:
                    ADBDevice.swipe(1000, 500, 1000, 200)
                    time.sleep(1)
        
        time.sleep(1)
        if (not self.detect()):
            return False
        else:
            # change the state
            self.m_data.currentState = self.getName()
            Logger.info('the current state is in chaldea gate')
            return True


    def detect(self):

        for i in range(0, 3):
            ADBDevice.screenshot()
            screenshot = ADBDevice.getScreenshot()
            annImage = cv2.imread('.//assets//fgo//state//gate//title.png')
            
            result = OpenCVUtil.match(screenshot[0:65, 500:1280], annImage, cv2.TM_CCOEFF_NORMED)

            if (result['max_val'] > 0.9):
                return True
            else:
                continue        # retry
        
        return False


    def getParentName(self):
        return str('Lobby')



