
import time

from .Logger import Logger

from .State import State
from .GameData import GameData

class StateManager:

    def __init__(self, data: GameData) -> None:
        self.m_enteredStates = list()       # the stack of entered states
        self.m_states = dict()
        self.m_data = data
        
    def init(self, initState: State):
        self.m_initState = initState
        self.m_states[initState.getName()] = initState
        self.m_enteredStates.append(initState)

    def addState(self, state: State):
        Logger.info('Adding ' + state.getName() + ' state')
        self.m_states[state.getName()] = state

    # Goto the state
    def goto(self, name: str):

        # 回到初始state
        if name == self.m_initState.getName():
            print(len(self.m_enteredStates) - 1)
            for i in range(len(self.m_enteredStates) - 1):
                print(self.m_enteredStates)
                state = self.m_enteredStates.pop()
                if not state.goback():
                    Logger.error('Failed to go back')
                    return False
                self.m_data.currentState = self.m_enteredStates[i - 1].getName()
            
            return True

        # 找尋該state
        wishState = self.m_states[name]

        Logger.info('Try to goto ' + name + ' state')

        if (wishState == None):
            Logger.warn('Unknown state ' + name + ' cant goto.')
            return False
        

        parentStateName = wishState.getParentName()
        Logger.info(wishState.getName() + ' parent name is ' + parentStateName)


        # 
        parentList = list()             # 該state的所有父state
        previousState = self.m_states[parentStateName]

        while (previousState != self.m_initState):
            parentList.append(previousState)
            Logger.info('Found parent ' + previousState.getName())
            previousState = self.m_states[previousState.getParentName()]

        backStateCount = -1              # 需要back的count
        enterStateCount = 0             # 需要enter的count
        for state in self.m_enteredStates:
            backStateCount += 1
            enterStateCount = 0

            # iterate父state
            for parentState in parentList:
                if (state.getName() == parentState.getName()):      # 找到父state
                    break
                enterStateCount += 1

            if (state.getName() == name):                         # 找到自己，直接回去
                Logger.info('Find in previous go back')
                for i in range(backStateCount + 1):
                    state = self.m_enteredStates.pop()
                    if (state.goback()):
                        self.m_data.currentState = self.m_enteredStates[len(self.m_enteredStates) - 1].getName()
                    else:
                        Logger.error('Failed to go back')
                    time.sleep(1)
                self.m_data.currentState = name
                return True                                         # 回到自己，成功
        
        #assert
        print(backStateCount)
        print(enterStateCount)
        if (backStateCount == len(self.m_enteredStates) and parentStateName != self.m_initState.getName()):
            Logger.warn('Unknown state ' + name + ' cant goto with go backing.')
            return False

        # 需要goback的state
        for i in range(backStateCount):
            state = self.m_enteredStates.pop()
            if (state.goback()):
                self.m_data.currentState = self.m_enteredStates[len(self.m_enteredStates) - 1].getName()
        
        # 需要進入的父state
        while (enterStateCount != 0):
            enterStateCount -= 1
            entered = False
            for i in range(0, 3):
                Logger.info('Entering parent state ' + parentList[enterStateCount].getName())
                if (parentList[enterStateCount].enter()):
                    self.m_enteredStates.append(parentList[enterStateCount])
                    entered = True
                    break
            if not entered:
                return False

        # 進入自己
        for i in range(0, 3):
            if (wishState.enter()):
                self.m_enteredStates.append(wishState)
                self.m_data.currentState = wishState.getName()
                return True
        
        return False







