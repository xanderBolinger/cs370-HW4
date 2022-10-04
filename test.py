import unittest
from process import Process, getProcesses


class TestCases(unittest.TestCase):
    def test_process(self):
        process = Process(1,2,3,4)
        self.assertEqual(process.process_id, 1)
        self.assertEqual(process.arival_time, 2)
        self.assertEqual(process.burst_time, 3)
        self.assertEqual(process.priority, 4)

    def test_get_processes(self):

        processes = getProcesses("processinfo.csv")
        print("\nBEGIN TEST GET PROCESSES: ")
        for process in processes:    
            print("Process ID: {}, Process Arival Time: {}, Process Burst Time: {}, Process Priority: {}"
                .format(process.process_id, process.arival_time, process.burst_time, process.priority))
                
        self.assertEqual(processes[0].process_id, 3)
        self.assertEqual(processes[0].arival_time, 0)
        self.assertEqual(processes[0].burst_time, 3)
        self.assertEqual(processes[0].priority, 2)

        self.assertEqual(processes[1].process_id, 2)
        self.assertEqual(processes[1].arival_time, 0)
        self.assertEqual(processes[1].burst_time, 5)
        self.assertEqual(processes[1].priority, 4)

        self.assertEqual(processes[2].process_id, 1)
        self.assertEqual(processes[2].arival_time, 9)
        self.assertEqual(processes[2].burst_time, 8)
        self.assertEqual(processes[2].priority, 1)

        self.assertEqual(processes[3].process_id, 4)
        self.assertEqual(processes[3].arival_time, 10)
        self.assertEqual(processes[3].burst_time, 6)
        self.assertEqual(processes[3].priority, 3)

        
        print("FINISHED TEST GET PROCESSES: ")

if __name__ == '__main__':
    unittest.main()
    
    