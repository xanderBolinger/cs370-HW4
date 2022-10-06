from process import Process
from enum import Enum
from collections import deque

class ProcessorType(Enum):
    FCFS = 1

class ProcessRunner: 
    processes: Process = []
    gantChart = []
    readyQueue = []
    executingProcess: Process = None
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
                self.readyQueue.insert(0, process)

        # if there is no executing process, pull first process from ready queue 
        if self.executingProcess == None or self.executingProcess.completed == True: 
            queue = deque(self.readyQueue)
            self.executingProcess = queue.popleft()

        # execute process 
        self.execute_process()

        # if process finished set it to completed 
        self.complete_process()

    def getBursts(self, process_id):
        count = 0
        for x in self.gantChart:
            if x == process_id:
                count = count + 1 

        return count 

    def complete_process(self):
        if self.getBursts(self.executingProcess.process_id) == self.executingProcess.burst_time:
            self.executingProcess.completed = True 

    def execute_process(self):
        if self.executingProcess == None:
            self.gantChart.append(None)
        else:
            self.gantChart.append(self.executingProcess.process_id)

    def getTu(self):
        return len(self.gantChart)

    def processesCompleted(self):
        for process in self.processes:
            if process.completed == False:
                return False
        return True 
    
