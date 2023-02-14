
import cv2
import subprocess


if __name__ == '__main__':




        subprocess.check_call([r".//toolkits//adb//adb.exe", "shell", "/system/bin/screencap", "-p", "/sdcard/screencap.png"])
        subprocess.check_call([r".//toolkits//adb//adb.exe", "pull", "/sdcard/screencap.png", "./screencap.png"])