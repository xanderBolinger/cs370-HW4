File Descriptions: 
process contains the process object used in the processRunner 
processRunner contains the logic for the cpu scheduling 
shceduler contains the main method of the program and configures the process scheduling,
shceduler also handles printing resutls to the user

1. Is the Shortest Remaining Time First a non-preemptive Algorithm? 
no, the idea behind srtf is that you can prempt the current process to perform a shorter newly arived process. 
2. What are the 5 different states a process can be in scheduling (Look into process state
diagram)?  
new, ready, running, exit, blocked.
3. Shortest Job First is like Priority Scheduling with the priority based on ______ of the process? 
the burst time
4. ________ effect is the primary disadvantage of First Come First Serve Scheduling algorithm. 
Long waiting time.
5. How does Multi Level Feedback queue prevent starvation of processes that waits too long in
lower priority queue
Starvation is prevented by moving processes down in priority if they are using excessive amounts of cpu time, 
conversly low priority processes that spend too much time in the queue are moved up in priority