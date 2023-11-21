import azure.functions as func
import logging
from azure.functions.decorators.core import DataType
import random
import uuid
from analytics import analytics_bp
from generate_data import generate_data_bp
from get_stats import get_stats_bp
from delete_data import delete_data_bp
from regularly_generate_data import regularly_generate_data_bp
from regular_db_clearence import regular_db_clearence_bp
from generate_data_scalability_test import generate_data_scalability_test_bp

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
app.register_functions(analytics_bp)
app.register_functions(generate_data_bp)
app.register_functions(get_stats_bp)
app.register_functions(delete_data_bp)
app.register_functions(regularly_generate_data_bp) 
app.register_functions(regular_db_clearence_bp)
app.register_functions(generate_data_scalability_test_bp)


#test input data
#{"sensorID": 1, "Tempurature": 10, "Wind": 20, "R.Humidity": 50, "CO2": 1000}
#{"sensorID": 1, "Tempurature": 12, "Wind": 22, "R.Humidity": 52, "CO2": 1002}

#takes data and stores it in the database
@app.function_name(name='store_data')
@app.route(route="store_data", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
@app.generic_output_binding(arg_name="sensorData", type='sql', CommandText="dbo.sensorData", ConnectionStringSetting="SqlConnectionString", data_type=DataType.STRING)
def store_data(req: func.HttpRequest, sensorData: func.Out[func.SqlRow]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    #getting the data from the request
    sensor = req.params.get('sensorID')
    if not sensor:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            sensor = req_body.get('sensorID')
    
    tempurature = req.params.get('Tempurature')
    if not tempurature:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            tempurature = req_body.get('Tempurature')
    
    wind = req.params.get('Wind')
    if not wind:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            wind = req_body.get('Wind')
    
    humidity = req.params.get('R.Humidity')
    if not humidity:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            humidity = req_body.get('R.Humidity')
    
    co2 = req.params.get('CO2')
    if not co2:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            co2 = req_body.get('CO2')
    
    #Adding the data to the database
    sensorData.set(func.SqlRow({"ID" : str(uuid.uuid4()), "sensorID" : sensor, "Tempurature" : tempurature, "Wind" : wind, "R.Humidity" : humidity, "CO2" : co2}))

    return func.HttpResponse(
        f"The following record was added to the data base:\nsensorID : {sensor}, Tempurature : {tempurature}, Wind : {wind}, R.Humidity : {humidity}, CO2 : {co2}",
        status_code=200)
    