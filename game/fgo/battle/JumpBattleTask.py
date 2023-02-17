
import time
import cv2

from core.Logger import Logger
from core.ADBDevice import ADBDevice

from .BattleTask import BattleTask
from .BattleData import BattleData

class JumpBattleTask(BattleTask):

    def __init__(self, data: BattleData, jumpCmdNo: int) -> None:
        self.m_jumpCmdNo = jumpCmdNo
        self.m_data = data

    def execute(self):
        self.m_data.executePC = self.m_jumpCmdNo
        return True





