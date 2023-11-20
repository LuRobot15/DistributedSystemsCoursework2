# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(regular_db_clearence) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints

import azure.functions as func
import logging
import requests

regular_db_clearence_bp = func.Blueprint()

delete_data_url = "https://distributedsystemscoursework2.azurewebsites.net/api/delete_data"

#at midnight everyday, delete all the data from the database
@regular_db_clearence_bp.timer_trigger(schedule="1.00:00:00", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def regular_db_clearence(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed. data in database deleted')
    
    requests.post(delete_data_url)