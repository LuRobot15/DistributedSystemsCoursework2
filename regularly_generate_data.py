# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(regularly_generate_data) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints

import azure.functions as func
import logging
import requests
import random

regularly_generate_data_bp = func.Blueprint()


add_data_url = "https://distributedsystemscoursework2.azurewebsites.net/api/store_data"
analytics_table_update_url = "https://distributedsystemscoursework2.azurewebsites.net/api/analytics"

#every 30 minutes, generate sensor data, submit it to the database and update the analytics table
@regularly_generate_data_bp.timer_trigger(schedule="00:30:00", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def regularly_generate_data(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('data added to database')
    
    #generating data for each sensor
    for i in range(1, 21):
        sensor_id = i
        temperature = random.randint(8, 15)
        wind = random.randint(15, 25)
        humidity = random.randint(40, 70)
        co2 = random.randint(500, 1500)
        
        #sending data to be stored in database
        data = {"sensorID": sensor_id, "Tempurature": temperature, "Wind": wind, "R.Humidity": humidity, "CO2": co2}
        response = requests.post(add_data_url, json = data)
    
    #updating analytics table
    #done via HTTP as there currently is no SQL trigger for python v2
    requests.post(analytics_table_update_url)
    