
from core.Logger import Logger

class NSLazyGameScriptor:

    def __init__(self) -> None:
        pass

if __name__ == '__main__':

    running = True

    print('NS Lazy script')

    while running:

        cmd = input('>')

        if cmd == 'help':
            pass
        else:
            Logger.warn('未知的命令')
