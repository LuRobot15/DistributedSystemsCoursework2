# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(analytics) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints


import azure.functions as func
import logging
from azure.functions.decorators.core import DataType
import json

analytics_bp = func.Blueprint()

#function is calledwhen data is stored in sensor data table, it updates the sensor analytics table given the data passed to it
#because python v2 doesn't have an sql trigger, a HTTP trigger was used instead
@analytics_bp.function_name(name='analytics')
@analytics_bp.route(route="analytics", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
@analytics_bp.generic_input_binding(arg_name="sensorData", type='sql', CommandText="select [sensorID], [Tempurature], [Wind], [R.Humidity], [CO2] from dbo.sensorData", ConnectionStringSetting="SqlConnectionString", data_type=DataType.STRING)
@analytics_bp.generic_input_binding(arg_name="deletingAnalytics", type='sql', CommandText="dbo.deleteSensorAnalytics", commandType="StoredProcedure", ConnectionStringSetting="SqlConnectionString", data_type=DataType.STRING)
@analytics_bp.generic_output_binding(arg_name="sensorAnalytics", type='sql', CommandText="dbo.sensorAnalytics", ConnectionStringSetting="SqlConnectionString", data_type=DataType.STRING)
def analytics(req: func.HttpRequest, sensorData: func.SqlRowList, deletingAnalytics: func.SqlRowList, sensorAnalytics: func.Out[func.SqlRow]) -> func.HttpResponse:
    #extracting the data from the sensor table
    sensor_data = list(map(lambda r: json.loads(r.to_json()), sensorData))
    
    logging.info('Python SQL trigger function processed a request.')
    
    analytics_data_sql_list = []
    
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
        
        #adding the data to the list that will be used to update the sensor analytics table
        analytics_data_sql_list.append((func.SqlRow({"sensorID" : sensor, "minTemp" : min_temp, "maxTemp" : max_temp,
                                                                        "minWind" : min_wind, "maxWind" : max_wind,
                                                                        "minHumidity" : min_humidity, "maxHumidity" : max_humidity,
                                                                        "minCO2" : min_co2, "maxCO2" : max_co2,
                                                                        "meanTemp" : avg_temp, "meanWind" : avg_wind, "meanHumidity" : avg_humidity, "meanCO2" : avg_co2})))
    
    #sending the data to the analytics table  
    sensorAnalytics.set(func.SqlRowList(analytics_data_sql_list))
    
    return func.HttpResponse(
        "Analytics table updated successfully\n",
        status_code=200)