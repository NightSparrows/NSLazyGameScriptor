

class Task:

    def __init__(self, name: str) -> None:
        self.m_name = name
        pass

    def execute(self):
        raise NotImplementedError('Task ' + self.m_name + ' not impl.')
