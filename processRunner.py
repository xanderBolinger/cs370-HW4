from concurrent.futures import process
from process import Process
from enum import Enum
from typing import List
import sys

# enum to handle type of cpu shceduling being used 
class ProcessorType(Enum):
    FCFS = 1
    RR = 2
    PS = 3

# class that handles cpu scheduling 
class ProcessRunner: 
    processes: List[Process] = []
    gant_chart = []
    ready_queue: List[Process] = []
    executing_process: Process = None
    processor_type = ProcessorType.FCFS
    time_quantum = 2

    def __init__(self,processes, type, time_quantum=2):
        self.processes = processes
        self.processor_type = type
        self.time_quantum = time_quantum


        processes.sort(key=lambda x: x.process_id, reverse=True)

    # triggers cpu scheduling 
    # builds gant chart and completes all processes 
    # calculates the completiong time, arival time, and turn around time of each process
    def run(self):

        self.gant_chart = []

        while self.processes_completed() == False: 
            if self.processor_type == ProcessorType.FCFS:
                self.fcfs()
            elif self.processor_type == ProcessorType.RR:
                self.rr()
            elif self.processor_type == ProcessorType.PS:
                self.ps()

        for process in self.processes:
            process.turn_around_time = process.completion_time - process.arival_time
            process.waiting_time = process.turn_around_time - process.burst_time

    # called to initiate round robin scheduling
    def rr(self):

        # check for ariving processes
        self.ariving_processes()
        
        self.save_ready_queue()

        # if there is no executing prcess, pull first process from ready queue 
        self.set_process()

        # if executing process is not none, 
        # set to none and append process back to the ready queue
        if self.executing_process != None: 
            process = self.executing_process
            process_completed = False 
            # for each time quantum 
            for _ in range(self.time_quantum):
                self.execute_process()
                # if process completed 
                if self.complete_process():
                    process_completed = True
                    break
                # print("Time Unit: {}".format(len(self.gant_chart)))

            if process_completed == False:
                self.ready_queue.append(process)
                self.executing_process = None 

            # print("return to ready queue: {}".format(process.process_id))
        else: 
            # add idle 
            self.execute_process()

        # print("Ready Queue Size: {}".format(len(self.ready_queue)))

    # called to initiate first come first serve scheduling
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

    # called to activate priority scheduling 
    def ps(self):

        #print("Print TU: "+str(self.getTu())+", "+str(self.gantChart))

        # check for ariving processes 
        self.ariving_processes()

        # if there is no executing process, pull first process from ready queue 
        self.set_process_priority()

        # If there is no active process this time unit, set process to idle 
        if self.executing_process == None:
            self.gant_chart.append("IDLE")
            # print("Execute Process IDLE")
            return 

        # execute process 
        while self.executing_process != None:
            self.execute_process()
            # if process finished set it to completed 
            self.complete_process()
        
    
    # checks if processes have arived this time unit 
    # if they have, inserts them to the ready queue 
    # after submission append is never used, it was only used during testing
    def ariving_processes(self, append=False):
        for process in self.processes:
            if (process.arival_time <= self.get_tu() 
                and process.completed == False 
                and process not in self.ready_queue 
                and process != self.executing_process
                ):

                if append == False:
                    self.ready_queue.insert(0, process)
                else:
                    self.ready_queue.append(process)
        
        
                # print("Ariving Process: {}".format(process.process_id))

    # version of set process method used during priority scheduling
    # If there is no executing process, picks highest priority process from the ready queue 
    # if two processes match in priority chooses the process with the lower pid to execute first
    def set_process_priority(self):
        if(self.executing_process != None and self.executing_process.completed != True):
            return 
        
        if len(self.ready_queue) > 1:
            lowest_burst_time: Process = self.ready_queue[0]
            for process in self.ready_queue:
                if process.burst_time < lowest_burst_time.burst_time:
                    lowest_burst_time = process

            for process in self.ready_queue:
                if process == lowest_burst_time:
                    continue 
                if process.burst_time == lowest_burst_time.burst_time:
                    if process.priority < lowest_burst_time.priority:
                        lowest_burst_time = process 
                    elif process.priority == lowest_burst_time.priority and process.process_id < lowest_burst_time.process_id:
                        lowest_burst_time = process

            self.executing_process = lowest_burst_time
            # print("Set Process: {}".format(self.executing_process.process_id))
            self.ready_queue.remove(self.executing_process)
        elif len(self.ready_queue) > 0:
                self.set_process()

    # when there is no process being executed, sets the process to the first process in hte ready queue 
    def set_process(self):
        if (self.executing_process == None or self.executing_process.completed == True) and len(self.ready_queue) > 0: 
            self.executing_process = self.ready_queue[0]
            # print("Set Process: {}".format(self.executing_process.process_id))
            self.ready_queue.remove(self.executing_process)
            self.executing_process.response_time = len(self.gant_chart) - self.executing_process.arival_time

    # gets the number of bursts/time units a process of process_id has executed for 
    def getBursts(self, process_id):
        count = 0
        for x in self.gant_chart:
            if x == process_id:
                count = count + 1 

        return count 

    # executes the executing process, or adds IDLE if there is no executing process 
    def execute_process(self):
        if self.executing_process == None:
            self.gant_chart.append("IDLE")
            # print("Execute Process IDLE")
        else:
            # print("Execute Process: {}".format(self.executing_process.process_id))
            self.gant_chart.append(self.executing_process.process_id)

    # checks if the executing process has been completed
    def complete_process(self):
        if self.executing_process != None and self.getBursts(self.executing_process.process_id) == self.executing_process.burst_time:
            self.executing_process.completed = True 
            self.executing_process.completion_time = len(self.gant_chart)
            self.executing_process = None
            return True
        return False 

    # returns the current time unit
    def get_tu(self):
        return len(self.gant_chart)

    # checks if all processes have been completed
    def processes_completed(self):
        for process in self.processes:
            if process.completed == False:
                return False
        return True 
    

    # returns average turn around time 
    def average_ttt(self):
        sum = 0
        for process in self.processes:
            sum = sum + process.turn_around_time
        
        return sum / len(self.processes)

    # refurns average wait time 
    def average_wt(self):
        sum = 0
        for process in self.processes:
            sum = sum + process.waiting_time
        
        return sum / len(self.processes)

    # returns the max completion time 
    def max_ct(self):
        max = -sys.maxsize - 1

        for process in self.processes:
            if process.completion_time > max: 
                max = process.completion_time
        
        return max
    
    # returns the minimum arival time 
    def min_at(self):
        min = sys.maxsize

        for process in self.processes:
            if process.arival_time < min:
                min = process.arival_time

        return min

    # returns throughput 
    def throughput(self):
        return len(self.processes) / (self.max_ct()) - (self.min_at())

    # prints the current state of the ready queue for round robin scheduling 
    def save_ready_queue(self):
        
        ready_queue = []
        for process in self.ready_queue:
            ready_queue.append(process.process_id)
        
        print("{}".format(ready_queue))
        
    # returns the process of pid equal to process_number
    def get_process(self, process_number):
        for process in self.processes:
            if process.process_id == process_number:
                return process
        return None
