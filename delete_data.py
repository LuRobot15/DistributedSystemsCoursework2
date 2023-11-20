# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(delete_data) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints


import azure.functions as func
import logging
import json
from azure.functions.decorators.core import DataType

delete_data_bp = func.Blueprint()

@delete_data_bp.function_name(name='delete_data')
@delete_data_bp.route(route="delete_data", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
@delete_data_bp.generic_input_binding(arg_name="deletingSensorData", type='sql', CommandText="dbo.deleteSensorData", commandType="StoredProcedure", ConnectionStringSetting="SqlConnectionString", data_type=DataType.STRING)
def delete_data(req: func.HttpRequest, deletingSensorData: func.SqlRowList) -> func.HttpResponse:
    logging.info('sensor data deleted')
    
    #extracting the data from the sensor table
    rows = list(map(lambda r: json.loads(r.to_json()), deletingSensorData))

    return func.HttpResponse(json.dumps(rows), status_code=200)