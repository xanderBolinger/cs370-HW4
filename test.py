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
        processes: list[Process] = getProcesses("processinfo.csv")
        processor = ProcessRunner(processes, ProcessorType.FCFS)
        self.assertEqual(len(processor.processes), 4)
        self.assertEqual(processor.processor_type, ProcessorType.FCFS)

        processor.executing_process = processes[0]
        for x in range(processes[0].burst_time):
            processor.gant_chart.append(processes[0].process_id)

        self.assertEqual(processor.getBursts(processes[0].process_id), processes[0].burst_time)

        processor.complete_process()

        self.assertEqual(processes[0].completed, True)
        self.assertEqual(processes[0].completed, processes[0].completed)

        processor.executing_process = processes[1]

        for x in range(processes[1].burst_time):
            processor.execute_process()

        processor.complete_process()

        self.assertEqual(processes[1].completed, True)
        self.assertEqual(processes[1].completed, processes[1].completed)

        processes[2].completed = True 
        processes[3].completed = True 

        self.assertEqual(processor.processes_completed(), True)

    def test_processor_run(self):
        print("TEST PROCESSOR")
        processes: list[Process] = getProcesses("processinfo.csv")
        processor = ProcessRunner(processes, ProcessorType.FCFS)
        
        processor.run()

        print("PROCESSOR GANT CHART: "+str(processor.gant_chart))

        self.assertEqual(processor.processes[0].completion_time, 8)
        self.assertEqual(processor.processes[0].turn_around_time, 8)
        self.assertEqual(processor.processes[0].waiting_time, 5)

        self.assertEqual(processor.processes[1].completion_time, 5)
        self.assertEqual(processor.processes[1].turn_around_time, 5)
        self.assertEqual(processor.processes[1].waiting_time, 0)
        
        self.assertEqual(processor.processes[2].completion_time, 17)
        self.assertEqual(processor.processes[2].turn_around_time, 8)
        self.assertEqual(processor.processes[2].waiting_time, 0)

        self.assertEqual(processor.processes[3].completion_time, 23)
        self.assertEqual(processor.processes[3].turn_around_time, 13)
        self.assertEqual(processor.processes[3].waiting_time, 7)

        self.assertEqual(len(processor.gant_chart), 23)


    def test_rr(self):
        processes: list[Process] = getProcesses("processinfo.csv")
        processor = ProcessRunner(processes, ProcessorType.RR, 2)
        
        processor.run()

        print("PROCESSOR RR GANT CHART: "+str(processor.gant_chart))

        # pid 3
        self.assertEqual(processor.processes[0].completion_time, 7)
        self.assertEqual(processor.processes[0].turn_around_time, 7)
        self.assertEqual(processor.processes[0].waiting_time, 4)

        # pid 2
        self.assertEqual(processor.processes[1].completion_time, 8)
        self.assertEqual(processor.processes[1].turn_around_time, 8)
        self.assertEqual(processor.processes[1].waiting_time, 3)
        
        # pid 1
        self.assertEqual(processor.processes[2].completion_time, 23)
        self.assertEqual(processor.processes[2].turn_around_time, 14)
        self.assertEqual(processor.processes[2].waiting_time, 6)

        # pid 4
        self.assertEqual(processor.processes[3].completion_time, 21)
        self.assertEqual(processor.processes[3].turn_around_time, 11)
        self.assertEqual(processor.processes[3].waiting_time, 5)

        self.assertEqual(len(processor.gant_chart), 23)

    def test_ps(self):
        processes: list[Process] = getProcesses("processinfo.csv")
        processor = ProcessRunner(processes, ProcessorType.PS)
        
        processor.run()

        print("PROCESSOR PS GANT CHART: "+str(processor.gant_chart))

        # pid 1
        self.assertEqual(processor.processes[2].completion_time, 17)
        self.assertEqual(processor.processes[2].turn_around_time, 8)
        self.assertEqual(processor.processes[2].waiting_time, 0)

        # pid 2
        self.assertEqual(processor.processes[1].completion_time, 8)
        self.assertEqual(processor.processes[1].turn_around_time, 8)
        self.assertEqual(processor.processes[1].waiting_time, 3)

        # pid 3
        self.assertEqual(processor.processes[0].completion_time, 3)
        self.assertEqual(processor.processes[0].turn_around_time, 3)
        self.assertEqual(processor.processes[0].waiting_time, 0)
        
        # pid 4
        self.assertEqual(processor.processes[3].completion_time, 23)
        self.assertEqual(processor.processes[3].turn_around_time, 13)
        self.assertEqual(processor.processes[3].waiting_time, 7)

        self.assertEqual(len(processor.gant_chart), 23)

    def test_fcfs_2(self):
        processes: list[Process] = getProcesses("processinfotest.csv")
        processor = ProcessRunner(processes, ProcessorType.FCFS)
        
        processor.run()
        print("PROCESSOR FCFS 2 GANT CHART: "+str(processor.gant_chart))
        # pid 1
        self.assertEqual(processor.processes[0].completion_time, 10)
        self.assertEqual(processor.processes[0].turn_around_time, 10)
        self.assertEqual(processor.processes[0].waiting_time, 0)

        # pid 2
        self.assertEqual(processor.processes[1].completion_time, 15)
        self.assertEqual(processor.processes[1].turn_around_time, 15)
        self.assertEqual(processor.processes[1].waiting_time, 10)

        # pid 3
        self.assertEqual(processor.processes[2].completion_time, 23)
        self.assertEqual(processor.processes[2].turn_around_time, 23)
        self.assertEqual(processor.processes[2].waiting_time, 15)

        self.assertEqual(processor.average_wt(),8+(1.0/3.0))
        self.assertEqual(processor.average_ttt(),16)

if __name__ == '__main__':
    unittest.main()
    
    