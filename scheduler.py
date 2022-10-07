import sys
import unittest

from processRunner import ProcessRunner,ProcessorType
import test
from process import getProcesses, Process
from typing import List

def print_processes(processes: List[Process],type):
    print("----------------- {} --------------------".format(type).ljust(50))
    print_formatted(["Process ID |", "Waiting Time |", "Turnaround Time"])

    processes.sort(key=lambda p: p.process_id, reverse=False)

    for process in processes:
        x = format_spaces(3, process.process_id) 
        y = format_spaces(6, process.waiting_time) 
        z = format_spaces(4, process.turn_around_time) 

        print(" "*6+str(process.process_id)+" "*x, end=" |")
        print(" "*6+str(process.waiting_time)+" "*y, end=" |")
        print(" "*6+str(process.turn_around_time)+" "*z, end=" ")
        print()

def print_gant_chart(processRunner: ProcessRunner):
    print("Gant Chart is:")
    process_start_time = 0
    active_process = None
    for i in range(len(processRunner.gant_chart)):
        if active_process == None: 
            active_process = processRunner.gant_chart[i]
            process_start_time = i
        elif processRunner.gant_chart[i] != active_process:
            print("[{} - {}] Process {}".format(process_start_time, i, active_process))
            active_process = processRunner.gant_chart[i]
            process_start_time = i
        elif(i == len(processRunner.gant_chart) - 1):
            print("[{} - {}] Process {}".format(process_start_time, i+1, active_process))

        
def print_averages(processRunner: ProcessRunner):
    print("Average Waiting Time: "+str(processRunner.average_wt()))
    print("Average Turnaround Time: "+str(processRunner.average_ttt()))
    print("Throughput: "+str(processRunner.throughput()))

def format_spaces(spaces, value):
    if value != 0 and len(str(value)) > 1:
        spaces = spaces - ( len(str(value)) - 1 )
    return spaces

def print_formatted(list):    
    for elem in list:
        print(f"{elem: >8}", end=" ")
    print("\n")

if __name__ == "__main__":

    # Check valid number of arguments 
    if len(sys.argv) != 3:
        print("Invalid number of argumnets.")
        exit(1)
    
    # Test cases TODO: comment out before submitting
    suite = unittest.TestLoader().loadTestsFromModule(test)
    unittest.TextTestRunner(verbosity=2).run(suite)

    # Get process objects 
    processes = getProcesses(sys.argv[1])

    processRunner = ProcessRunner(processes,ProcessorType.FCFS)
    processRunner.run()

    # Call FCFS
    print_processes(processRunner.processes, "FCFS")
    print()

    print_gant_chart(processRunner)

    print()
    print_averages(processRunner)

    # Test print TODO: comment out before submitting
    print("pass finished main".upper())

    




