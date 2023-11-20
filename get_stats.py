# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(get_stats) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints


import azure.functions as func
import logging
from azure.functions.decorators.core import DataType
import json

get_stats_bp = func.Blueprint()

#gets the stats for each sensor and returns them in a string
@get_stats_bp.function_name(name='get_stats')
@get_stats_bp.route(route="get_stats", auth_level=func.AuthLevel.ANONYMOUS)
@get_stats_bp.generic_input_binding(arg_name="sensorData", type='sql', CommandText="select [sensorID], [Tempurature], [Wind], [R.Humidity], [CO2] from dbo.sensorData", ConnectionStringSetting="SqlConnectionString", data_type=DataType.STRING)
def get_stats(req: func.HttpRequest, sensorData: func.SqlRowList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

	#extracting the data from the sensor table
    sensor_data = list(map(lambda r: json.loads(r.to_json()), sensorData))
    
    analytics_list = []
    
    #iterating through the sensors and setting a min and max that will change on the first record for each sensor
    for sensor in range(1, 21):
        num_sensors = 0
        total_temp = 0
        total_wind = 0
        total_humidity = 0
        total_co2 = 0.
        min_temp = 100000
        max_temp = -100000
        min_wind = 100000
        max_wind = -100000
        min_humidity = 100000
        max_humidity = -100000
        min_co2 = 100000
        max_co2 = -100000
        #iterating through the sensor data to find records of the sensor, to update the min, max and averages for each data point
        for row in sensor_data:
            if row["sensorID"] == sensor:
                num_sensors = num_sensors + 1
                total_temp = total_temp + row["Tempurature"]
                total_wind = total_wind + row["Wind"]
                total_humidity = total_humidity + row["R.Humidity"]
                total_co2 = total_co2 + row["CO2"]
                if row['Tempurature'] < min_temp:
                    min_temp = row['Tempurature']
                if row['Tempurature'] > max_temp:
                    max_temp = row['Tempurature']
                if row['Wind'] < min_wind:
                    min_wind = row['Wind']
                if row['Wind'] > max_wind:
                    max_wind = row['Wind']
                if row['R.Humidity'] < min_humidity:
                    min_humidity = row['R.Humidity']
                if row['R.Humidity'] > max_humidity:
                    max_humidity = row['R.Humidity']
                if row['CO2'] < min_co2:
                    min_co2 = row['CO2']
                if row['CO2'] > max_co2:
                    max_co2 = row['CO2']
        
        #avoiding division by 0
        if num_sensors == 0:
            continue
        
        avg_temp = total_temp / num_sensors
        avg_wind = total_wind / num_sensors
        avg_humidity = total_humidity / num_sensors
        avg_co2 = total_co2 / num_sensors

		#adding the data to the list for output
        analytics_list.append({"sensorID" : sensor, "minimum Tempurature" : min_temp, "maximum Tempurature" : max_temp, "adverage Tempurature" : avg_temp,
                                "minimum Wind" : min_wind, "maximum Wind" : max_wind, "adverage Wind" : avg_wind,
                                "minimum Humidity" : min_humidity, "maximum Humidity" : max_humidity, "adverage Humidity" : avg_humidity,
                                "minimum CO2" : min_co2, "maximum CO2" : max_co2, "adverage CO2" : avg_co2})

	#building the output string
    output = ""
    for row in analytics_list:
        output = output + str(row) + "\n"
    
    return func.HttpResponse(output, status_code=200)