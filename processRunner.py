from concurrent.futures import process
from enum import Enum
from collections import deque

class ProcessorType(Enum):
    FCFS = 1

class ProcessRunner: 
    processes = []
    gantChart = []
    readyQueue = []
    executingProcess = None
    type = ProcessorType.FCFS

    def __init__(self,processes,type):
        self.processes = processes
        self.type = type

    def run(self):
        while self.processesCompleted() == False: 
            if self.type == ProcessorType.FCFS:
                self.fcfs()

    def fcfs(self):
        # check for ariving processes 
        for process in self.processes:
            if process.arival_time == self.getTu():
                self.readyQueue.insert(process)

        # if there is no executing process, pull first process from ready queue 
        if self.executingProcess == None: 
            queue = deque(self.readyQueue)
            self.executingProcess = queue.popleft()

        # execute process 
        if self.executingProcess == None:
            self.gantChart.append(None)
        else:
            self.gantChart.append(self.executingProcess.process_id)

        # if process finished set it to completed 
        if self.getBursts(self.executingProcess.process_id) == self.executingProcess.burst_time:
            self.executingProcess.comleted = True 
            self.executingProcess = None

    def getBursts(self, process_id):
        count = 0
        for x in self.gantChart:
            if x == process_id:
                count = count + 1 

        return count 

    def getTu(self):
        return len(self.gantChart)

    def processesCompleted(self):
        for process in self.processes:
            if process.completed == False:
                return False
        return True 
    
