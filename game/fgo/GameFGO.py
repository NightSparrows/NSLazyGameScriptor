
import cv2
import time
import datetime
import json

from core.Game import Game
from core.ADBDevice import ADBDevice
from core.Logger import Logger
from utils.opencvUtil import OpenCVUtil
from utils.util import Util

from .state.LobbyState import LobbyState
from .state.GateState import GateState
from .state.DailyState import DailyState

from .tasks.DailyQPTask import DailyQPTask

from .battle.Battle import Battle

from .assets import Assets

class GameFGO(Game):

    # 執行task
    def execute(self):
        if not self.m_enable:
            return False

        self.restart()
        
        # execute the tasks that should be done

        # find the closest tasks that should be execute
        # write the next execute time to the file

        raise NotImplementedError()

    def __init__(self) -> None:
        super().__init__('FGO')

        # load the setting file

        # load state image
        self.m_annImage = cv2.imread('.//assets//fgo//stateDetect//announcement.png')

        # creating init state
        self.m_lobbyState = LobbyState(self.getData())
        self.m_gateState = GateState(self.getData())
        self.m_dailyState = DailyState(self.getData())

        f = open('settings/fgo/config.json')
        fgoData = json.load(f)
        f.close()

        #TODO read battle settings from file
        # 讀取戰鬥設定檔
        self.m_battles = dict()

        for battleData in fgoData['battle']:
            battle = Battle( 
                battleData['partyNumber'],
                battleData['friendServantName'],
                battleData['skillRequirement'], 
                battleData['script'],
                ""
                )
            self.m_battles[battleData['name']] = battle
            Logger.info('Battle setting: ' + battleData['name'] + ' loaded.')

        # init tasks
        self.m_tasks = []

        # TODO read setting from file and setup the tasks
        qptaskData = fgoData['QPTask']
        time = Util.gt(qptaskData['datetime'])
        qptask = DailyQPTask(time, self.m_stateManager, self.m_battles[qptaskData['battleName']], qptaskData['executionTime'])
        self.m_tasks.append(qptask)

    def wrtieSettingToFile(self):
        raise NotImplementedError('Do not impl write config to file')

    def restart(self):
        ADBDevice.killApp('com.xiaomeng.fategrandorder')
        ADBDevice.openApp('com.xiaomeng.fategrandorder/jp.delightworks.Fgo.player.AndroidPlugin')

        # try to go to lobby
        # Retry one time to assert
        # 第一次重開一定有公告
        timer = 0
        Logger.info('Wait for 公告視窗')
        while timer <= 60:
            ADBDevice.screenshot()
            screenshot = ADBDevice.getScreenshot()

            # whether it have open 公告
            result = OpenCVUtil.match(screenshot[0:65, 0:1280], self.m_annImage)

            if (OpenCVUtil.isMatch(result)):
                Logger.info('Has announcement, close it')
                ADBDevice.tap(1275, 5)
                time.sleep(1)
                break

            # Unknown, tap safe position
            ADBDevice.tap(150, 400)
            timer += 1
            time.sleep(1)
        
        timer = 0
        loginPriceImage = cv2.imread('.//assets//fgo//state//lobby//loginPrice.png')
        Logger.info('確認是否有公告')
        while timer <= 2:
            ADBDevice.screenshot()
            screenshot = ADBDevice.getScreenshot()
            result = OpenCVUtil.match(screenshot[40:360, 300:1000], loginPriceImage)

            if (OpenCVUtil.isMatch(result)):
                Logger.info('Has a login price, close it')
                ADBDevice.tap(640, 560)
                time.sleep(1)
                break

            time.sleep(1)
            timer += 1

        # TODO 確認是否有友情點數
        while timer <= 3:
            ADBDevice.screenshot()
            result = ADBDevice.scan_screenshot(Assets.OKBtnImage)
            time.sleep(1)           # scan 到不代表按的到

            if (OpenCVUtil.isMatch(result)):
                Logger.info('有怪怪的視窗，按確定')
                point = OpenCVUtil.calculated(result, Assets.OKBtnImage.shape)
                ADBDevice.tap(point['x']['center'], point['y']['center'])
                time.sleep(1)
                break

            time.sleep(1)
            timer += 1


        while True:
            time.sleep(1)                           # wait for safty
            ADBDevice.screenshot()

            screenshot = ADBDevice.getScreenshot()

            # whether it is in lobby
            if (self.m_lobbyState.detect()):
                break
            
        
        self.initState()
        

        return True


    def initState(self):

        # init something
        self.getData().currentState = 'Lobby'

        # add state to state manager
        self.m_stateManager.init(self.m_lobbyState)
        self.m_stateManager.addState(self.m_gateState)
        self.m_stateManager.addState(self.m_dailyState)



        

