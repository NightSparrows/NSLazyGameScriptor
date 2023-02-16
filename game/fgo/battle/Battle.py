
import cv2
import time
from enum import Enum

from core.Logger import Logger
from core.ADBDevice import ADBDevice
from utils.opencvUtil import OpenCVUtil

from .BattleData import BattleData
from .BattleUtil import BattleUtil
from .Apple import Apple

from ..assets import Assets

class Battle:

    class Stage(Enum):
        ChooseFriend = 'chooseFriend'
        ChooseParty = 'chooseParty'
        InBattle = 'inBattle'
        End = 'end'

    s_winConditionImage = cv2.imread('.//assets//fgo//battle//winCondition.png')
    s_nextStepBtnImage = cv2.imread('.//assets//fgo//battle//nextStepBtn.png')
    s_endDicisionImage = cv2.imread('.//assets//fgo//battle//endDicision.png')
    s_refreshBtnImage = cv2.imread('.//assets//fgo//battle//refreshBtn.png')

    # partyNumber: 1 ~ 10
    def __init__(self, partyNumber: int, friend: str, skill, script: str, prefer: str) -> None:
        self.m_partyNumber = partyNumber
        self.m_friendInfo = {
            'name' : friend,
            'class' : 5,            # TODO: 我懶得設定以後再說，預設術職
            'nameImage' : cv2.imread('.//assets//fgo//servant//' + friend + '//name.png'),
            'skill1' : cv2.imread('.//assets//fgo//servant//' + friend + '//skill1.png'),
            'skill2' : cv2.imread('.//assets//fgo//servant//' + friend + '//skill2.png'),
            'skill3' : cv2.imread('.//assets//fgo//servant//' + friend + '//skill3.png')
            }
        self.m_skill = skill                    # 技10 三個float
        
        # serialize script
        self.m_data = BattleData()
        self.m_tasks = BattleUtil.SerializeTask(script)
        Logger.info('Implement ' + str(len(self.m_tasks)) + ' tasks.')

        self.m_skipChooseParty = False

        #assets load
        self.m_inBattleFlagImage = cv2.imread('.//assets//fgo//battle//inBattleFlag.png')
        self.m_touchImage = cv2.imread('.//assets//fgo//battle//touch.png')
        self.m_attackBtnImage = cv2.imread('.//assets//fgo//battle//attackBtn.png')

    # 選擇好友的method
    def chooseFriend(self):
        inStage = False
        Logger.info('assert is in choose friend stage')
        for i in range(3):      # retry 3 time for checking it is in choose friend stage
            time.sleep(1)
            ADBDevice.screenshot()
            result = ADBDevice.scan_screenshot(Assets.chooseFriendIcon)
            if result['max_val'] > 0.9:
                inStage = True
                break
        
        if not inStage:
            return False
        
        # 選擇助戰職階
        classX = 90 + self.m_friendInfo['class'] * 68
        Logger.info('choosing the correct classes ... ')
        for i in range(2):
            ADBDevice.tap(classX, 128)
            time.sleep(1)

        # Find servant
        foundServant = False
        Logger.info('Finding servant ... ')
        refreshCount = 0
        while True:
            for i in range(10):
                # scan for servant
                foundServant = False
                time.sleep(1)
                ADBDevice.screenshot()
                result = ADBDevice.scan_screenshot(self.m_friendInfo['nameImage'])
                if OpenCVUtil.isMatch(result):                        # found servant
                    Logger.info('Found servant!')
                    foundServant = True
                    # check the skill 
                    servantPosition = [result['max_loc'][0], result['max_loc'][1]]
                    skillLeft = servantPosition[0] + 460
                    skillTop = servantPosition[1]
                    skillImage = ADBDevice.getScreenshot()[skillTop:(skillTop + 105), skillLeft:(skillLeft + 300)]
                    #cv2.imshow("", skillImage)
                    #cv2.waitKey(0)


                    if (self.m_skill[0] == True):
                        Logger.info('Checking skill 1 ... ')
                        result = OpenCVUtil.match(skillImage, self.m_friendInfo['skill1'])
                        if (not OpenCVUtil.isMatch(result)):
                            foundServant = False
                        else:
                            Logger.info('Skill 1 match!')
                    if (self.m_skill[1] == True):
                        Logger.info('Checking skill 2 ... ')
                        result = OpenCVUtil.match(skillImage, self.m_friendInfo['skill2'])
                        if (not OpenCVUtil.isMatch(result)):
                            foundServant = False    # 不符合找下一個
                        else:
                            Logger.info('Skill 2 match!')
                    if (self.m_skill[2] == True):
                        Logger.info('Checking skill 3 ... ')
                        result = OpenCVUtil.match(skillImage, self.m_friendInfo['skill3'])
                        if (not OpenCVUtil.isMatch(result)):
                            foundServant = False    # 不符合找下一個
                        else:
                            Logger.info('Skill 3 match!')
                    
                    # TODO 禮裝檢查

                    # Choose it!
                    if (foundServant):
                        Logger.info('Servant ' + self.m_friendInfo['name'] + ' Found!')
                        time.sleep(0.5)
                        ADBDevice.tap(servantPosition[0], servantPosition[1])
                        return True

                # 沒找到，scroll一個
                ADBDevice.holdScroll(128, 610, 128, 450, 500)
                time.sleep(1)
            
            # 沒找到，refresh
            result = ADBDevice.scanAndRetry(Battle.s_refreshBtnImage, 3)
            if result == None:
                return False
            else:
                refreshCount += 1
                point = OpenCVUtil.calculated(result, Battle.s_refreshBtnImage.shape)
                ADBDevice.tap(point['x']['center'], point['y']['center'])

                # TODO OK button press, 他是'是'
                result = ADBDevice.scanAndRetry(Assets.YesBtnImage, 3)
                time.sleep(1)
                if result != None:
                    point = OpenCVUtil.calculated(result, Assets.YesBtnImage.shape)
                    ADBDevice.tap(point['x']['center'], point['y']['center'])
                    Logger.info('click ok button')
                    time.sleep(1) 
                else:
                    Logger.error('Press refresh dont have window.')
                    return False       
                if (refreshCount >= 5):
                    Logger.error('Do you dont have friends?')
                    return False
            

        return False

    def chooseParty(self):

        # TODO Make sure you are in choose party
        time.sleep(2)
        ADBDevice.tap(527, 50)
        time.sleep(1)
        
        
        partyBtnX = 527 + (self.m_partyNumber - 1) * 25

        time.sleep(1)
        ADBDevice.tap(partyBtnX, 50)

        time.sleep(2)
        ADBDevice.tap(1165, 675)
        #ADBDevice.hold(1165, 675, 100)

        return True


    def inBattle(self):

        # init battle variables
        self.m_data.executePC = 0
        result = ADBDevice.WaitUntil(self.m_inBattleFlagImage, 60)
        result = ADBDevice.WaitUntil(self.m_attackBtnImage, 60)

        isWin = False
        while not isWin:

            Logger.info('Wait for battle safty stage...')
            timer = 0
            while timer < 60.0:
                ADBDevice.screenshot()
                screenshot = ADBDevice.getScreenshot()
                result1 = OpenCVUtil.match(screenshot, self.m_inBattleFlagImage)
                result2 = OpenCVUtil.match(screenshot, self.m_attackBtnImage)
                if (OpenCVUtil.isMatch(result1) and OpenCVUtil.isMatch(result2)):
                    break       # is safty
                #check win condition
                result = OpenCVUtil.match(screenshot, Battle.s_nextStepBtnImage)
                if OpenCVUtil.isMatch(result):
                    isWin = True
                    break
                ADBDevice.tap(900, 55)
                time.sleep(1)
                timer += 1

            # assert in stable battle state
            time.sleep(1)
            if isWin:
                break

            if (timer >= 60):
                Logger.error('Failed to wait safty stage')
                raise NotImplementedError()

            if (self.m_data.executePC == len(self.m_tasks)):
                # check if it is 
                result = ADBDevice.WaitUntil(self.m_touchImage, 5)
                if (result != None):
                    ADBDevice.tap(640, 360)
                    isWin = True
                    break
                else:
                    raise NotImplementedError()

            self.m_tasks[self.m_data.executePC].execute()
            self.m_data.executePC += 1
        
        if isWin:
            Logger.info('Battle win')
            ADBDevice.tap(1100, 640)
            time.sleep(1)
            return True
            # tap the next step btn ...
        raise NotImplementedError()

    def execute(self, count: int = 1):
        self.m_currentStage = Battle.Stage.ChooseFriend

        self.m_endFlags = False

        executeCount = 0

        while not self.m_endFlags:
            if self.m_currentStage == Battle.Stage.ChooseFriend:
                if not self.chooseFriend():
                    Logger.error('Failed to choose friend!')
                else:
                    if self.m_skipChooseParty:
                        self.m_currentStage = Battle.Stage.InBattle
                    else:
                        self.m_currentStage = Battle.Stage.ChooseParty
            elif self.m_currentStage == Battle.Stage.ChooseParty:
                if not self.chooseParty():
                    Logger.error('Failed to choose party')
                else:
                    self.m_currentStage = Battle.Stage.InBattle
            elif self.m_currentStage == Battle.Stage.InBattle:
                if not self.inBattle():
                    Logger.error('Failed to do battle')
                else:
                    self.m_currentStage = Battle.Stage.End
            elif self.m_currentStage == Battle.Stage.End:  # 戰鬥結束
                executeCount += 1
                Logger.info('戰鬥結束，完成第' + str(executeCount) + '次')
                result = ADBDevice.WaitUntil(Battle.s_endDicisionImage, 5)
                time.sleep(1)
                if result == None:
                    Logger.error('無法找到結束確認視窗')
                    return False
                else:
                    if (executeCount == count):
                        self.m_endFlags = True
                        ADBDevice.tap(444, 567)
                        time.sleep(1)
                    else:
                        self.m_skipChooseParty = True
                        self.m_currentStage = Battle.Stage.ChooseFriend
                        ADBDevice.tap(840, 565)
                        time.sleep(1)

                        # checking apple
                        Apple.checkAppleWindow()
            else:
                Logger.error('Unknown battle stage')
                return False
        
        Logger.info('Battle task complete.')
        return True
        


