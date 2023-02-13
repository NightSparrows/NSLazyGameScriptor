
import time
import cv2

from core.Logger import Logger
from core.ADBDevice import ADBDevice

from .BattleTask import BattleTask


class CardBattleTask(BattleTask):

    s_atkBtnImage = cv2.imread('.//assets//fgo//battle//attackBtn.png')
    def __init__(self, cards) -> None:
        self.m_cards = cards
        assert(len(cards) == 3)

    def execute(self):
        
        # 按attack進入選卡
        result = ADBDevice.WaitUntil(CardBattleTask.s_atkBtnImage, 5)
        
        if result == None:
            Logger.info('Failed to get attack button')
            return False
        
        time.sleep(1)
        ADBDevice.tap(result['max_loc'][0], result['max_loc'][1])
        time.sleep(1)

        chosenCard = [False, False, False, False, False]
        for i in range(3):
            time.sleep(1)
            cardCmd = self.m_cards[i]

            if cardCmd[0] == 'c':   # 寶具
                charNo = int(cardCmd[1])
                cardX = 140 + (charNo * 250)
                ADBDevice.tap(cardX, 220)
                Logger.info('Choose 寶具' + str(charNo))
            elif cardCmd[0] == 'r':           # 隨便選
                for j in range(5):
                    if (chosenCard[j]):
                        continue
                    cardX = 140 + (j * 250)
                    ADBDevice.tap(cardX, 500)
                    Logger.info('Choose random ' + str(j))
                    chosenCard[j] = True
                    break
            else:
                Logger.error('Card script syntax error')
                return False

        return True





