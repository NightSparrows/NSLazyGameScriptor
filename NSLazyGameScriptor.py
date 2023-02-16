
import datetime

from core.Logger import Logger

from game.fgo.GameFGO import GameFGO

class NSLazyGameScriptor:

    def __init__(self) -> None:
        self.m_running = False

        self.m_games = []

        fgoGame = GameFGO()


    def cmdHelp(self):
        print('NS Lazy script')



        print(
            f"{'命令':<10}{'解釋'}",'\n',
            f"{'help':<10}{'顯示此help'}",'\n',
            f"{'quit':<10}{'結束NS lazy game scriptor'}",'\n',
        )


    def run(self):
        print('NS Lazy script')

        # init games

        self.m_running = True
        while self.m_running:

            cmd = input('>')

            if cmd == 'help' or cmd == 'h':
                self.cmdHelp()
            elif cmd == 'quit' or cmd == 'q':
                self.m_running = False
            else:
                Logger.warn('未知的命令')

if __name__ == '__main__':



    script = NSLazyGameScriptor()

    script.run()
