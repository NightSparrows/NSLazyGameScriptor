
import cv2

import time

from core.Logger import Logger
from core.State import State
from core.ADBDevice import ADBDevice
from core.GameData import GameData

from utils.opencvUtil import OpenCVUtil

from ..assets import Assets

class DailyState(State):
    
    s_dailyBtnImage = cv2.imread('.//assets//fgo//state//daily//dailyBtn.png')

    def __init__(self, gameData: GameData) -> None:
        super().__init__('Daily')
        self.m_data = gameData

    def goback(self):
        Logger.info('daily state go back')

        if self.m_data.currentState != self.getName():
            Logger.error('Current state is not daily!')
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

    def detectDailyBtnAndClick(self):
        result = ADBDevice.scan_screenshot(DailyState.s_dailyBtnImage)

        if (result['max_val'] > 0.9):
            point = OpenCVUtil.calculated(result, DailyState.s_dailyBtnImage.shape)
            ADBDevice.tap(point['x']['center'], point['y']['center'])
            return True

        return False

    def enter(self):
        Logger.info('Entering daily state')
        # assert is in gate state
        if (self.m_data.currentState != 'Gate'):
            Logger.warn('Current state not gate cant enter.')
            return False

        # 往上滑找Daily按鈕
        pressed = False
        for i in range(1, 5):
            ADBDevice.screenshot()
            if (self.detectDailyBtnAndClick()):
                pressed = True
                break
            else:
                ADBDevice.swipe(1000, 200, 1000, 500)
                time.sleep(1)

        # 往下找
        if not pressed:
            for i in range(1, 10):
                ADBDevice.screenshot()
                if (self.detectDailyBtnAndClick()):
                    pressed = True
                    break
                else:
                    ADBDevice.swipe(1000, 500, 1000, 200)
                    time.sleep(1)
        
        if pressed:
            return True
        else:
            return False

    def detect(self):
        raise NotImplementedError('state detect() not impl.')

    def getParentName(self):
        return 'Gate'
