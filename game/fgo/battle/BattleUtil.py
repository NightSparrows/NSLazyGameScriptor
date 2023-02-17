
from core.Logger import Logger

from .BattleData import BattleData
from .SkillBattleTask import SkillBattleTask
from .CardBattleTask import CardBattleTask
from .JumpBattleTask import JumpBattleTask

class BattleUtil:

    # state method for searialize the battle script
    def SerializeTask(data: BattleData, script: str):
        tasks = list()

        scriptLines = script.splitlines()

        for line in scriptLines:
            cmdArgs = line.split(' ')
            if cmdArgs[0] == 'skill':
                task = None
                if len(cmdArgs) == 3:
                    task = SkillBattleTask(charNo=int(cmdArgs[1]), skillNo=int(cmdArgs[2]), useCharNo=-1)
                elif len(cmdArgs) == 4:
                    task = SkillBattleTask(charNo=int(cmdArgs[1]), skillNo=int(cmdArgs[2]), useCharNo=int(cmdArgs[3]))
                else:
                    Logger.error('skill command syntax error')
                    return None
                tasks.append(task)
            elif cmdArgs[0] == 'card':
                assert(len(cmdArgs) == 4)
                task = CardBattleTask([cmdArgs[1], cmdArgs[2], cmdArgs[3]])
                tasks.append(task)
            elif cmdArgs[0] == 'jump':
                assert(len(cmdArgs) >= 2)
                task = JumpBattleTask(data, int(cmdArgs[1]))
                tasks.append(task)
            else:
                Logger.error("Unknown script command.")

        return tasks
