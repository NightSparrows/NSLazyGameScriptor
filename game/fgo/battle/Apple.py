
import time
import cv2

from core.Logger import Logger
from core.ADBDevice import ADBDevice

class Apple:

    s_appleWindow = cv2.imread('.//assets//fgo//battle//appleWindow.png')
    s_copperAppleImage = cv2.imread('.//assets//fgo//battle//copperApple.png')
    s_OKBtnImage = cv2.imread('.//assets//fgo//battle//ok.png')

    def checkAppleWindow():

        Logger.info('Checking apple window...')
        result = ADBDevice.WaitUntil(Apple.s_appleWindow, 2)

        if result == None:
            Logger.info('No apple window')
            return False
        else:
            Logger.info('Having apple window, Eat apple')
            Apple.eatApple()
            return True


    def eatApple():
        ADBDevice.swipe(640, 400, 640, 200)
        time.sleep(1)
        ADBDevice.tapImage(Apple.s_copperAppleImage)
        timer = 0
        Tapped = False
        while timer < 5:
            time.sleep(0.5)
            ADBDevice.screenshot()
            result = ADBDevice.scan_screenshot(Apple.s_OKBtnImage)
            if result['max_val'] > ADBDevice.s_maxValue:
                Logger.info('OK window is not close')
                if ADBDevice.tapImage(Apple.s_OKBtnImage):
                    Tapped = True
            else:
                if Tapped:
                    Logger.info('apple eaten.')
                    break
            timer += 1
            time.sleep(1)

        
