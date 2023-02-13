
import time

from .BattleTask import BattleTask

from core.ADBDevice import ADBDevice
from core.Logger import Logger

class SkillBattleTask(BattleTask):

    def __init__(self, charNo: int, skillNo: int, useCharNo: int) -> None:
        self.m_charNo = charNo
        self.m_skillNo = skillNo
        self.m_useCharNo = useCharNo

    def execute(self):


        skillX = 70 + (self.m_charNo - 1) * 320 + (self.m_skillNo - 1) * 90

        ADBDevice.tap(skillX, 580)
        time.sleep(1)

        if self.m_useCharNo != -1:
            useCharX = 320 * self.m_useCharNo
            ADBDevice.tap(useCharX, 450)
            time.sleep(1)

        Logger.info('skill ' + str(self.m_charNo) + ' ' + str(self.m_skillNo) + ' executed.')
        return True
