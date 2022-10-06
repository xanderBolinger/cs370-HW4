import unittest
from process import Process, getProcesses
from processRunner import ProcessRunner, ProcessorType

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

    def test_processor_methods(self):
        pass

    def test_processor_run(self):
        print("TEST PROCESSOR")
        processes: list[Process] = getProcesses("processinfo.csv")
        processor = ProcessRunner(processes, ProcessorType.FCFS)
        self.assertEqual(len(processor.processes), 4)
        self.assertEqual(processor.type, ProcessorType.FCFS)

        processor.executingProcess = processes[0]
        for x in range(processes[0].burst_time):
            processor.gantChart.append(processes[0].process_id)

        self.assertEqual(processor.getBursts(processes[0].process_id), processes[0].burst_time)

        processor.complete_process()

        self.assertEqual(processor.executingProcess.completed, True)
        self.assertEqual(processor.executingProcess.completed, processes[0].completed)

        processor.executingProcess = processes[1]

        for x in range(processes[1].burst_time):
            processor.execute_process()

        gantChart = []
        for i in range(3):
            gantChart.append(processes[0].process_id)
        
        for i in range(5):
            gantChart.append(processes[1].process_id)

        gantChart.append(None)

        for i in range(8):
            gantChart.append(processes[2].process_id)
        
        for i in range(6):
            gantChart.append(processes[3].process_id)
        
        # processor.run()

        # self.assertEqual(len(processor.gantChart), len(gantChart))




        
if __name__ == '__main__':
    unittest.main()
    
    