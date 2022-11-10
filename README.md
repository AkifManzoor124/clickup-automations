# clickup-automations

1. An alternative to Motion for Clickup where tasks are scheduled/rescheduled based on avaliability,time estimate and priority

// retrieve all the tasks which are already scheduled (first iteration) <br> 
// retrieve all tasks which are overdue || empty(start date && due date) <br> 
// retrieve all times where assignee is avaliable within calendar <br> 
// run an algorithm to schedule the high priority items before the low priority <br> 

Task has to be assigned to you <br> 
Task needs to have a time estimate <br> 
Task must be within specified list/s <br> 
Task optionally needs a priority <br> 

The tool aims to automatically schedule/reschedule tasks start/due date based on openings within assignee's calendar <br> 


Zero Iteration: Scheduling without recurring tasks
First Iteration: I can start with just scheduling tasks within a timeframe of 2 week <br> 
Second Iteration: Custom timeframe <br> 
Third Iteration: combinations of start date && due date <br> 
 
features: shortest day <br> 
features: maximum tasks per day <br> 
features: minimum/maximum number of pomodoro sessions <br> 
features: associate tasks with pomodoros <br> 
features: change the list based on the current sprint automatically <br>



I am trying to retrieve all tasks within the sprint folder, and schedule them to all avaliable times before the end of the sprint
The last time will be sunday at 11:59pm
depending on the priority and time estimate of the task, it will be scheduled to the earliest avaliable time
I will have to consider the rituals list to find blocks of time which are already scheduled