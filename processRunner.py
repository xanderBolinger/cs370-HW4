from process import Process
from enum import Enum
from typing import List
class ProcessorType(Enum):
    FCFS = 1
    RR = 2

class ProcessRunner: 
    processes: List[Process] = []
    gant_chart = []
    ready_queue = []
    executing_process: Process = None
    processor_type = ProcessorType.FCFS
    time_quantum = 0

    def __init__(self,processes,type, time_quantum=0):
        self.processes = processes
        self.processor_type = type
        self.time_quantum = time_quantum

    def run(self):

        self.gant_chart = []

        count = 0
        while self.processes_completed() == False and count < 50: 
            if self.processor_type == ProcessorType.FCFS:
                self.fcfs()
            elif self.processor_type == ProcessorType.RR:
                self.rr()

            count = count + 1 

        for process in self.processes:
            process.turn_around_time = process.completion_time - process.arival_time
            process.waiting_time = process.turn_around_time - process.burst_time

    def rr(self):

        # check for ariving processes
        self.ariving_processes()

        # if there is no executing prcess, pull first process from ready queue 
        self.set_process()

        # for each time quantum 
        for _ in range(self.time_quantum):

             # check for ariving processes
            self.ariving_processes()

            # if process completed 
            if self.executing_process == None:
                break 

            # TODO: check for when the processor is actually idle, or give complete process a return value for it it comlpeted an active process

            self.execute_process()
            self.complete_process()
            print("Time Unit: {}".format(len(self.gant_chart)))
        
        # if executing process is not none, set to none and append process back to the ready queue
        if self.executing_process != None: 
            process = self.executing_process
            self.ready_queue.append(process)
            self.executing_process = None
            print("return to ready queue: {}".format(process.process_id))

        print("Ready Queue Size: {}".format(len(self.ready_queue)))


    def fcfs(self):

        #print("Print TU: "+str(self.getTu())+", "+str(self.gantChart))

        # check for ariving processes 
        self.ariving_processes()

        # if there is no executing process, pull first process from ready queue 
        self.set_process()

        # execute process 
        self.execute_process()

        # if process finished set it to completed 
        self.complete_process()

        #print("Ready Queue Size: {}".format(len(self.readyQueue)))

    def ariving_processes(self, append=False):
        for process in self.processes:
            if (process.arival_time == self.get_tu() 
                and process.completed == False 
                and process not in self.ready_queue 
                and process != self.executing_process
                ):

                if append == False:
                    self.ready_queue.insert(0, process)
                else:
                    self.ready_queue.append(process)
                print("Ariving Process: {}".format(process.process_id))

    def set_process(self):
        if (self.executing_process == None or self.executing_process.completed == True) and len(self.ready_queue) > 0: 
            self.executing_process = self.ready_queue[0]
            print("Set Process: {}".format(self.executing_process.process_id))
            self.ready_queue.remove(self.executing_process)
            self.executing_process.response_time = len(self.gant_chart) - self.executing_process.arival_time

    def getBursts(self, process_id):
        count = 0
        for x in self.gant_chart:
            if x == process_id:
                count = count + 1 

        return count 

    def execute_process(self):
        if self.executing_process == None:
            self.gant_chart.append("IDLE")
            print("Execute Process IDLE")
        else:
            print("Execute Process: {}".format(self.executing_process.process_id))
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