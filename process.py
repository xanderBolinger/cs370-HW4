import csv

class Process: 
    process_id = 0
    arival_time = 0
    burst_time = 0
    priority = 0
    waiting_time = 0
    turnaround_time = 0
    completed = False

    def __init__(self,process_id, arival_time, burst_time,priority):
        self.process_id = int(process_id)
        self.arival_time = int(arival_time)
        self.burst_time = int(burst_time)
        self.priority = int(priority)
    
def getProcesses(file_name):
    processes = []
    with open(file_name) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            processes.append(Process(row[0], row[1], row[2], row[3]))
    
    return processes