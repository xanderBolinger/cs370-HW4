from process import Process
from enum import Enum
from typing import List
class ProcessorType(Enum):
    FCFS = 1

class ProcessRunner: 
    processes: List[Process] = []
    gant_chart = []
    ready_queue = []
    executing_process: Process = None
    processor_type = ProcessorType.FCFS

    def __init__(self,processes,type):
        self.processes = processes
        self.processor_type = type

    def run(self):

        self.gant_chart = []

        while self.processes_completed() == False: 
            if self.processor_type == ProcessorType.FCFS:
                self.fcfs()
        
        for process in self.processes:
            process.turn_around_time = process.completion_time - process.arival_time
            process.waiting_time = process.turn_around_time - process.burst_time

    def fcfs(self):

        #print("Print TU: "+str(self.getTu())+", "+str(self.gantChart))

        # check for ariving processes 
        for process in self.processes:
            if process.arival_time == self.get_tu():
                self.ready_queue.insert(0, process)

        # if there is no executing process, pull first process from ready queue 
        if (self.executing_process == None or self.executing_process.completed == True) and len(self.ready_queue) > 0: 
            self.executing_process = self.ready_queue[0]
            self.ready_queue.remove(self.executing_process)
            self.executing_process.response_time = len(self.gant_chart) - self.executing_process.arival_time

        # execute process 
        self.execute_process()

        # if process finished set it to completed 
        self.complete_process()

        #print("Ready Queue Size: {}".format(len(self.readyQueue)))

    def getBursts(self, process_id):
        count = 0
        for x in self.gant_chart:
            if x == process_id:
                count = count + 1 

        return count 

    def execute_process(self):
        if self.executing_process == None:
            self.gant_chart.append("IDLE")
        else:
            #print("Append Process: {}".format(self.executingProcess.process_id))
            self.gant_chart.append(self.executing_process.process_id)

    def complete_process(self):
        if self.executing_process != None and self.getBursts(self.executing_process.process_id) == self.executing_process.burst_time:
            self.executing_process.completed = True 
            self.executing_process.completion_time = len(self.gant_chart)
            self.executing_process = None

    def get_tu(self):
        return len(self.gant_chart)

    def processes_completed(self):
        for process in self.processes:
            if process.completed == False:
                return False
        return True 
    
    def average_ttt(self):
        sum = 0
        for process in self.processes:
            sum = sum + process.turn_around_time
        
        return sum / len(self.processes)

    def average_wt(self):
        sum = 0
        for process in self.processes:
            sum = sum + process.waiting_time
        
        return sum / len(self.processes)

    def throughput(self):
        sum = 0
        for process in self.processes:
            sum = sum + process.response_time
        
        return sum / len(self.processes) / len(self.gant_chart)