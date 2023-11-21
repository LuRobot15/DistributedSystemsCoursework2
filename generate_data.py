# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(generate_data) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints


import azure.functions as func
import logging
import requests
import random

generate_data_bp = func.Blueprint()

add_data_url = "https://distributedsystemscoursework2.azurewebsites.net/api/store_data"

@generate_data_bp.function_name(name='generate_data')
@generate_data_bp.route(route="generate_data", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
def generate_data(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request, generating data.')

    #generating the data
    for i in range(1, 21):
        temperature = random.randint(8, 15)
        wind = random.randint(15, 25)
        humidity = random.randint(40, 70)
        co2 = random.randint(500, 1500)
        
        data = {"sensorID": i, "Tempurature": temperature, "Wind": wind, "R.Humidity": humidity, "CO2": co2}
        response = requests.post(add_data_url, json = data)

    if response.status_code == 200:
        return func.HttpResponse(
			"Data generated and stored in database\n",
			status_code=200
		)
    else:
        return func.HttpResponse(
			"An error occured while generating or storing the data\n",
			status_code=400
		)