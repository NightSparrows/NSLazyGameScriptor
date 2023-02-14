
import cv2
import time

from game.fgo.GameFGO import GameFGO

from game.fgo.battle.Battle import Battle
from game.fgo.tasks.DailyQPTask import DailyQPTask
#from module.logger import logger

if __name__ == '__main__':

    game = GameFGO()
    battle = Battle( 8, 'skadi', [True, False, True], 
    "skill 2 3\ncard c2 r r\nskill 1 3 2\nskill 1 1 2\nskill 3 1 2\nskill 2 1\ncard c2 r r\nskill 3 3 2\ncard c2 r r\n",
    "")
    qpTask = DailyQPTask(game.m_stateManager, battle, 5)
    game.restart()

    qpTask.execute()

    exit()
    battle = Battle( 8, 'skadi', [True, False, True], 
    "skill 2 3\ncard c2 r r\nskill 1 3 2\nskill 1 1 2\nskill 3 1 2\nskill 2 1\ncard c2 r r\nskill 3 3 2\ncard c2 r r\n",
    "")

    #battle.inBattle()
    battle.execute(10)

    exit()

    game = GameFGO()
    
    game.restart()

    exit()

    game = GameFGO()
    
    game.initState()
    game.m_stateManager.goto('Daily')

    game.m_stateManager.goto('Lobby')

    exit()

    battle.chooseFriend()

    exit()

    game = GameFGO()
    
    game.restart()

    count = 0

    for i in range(1, 1000):
        time.sleep(1)
        ADBDevice.screenshot()

        screenshot = ADBDevice.getScreenshot()
        annImage = cv2.imread('.//assets//fgo//state//gate//title.png')
        #annImage = cv2.imread('.//assets//fgo//stateDetect//chooseFriend.png')

        #cv2.imshow("", screenshot[0:65, 500:1280])
        #cv2.waitKey(0)

        result = OpenCVUtil.match(screenshot[0:65, 500:1280], annImage, cv2.TM_CCOEFF_NORMED)

        print('max_val: ' + str(result['max_val']))
        if (result['max_val'] > 0.93):
            continue
        else:
            Logger.info('Is not gate!')
            count += 1
    
    print('Not gate: ' + str(count))

