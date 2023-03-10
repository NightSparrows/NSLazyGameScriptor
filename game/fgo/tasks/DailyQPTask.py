
import cv2
import time
import datetime

from core.Logger import Logger
from core.Task import Task
from core.ADBDevice import ADBDevice
from core.StateManager import StateManager

from utils.opencvUtil import OpenCVUtil

from ..battle.Battle import Battle
from ..battle.Apple import Apple

class DailyQPTask(Task):

    s_QPQuestBtnImage = cv2.imread('.//assets//fgo//task//dailyQP//QPBtn.png')

    # battle: 你的battle設定黨(class)
    def __init__(self, date: datetime, stateManager: StateManager, battle: Battle, executeTime = 1) -> None:
        super().__init__('DailyQP', date)
        self.m_stateManager = stateManager
        self.m_battle = battle
        self.m_executeTime = executeTime
    
    def pressTaskBtn(self):
        for i in range(5):
            ADBDevice.screenshot()
            result = ADBDevice.scan_screenshot(DailyQPTask.s_QPQuestBtnImage)
            if result != None:
                point = OpenCVUtil.calculated(result, DailyQPTask.s_QPQuestBtnImage.shape)
                ADBDevice.tap(point['x']['center'], point['y']['center'])
                time.sleep(1)
                return True

            ADBDevice.holdScroll(1150, 210, 1150, 350, 600)
            time.sleep(1)

        return False

    def execute(self):
        Logger.info('Start executing task: daily QP')
        # goto the daily
        if not self.m_stateManager.goto('Daily'):
            Logger.error('Daily QP Task failed to goto parent state.')
            return False
        
        # tap the scroll the get to the bottom (因為通常在下面)
        time.sleep(1)
        ADBDevice.tap(1258, 530)
        time.sleep(1)

        #scroll up and search the QP task button and pressed it
        toBattle = self.pressTaskBtn()
            
        if toBattle:
            Apple.checkAppleWindow()
            result, count = self.m_battle.execute(self.m_executeTime)
            if result:
                Logger.info('Daily QP task complete')
                return True
            else:
                self.pressTaskBtn()
                result, _ = self.m_battle.execute(self.m_executeTime - count)
                if result:
                    Logger.info('Daily QP task complete')
                    return True
                else:
                    Logger.error('Failed to complete daily QP task')
                    return False


        
        return False

    


