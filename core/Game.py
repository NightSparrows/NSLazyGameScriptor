
from .GameData import GameData
from .StateManager import StateManager
from .State import State

class Game:

    def __init__(self, name: str) -> None:
        self.m_name = name
        self.m_data = GameData()
        self.m_stateManager = StateManager(self.m_data)

    def execute(self):
        raise NotImplementedError('Game ' + self.m_name + ' execute not impl')

    def restart(self):
        raise NotImplementedError('Game ' + self.m_name + ' restart not impl.')

    def getName(self):
        return self.m_name

    def getData(self):
        return self.m_data
