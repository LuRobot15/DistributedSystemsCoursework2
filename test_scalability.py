import random
import requests
import time
import matplotlib.pyplot as plt
import math

generate_data_url = "https://distributedsystemscoursework2.azurewebsites.net/api/generate_data_scalability_test"
reset_table_url = "https://distributedsystemscoursework2.azurewebsites.net/api/delete_data"

def main():
	amount_of_iterations = [1, 10, 100, 1000, 10000, 100000, 1000000]
	time_taken = test(amount_of_iterations)
 
	#plotting the graph
	xpoints = []
	ypoints = []
	for amount in amount_of_iterations:
		xpoints.append(math.log(amount, 10))
	for time in time_taken:
		ypoints.append(math.log(time, 10))
	
	plt.plot(xpoints, ypoints, 'o', linestyle='solid')
	plt.xlabel("log10(number of records added)")
	plt.ylabel("log10(time taken for all data to be stored)")
	plt.show()
	plt.savefig("scalability.pdf", format="pdf", bbox_inches='tight')
 

#returns how long it takes to run the function for each amount of iterations
def test(amount_of_iterations):
	time_taken = []
    
	for amount in amount_of_iterations:   
		start = time.time()

		response = requests.post(generate_data_url, json = {"amount_of_data": amount})

		end = time.time()

		time_taken.append(end - start)

		response = requests.post(reset_table_url)
	
	return time_taken


if __name__ == "__main__":
	main()