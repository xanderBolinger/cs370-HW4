from process import Process
from enum import Enum
from collections import deque

class ProcessorType(Enum):
    FCFS = 1

class ProcessRunner: 
    processes = []
    gantChart = []
    readyQueue = []
    executingProcess: Process = None
    processor_type = ProcessorType.FCFS

    def __init__(self,processes,type):
        self.processes = processes
        self.processor_type = type

    def run(self):

        self.gantChart = []

        while self.processesCompleted() == False: 
            if self.processor_type == ProcessorType.FCFS:
                self.fcfs()

    def fcfs(self):

        #print("Print TU: "+str(self.getTu())+", "+str(self.gantChart))

        # check for ariving processes 
        for process in self.processes:
            if process.arival_time == self.getTu():
                self.readyQueue.insert(0, process)

        # if there is no executing process, pull first process from ready queue 
        if (self.executingProcess == None or self.executingProcess.completed == True) and len(self.readyQueue) > 0: 
            self.executingProcess = self.readyQueue[0]
            self.readyQueue.remove(self.executingProcess)

        # execute process 
        self.execute_process()

        # if process finished set it to completed 
        self.complete_process()

        #print("Ready Queue Size: {}".format(len(self.readyQueue)))

    def getBursts(self, process_id):
        count = 0
        for x in self.gantChart:
            if x == process_id:
                count = count + 1 

        return count 

    def execute_process(self):
        if self.executingProcess == None:
            self.gantChart.append(None)
        else:
            #print("Append Process: {}".format(self.executingProcess.process_id))
            self.gantChart.append(self.executingProcess.process_id)

    def complete_process(self):
        if self.executingProcess != None and self.getBursts(self.executingProcess.process_id) == self.executingProcess.burst_time:
            self.executingProcess.completed = True 

    def getTu(self):
        return len(self.gantChart)

    def processesCompleted(self):
        for process in self.processes:
            if process.completed == False:
                return False
        return True 
    
