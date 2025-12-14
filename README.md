README - Performance Modelling and Simulation of Dambulla Economic Centre.
==========================================================================
Overview
------------------
This project provides data-scale discrete-time simulation of the unloading dock activities in the Dambulla Economic Centre, Sri Lanka. The simulation analyses the performance of the systems during peak-hours and compares three operating conditions to determine the congestion, bottlenecks and possible improvements.

Python and Simpy are used to develop the model, which is supported with visual analytics in Matplotlib.

System Description
------------------
The model system is a replica of the 30-dock area of the Dambulla Economic Centre in which the mean number of active docks is 26 during the rush hours. These farmers come with harvest to be unloaded, weighed and processed. Queues are formed during the rush hours because of the low unloading power and the rate of arrival.

Simulated Scenarios
-------------------
Three stages are tested in the simulation:

Baseline Scenario
-------------------
2 workers per dock

Arrival and service time obtained based on actual field data.

Indicates the present operating conditions.

More Staff Scenario
-------------------
4 workers per dock

Reduced service time because of greater manpower.

Tests the effect of capacity of services.

Arrival Smoothing Scenario
--------------------------
Regulated intervals of arrival.

Equal staffing and time of service compared to the baseline.

Determines the reduction of congestion without extra personnel.

Performance Metrics
--------------------
The indicators are the following key performance measurements that are measured and reported:

Mean waiting time (minutes)

Mean queue time (number of farmers)

System throughput (farmers per minute)

Dock utilization (%)

The simulation of each scenario is done several times and the average outcomes are given, to enhance statistical reliability.

Visualization Outputs
----------------------
The code creates a number of visualizations in order to facilitate analysis and interpretation:

Comparative bar chart of all the key performance measures.

Pie chart of relative contribution towards total waiting time.

Bar chart of dock use in different cases.

Time-series plot of variation of lengths of queues during the operating period.

These visualizations are useful in elucidating congestion, trade-offs in performance and system stability.

How to Run the Code
------------------------
1. Make sure that Python is installed with the following libraries:
            simpy
            matplotlib
            numpy
2. The simulation script will be run to produce numerical results concerning performance.
3. Run the visualisation parts to generate graphs (suggested in Jupyter Notebook).
4. Make use of the resulting outputs and figures, report or present.

Key Insights
--------------
The peak hours are characterized by serious congestion of the baseline system.

High staffing levels have a great impact in reducing waiting time and queue length as well as increasing throughput.

Arrival smoothing is a moderate solution that does not require the extra staff.

The behavior and stability of a system as seen through visual analysis is not easily apparent using average measures.

Notes
--------------
The model is tuned with a small amount of real-life data whose samples are limited to four days in the frame.

There are external influencing factors like road congestion and parking delay.

The framework of the simulation could be expanded to represent bigger areas or further working policies.

Intended Use
---------------
The project will be applied to the performance of academic performance modelling, system evaluation and decision support analysis concerning market logistics and service systems.
