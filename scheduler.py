import sys
import csv
import unittest
import test
from process import getProcesses

def print_processes(processes,type):
    print("----------------- {} --------------------".format(type).ljust(50))
    print_formatted(["Process ID |", "Waiting Time |", "Turnaround Time"])
    
    for process in processes:
        x = format_spaces(3, process.process_id) 
        y = format_spaces(6, process.waiting_time) 
        z = format_spaces(4, process.turnaround_time) 

        print(" "*6+str(process.process_id)+" "*x, end=" |")
        print(" "*6+str(process.waiting_time)+" "*y, end=" |")
        print(" "*6+str(process.turnaround_time)+" "*z, end=" ")
        print()

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

    # Call FCFS
    print_processes(processes, "FCFS")

    # Test print TODO: comment out before submitting
    print("pass finished main".upper())

    




