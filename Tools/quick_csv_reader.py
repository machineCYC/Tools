import csv
import datetime as dt
import json
import os
import queue
import re
import threading
import time

import pandas as pd
from loguru import logger


#=====================================================================================#
#Job Class. It's  responsibility is  read and pre-processing data
#=====================================================================================#
class Worker:
    def __init__(self, filepath, lock, csv_sep=",", patterns=[]):
        self.filepath = filepath
        self.lock = lock
        self.csv_sep = csv_sep
        self.patterns = patterns
        self.ThdId = 0
        self.logger = logger
        self._is_legal_file = True
        self._filename = os.path.abspath(filepath)


    def setThdId(self,ThdId):
        self.setThdId = ThdId


    def _valid_file(self):
        if self.patterns:
            bool_pattern_match = []
            for p in patterns:
                pattern_match = re.search(p, self._filename)
                if bool(pattern_match):
                    break
            else:
                self.is_legal_file = False


    def process_data(self):
        pass


    def do(self):
        global RawData
        _ = self._valid_file()

        if self.is_legal_file:
            self.logger.info("file:{0} reading...".format(self.filepath))
            try:
                self.RawData= pd.read_csv(self.filepath, sep=self.csv_sep, low_memory=False, quoting=csv.QUOTE_NONE)
            except UnicodeDecodeError:
                self.logger.error("read csv file:{0} fail!...".format(self.filepath))
            except KeyError:
                self.logger.error("read csv file:{0} fail!...".format(self.filepath))

            _ = self.process_data()

            self.logger.info("file:{0} prepare acquire lock...".format(self.filepath))

            st = dt.datetime.now()
            self.lock.acquire()
            RawData = RawData.append(self.RawData) # 不能同時讓多個 thread 進行
            self.lock.release()
            td = dt.datetime.now() - st
            self.logger.debug("file:{0} release lock...Spending time={1}!".format(self.filepath,td))


#===============================================================================
# thread target function, 檢查queue中是否還有工作需處理
#===============================================================================
def ConsumeQueue(*args):
    queue = args[0]
    lock = args[1]
    ThdId = args[2]

    while True:
        lock.acquire()
        if queue.qsize() >0:
            job = queue.get()
            lock.release()
            job.setThdId(ThdId)
            job.do()
        else:
            lock.release()
            break


def launchThreads(que, queLock, num):
    thd = list()
    for i in range(num+1):
        thd_obj = threading.Thread(target=ConsumeQueue, name='Thd'+str(i), args=(que,queLock,i))
        thd_obj.start()
        thd.append(thd_obj)

    for i in range(num+1):
        while thd[i].is_alive():
            time.sleep(5)
    del thd
    return


def CombineData(process_worker, wd, thread_number):
    '''
    :process_worker: process data worker
    :param wd: working directory
    :thread_number: setting thread number
    :return: None
    '''
    global RawData

    #=================================================================================#
    #Queue for keep threads' job & Plot instance
    #=================================================================================#
    que = queue.Queue()
    #=================================================================================#
    #Lock for avoid data be compromised
    #=================================================================================#
    dfLock = threading.Lock()
    queLock = threading.Lock()

    RawData = pd.DataFrame({})

    for response in os.walk(wd):
        for filepath in response[2]:
            file_loc = wd+'/'+ filepath
            que.put(process_worker(file_loc, dfLock))

    launchThreads(que, queLock, thread_number)

    return RawData
