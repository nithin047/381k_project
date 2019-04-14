#Simulating a hierarchical system of crowdsourcing (via experts) queues and possible routing strategies
#381K project
#Nithin Ramesan, Nihal Sharma, Manan Gupta, Akash Doshi

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rn
import time
import copy
from random import shuffle
from progress.bar import Bar

start_time = time.time()

#packet information is stored as [size, residual work]

#global definitions - model parameters
K = 10 #number of levels in the hierarchy

def initial_conditions(grid, length):

	for ii in range(K):
		a = []
		grid.append(a)
		b = []
		b.append(0)
		length.append(b)

	return grid, length

def check_variables(N, p_def):

	if(len(N) != K):
		raise Exception('The length of array N is wrong!')

	if(len(p_def) != K):
		raise Exception('The length of array p_def is wrong!')

	for ii in range(K-1):

		if(N[ii]<N[ii+1]):
			raise Exception('N is not a decreasing array!')

	for ii in range(K-1):

		if (p_def[ii] < p_def[ii+1]):
			raise Exception('p_def is not a decreasing array!')

def level_decision(grid, length, N, p_def, rate, ii):

	length_list = length[ii].copy()
	state_list = grid[ii].copy()

	#"backpressure"
	var = (length_list[-1] * (1 + p_def[ii])) / (N[ii] * rate[ii]) 

	#random routing - re-route with p=0.5, and push forward with p=0.5
	#var = rn.uniform()

	return var

def arrival(grid, length, lam_array, step):

	for ii in range(K):
	
		length_list = length[ii]
		state_list = grid[ii]

		mu = 1 #exp(1) file size

		current_length = length_list[-1] 
		is_arrival = rn.binomial(1, lam_array[ii] * step)

		if is_arrival == 1:

			#add a packet into the queue
			packet_info = []
			size = rn.exponential(1/mu)
			packet_info.append(size)
			packet_info.append(size) #unfinished work, now equal to size

			state_list.append(packet_info) # packet has been pushed into queue
			current_length = current_length + 1

		length_list.append(current_length)

	return grid, length

def departure(grid, length, N, p_def, rate, step):

	for ii in range(K):

		length_list = length[ii].copy()
		state_list = grid[ii].copy()

		pop_index_list = []

		if state_list:

			limit = min(N[ii], len(state_list)) #number of users to serve

			#print(limit)

			for jj in range(limit):

				packet_info = state_list[jj]
				packet_info[1] = packet_info[1] - (rate[ii] * step) #serve limit # of customers

				

				if packet_info[1] <= 0: #if service is done

					pop_index_list.append(jj)
					#print("packet scheduled for popping")

					coin_toss = rn.uniform()

					if coin_toss > p_def[ii]:
						pass
					else:

						if ((level_decision(grid, length, N, p_def, rate, ii) < level_decision(grid, length, N, p_def, rate, ii+1)) or (ii == K-1)):
							
							new_packet_info = packet_info.copy()
							new_packet_info[1] = new_packet_info[0]
							state_list.append(new_packet_info)
							length_list[-1] = length_list[-1] + 1

							if(len(state_list) != length_list[-1]):
								raise NameError('lengths dont match at deferral+re-routing')

						else:

							new_packet_info = packet_info.copy()
							new_packet_info[1] = new_packet_info[0]
							new_state_list = grid[ii+1].copy()
							new_state_list.append(new_packet_info)
							new_length_list = length[ii+1]
							new_length_list[-1] = new_length_list[-1] + 1

							grid[ii+1] = new_state_list.copy()
							length[ii+1] = new_length_list.copy()

							if(len(new_state_list) != new_length_list[-1]):
								raise NameError('lengths dont match at deferral+forward-routing')

			#popping packets

			popped_state_list = []

			for jj in range(length_list[-1]):

				if jj in pop_index_list:
					pass
				else:
					popped_state_list.append(state_list[jj].copy())

			length_list[-1] = length_list[-1] - len(pop_index_list)

			grid[ii] = popped_state_list.copy()
			length[ii][-1]=len(grid[ii])

			if(len(grid[ii]) != length_list[-1]):
				raise NameError('lengths dont match at end')

	return grid, length

def main():

	#simulation parameters
	step = 0.001
	T = 40

	#Number of experts per level
	N = [1000, 500, 300, 100, 60, 30, 15, 10, 5, 1]

	#probability of deferral per level
	p_def = [0.8, 0.6, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0]

	#rate of service per level
	rate = np.ones(K)

	lam = 600 #arrival rate for first level

	lam_array = np.concatenate((np.array([lam]), np.zeros(K-1)))

	#state variables
	grid = [] #state of queues in the hierarchy
	length = [] #lengths of queues in the hierarchy

	grid, length = initial_conditions(grid, length) #initialize things
	check_variables(N, p_def) #check array validity

	t=0

	bar = Bar('Running', max=int(T/step))

	while(t < T):


		#arrivals
		grid, length = arrival(grid, length, lam_array, step)

		#departures
		grid, length = departure(grid, length, N, p_def, rate, step)

		t = t + step

		bar.next()

	bar.finish()

	#print(length[0])

	# length = ct_mm1(lam=1,  mu=1.1, step = 0.01, T=1000)
	plt.clf() 
	plt.plot(length[0], label = 'Queue 0')
	plt.plot(length[1], label = 'Queue 1')
	plt.plot(length[2], label = 'Queue 2')
	plt.plot(length[3], label = 'Queue 3')
	plt.plot(length[4], label = 'Queue 4')
	plt.plot(length[5], label = 'Queue 5')
	plt.plot(length[6], label = 'Queue 6')
	plt.plot(length[7], label = 'Queue 7')
	plt.plot(length[8], label = 'Queue 8')
	plt.plot(length[9], label = 'Queue 9')
	plt.title('Queue length over time')
	plt.legend()
	plt.savefig('queue_length.eps')

	# plt.clf() 
	# plt.plot(np.mean(length, 0))
	# plt.title('Mean queue length over time')
	# plt.legend()
	# plt.savefig('mean_queue_length.eps')

	#print(np.mean(length, 0))


	# plt.clf() 
	# plt.plot(alt_length_0, label = 'whatevs')
	# plt.title('Queue length over time')
	# plt.legend()
	# plt.savefig('queue_length_alt.eps')


if __name__ == "__main__":
    main()

print("--- %s seconds ---" % (time.time() - start_time))
