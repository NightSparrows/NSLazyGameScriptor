

import subprocess

import cv2
import numpy
import time
import lz4.block

import numpy as np


from .Logger import Logger
from utils.opencvUtil import OpenCVUtil

class ADBDevice:

    s_maxValue = 0.91
    s_delay = 1
    s_screenshot = None
    s_adbExePath = '.\\toolkits\\adb\\adb.exe'
    s_connectEmulator = 'emulator-5554'

    #s_screenCap = '/system/bin/screencap'
    s_screenCap = '/data/local/tmp/ascreencap'

    def init() -> None:

        subprocess.check_output(ADBDevice.s_adbExePath + ' -s ' + ADBDevice.s_connectEmulator + ' push toolkits/ascreenCap/x86_64/ascreencap /data/local/tmp')
        subprocess.check_output(ADBDevice.s_adbExePath + ' -s ' + ADBDevice.s_connectEmulator + ' shell chmod 777 /data/local/tmp/ascreencap')

        ADBDevice.s_maxValue = 0.93         # max value of matching
        ADBDevice.s_delay = 2               # delay capture screen time
        #ADBDevice.screenshot()
    
    def screenshot_save():
        subprocess.check_output(ADBDevice.s_adbExePath + ' -s ' + ADBDevice.s_connectEmulator + ' exec-out ' + ADBDevice.s_screenCap + ' -f /sdcard/screencap.bmz')
        subprocess.check_output(ADBDevice.s_adbExePath + ' -s ' + ADBDevice.s_connectEmulator + ' pull /sdcard/screencap.bmz ./screencap.bmz')
        return

    # capture the screen for operation
    def screenshot():
        #
        pipe = subprocess.Popen(ADBDevice.s_adbExePath + ' -s ' + ADBDevice.s_connectEmulator + ' exec-out ' + ADBDevice.s_screenCap + ' --pack 2 --stdout',
                        stdout=subprocess.PIPE, shell=True)
        #image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
        #image = cv2.imdecode(numpy.fromstring(image_bytes, numpy.uint8), cv2.IMREAD_COLOR)
        #ADBDevice.s_screenshot = image
        
        data = pipe.stdout.read()
        pipe.terminate()

        # See headers in:
        # https://github.com/ClnViewer/Android-fast-screen-capture#streamimage-compressed---header-format-using
        compressed_data_header = np.frombuffer(data[0:20], dtype=np.uint32)
        
        if compressed_data_header[0] != 828001602:
            compressed_data_header = compressed_data_header.byteswap()
            if compressed_data_header[0] != 828001602:
                Logger.error('Failed to verify aScreenCap data header!')
                return False
        
        _, uncompressed_size, _, width, height = compressed_data_header
        channel = 3
        decodeData = lz4.block.decompress(data[20:], uncompressed_size=uncompressed_size)

        image = np.frombuffer(decodeData, dtype=np.uint8)
        if image is None:
            Logger.error('Empty image after reading from buffer')
            return False
        
        try:
            image = image[-int(width * height * channel):].reshape(height, width, channel)
        except ValueError as e:
            Logger.error('cannot reshape array of size 0 into shape')
            return False
    
        image = cv2.flip(image, 0)
        if image is None:
            Logger.error('Empty image after cv2.flip')

        #cv2.imshow('', image)
        #cv2.waitKey(0)
        ADBDevice.s_screenshot = image
        
    def getScreenshot():
        return ADBDevice.s_screenshot

    def scanAndRetry(prepared, retryCount):
        count = 0
        while True:
            if count >= retryCount:
                return None
            ADBDevice.screenshot()
            result = ADBDevice.scan_screenshot(prepared)
            if result['max_val'] > 0.9:
                return result
            count += 1
            time.sleep(1)

    #scan the current screenshot for prepared image
    def scan_screenshot(prepared, method = cv2.TM_CCOEFF_NORMED):
        result = cv2.matchTemplate(ADBDevice.s_screenshot, prepared, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        #cv2.imshow("", result)
        #cv2.waitKey(0)
        return {'screenshot': ADBDevice.s_screenshot, 'min_val':min_val, 'max_val':max_val, 'min_loc':min_loc, 'max_loc':max_loc}

    def tapImage(prepared):
        ADBDevice.screenshot()
        result = ADBDevice.scan_screenshot(prepared)
        if result['max_val'] > ADBDevice.s_maxValue:
            point = OpenCVUtil.calculated(result, prepared.shape)
            ADBDevice.tap(point['x']['center'], point['y']['center'])
            time.sleep(1)
            return True
        return False


    # wait for something appear
    def WaitUntil(prepared, timeout):

        counter = 0.0

        while True:
            ADBDevice.screenshot()
            result = ADBDevice.scan_screenshot(prepared)
            if (result['max_val'] > ADBDevice.s_maxValue):
                return result
            
            if (counter >= timeout):
                return None

            time.sleep(ADBDevice.s_delay)
            counter += ADBDevice.s_delay
            
    def openApp(appName):
        return subprocess.check_output([ADBDevice.s_adbExePath,'-s', ADBDevice.s_connectEmulator, "shell", "am", "start", "-n", appName])

    def killApp(appName):
        return subprocess.check_output([ADBDevice.s_adbExePath,'-s', ADBDevice.s_connectEmulator, "shell", "am", "force-stop", appName])

    # Tap the screen
    def tap(x, y):
        subprocess.check_output(ADBDevice.s_adbExePath + ' -s ' + ADBDevice.s_connectEmulator + ' shell input tap %d %d' % (x, y), shell=True)

    # Swipe the screen
    def swipe(x0, y0, x1, y1):
        subprocess.check_output(ADBDevice.s_adbExePath + ' -s ' + ADBDevice.s_connectEmulator + ' shell input swipe %d %d %d %d' % (x0, y0, x1, y1), shell=True)

    # ??????
    # time in millisecond
    def hold(x, y, time):
        subprocess.check_output(ADBDevice.s_adbExePath + ' -s ' + ADBDevice.s_connectEmulator + ' shell input swipe %d %d %d %d %d' % (x, y, x, y, time), shell=True)

    # ??????
    # time in millisecond
    def holdScroll(x0, y0, x1, y1, time):
        subprocess.check_output(ADBDevice.s_adbExePath + ' -s ' + ADBDevice.s_connectEmulator + ' shell input swipe %d %d %d %d %d' % (x0, y0, x1, y1, time), shell=True)
