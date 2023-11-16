import azure.functions as func
import logging
from azure.functions.decorators.core import DataType
import random
import uuid

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name='generate_data')
@app.route(route="generate_data", auth_level=func.AuthLevel.ANONYMOUS)
@app.generic_output_binding(arg_name="sensorData", type='sql', CommandText="dbo.sensorData", ConnectionStringSetting="SqlConnectionString", data_type=DataType.STRING)
def generate_data(req: func.HttpRequest, sensorData: func.Out[func.SqlRow]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    #generating the data and storing it in the database
    sensor_data_generated = []
    sensor_data_generated_sql = []
    for i in range(1, 21):
        tempurature = random.randint(8, 15)
        wind_speed = random.randint(15, 25)
        humidity = random.randint(40, 70)
        co2 = random.randint(500, 1500)
        sensor_data_generated_sql.append(func.SqlRow({"ID" : str(uuid.uuid4()), "sensorID" : i, "Tempurature" : tempurature, "Wind" : wind_speed, "R.Humidity" : humidity, "CO2" : co2}))
        sensor_data_generated.append([i, tempurature, wind_speed, humidity, co2])
    
    sensorData.set(func.SqlRowList(sensor_data_generated_sql))
    
    output_string = ""
    for i in range(0, 20):
        output_string = output_string + f"sensorID: {sensor_data_generated[i][0]}, temp: {sensor_data_generated[i][1]}, wind: {sensor_data_generated[i][2]}, humidity: {sensor_data_generated[i][3]}, co2: {sensor_data_generated[i][4]}\n"

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.\n" + output_string)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response. \n" + output_string,
             status_code=200
        )