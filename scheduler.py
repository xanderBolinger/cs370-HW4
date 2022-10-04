import sys
import csv
import unittest
import test
from process import getProcesses

def print_processes(processes,type):
    print("----------------- {} -----------------".format(type))
    print("Process ID | Waiting Time | Turnaround Time".rjust(50))

if __name__ == "__main__":
    # print('Number of arguments:', len(sys.argv), 'arguments.')
    # print('Argument List:', str(sys.argv))

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

    




