from technical import Indicator
import threading
import multiprocessing

from database import DataBase

class Current() :

    def current():
        pass


class BackTest():
    def backTest():
        pass


if __name__ == '__main__':
    
    multiprocessing.Process(target=BackTest().backTest).start()
    Current().current()
