# 381k_project
Code to simulate a hierarchy of experts for task completion

Variables of interest:

K (defined globally) - the number of levels in the hierarchy.
Initial simulations show that packets don't go past level 7 or 8, but that may be dependent on the choice of N and p_def (defined later). If you're changing this parameter, you will also need to change N and p_def.

The following variables are defined in main() - 

step - the time steps at which the simulation calculates arrivals and departures. Don't change this unless lam * step > 1, in which case, decrease step. Decreasing step will increase simulation time.

T - the time in seconds for which the simulation is set to run. Total loop iterations are hence T/step. Don't change this unless the queues aren't converging to their stationary distribution, in which case increase T.

N - array with number of experts (servers) per level.

p_def - the array of probabilities of deferral of a task by an expert in a level. Essentially, a task is serviced, and then leaves the system with probability 1-p_def, and stays with probability p_def, in which case it has to be put into the same queue or the next queue. 

rate - rates of service at every level. I've assumed constant unit rates, but these could be made level-specific.

lam - rate of arrival of tasks/packets into level 1.

I plot all queue lengths as the output of the system. Other quantities of interest could be mean queue length, etc.

RESULTS:

Our "backpressure" algorithm definitely increases the stability region. Here we define stability as ALL queues having a stationary distribution/being positive recurrent. 

TODO: Characterize improvement in stability region. See how different "topologies" of experts impacts things. 

PLEASE ADD IDEAS.

kthxbye
