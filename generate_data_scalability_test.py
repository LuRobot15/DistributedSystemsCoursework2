# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(generate_data_bp) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints

import azure.functions as func
import requests
import random
import logging

generate_data_scalability_test_bp = func.Blueprint()

add_data_url = "https://distributedsystemscoursework2.azurewebsites.net/api/store_data"

#generates data and sends it to the store_data function data and stores it in the database
@generate_data_scalability_test_bp.function_name(name='generate_data_scalability_test')
@generate_data_scalability_test_bp.route(route="generate_data_scalability_test", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
def generate_data_scalability_test(req: func.HttpRequest) -> func.HttpResponse:
    
    #getting the data from the request
    amount_of_data = req.params.get('amount_of_data')
    if not amount_of_data:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            amount_of_data = req_body.get('amount_of_data')
    
    #generating the data
    for i in range(amount_of_data):
        sensor_id = random.randint(1, 20)
        temperature = random.randint(8, 15)
        wind = random.randint(15, 25)
        humidity = random.randint(40, 70)
        co2 = random.randint(500, 1500)
        
        data = {"sensorID": sensor_id, "Tempurature": temperature, "Wind": wind, "R.Humidity": humidity, "CO2": co2}
        response = requests.post(add_data_url, json = data)
    
    return func.HttpResponse(
        "Data generated and stored in database\n",
        status_code=200)