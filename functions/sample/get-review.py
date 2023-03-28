import sys

from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(param_dict):
    authenticator = IAMAuthenticator(param_dict["IAM_API_KEY"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(param_dict["COUCH_URL"])
    
    selector = {}
    if param_dict["dealerId"] is not None and param_dict["dealerId"] != "":
        selector = {'dealership': {'$eq': int(param_dict["dealerId"])}}
        
    try:
        response = service.post_find(
            db='reviews',
            selector=selector,
        ).get_result()
        # result_by_filter=my_database.get_query_result(selector,raw_result=True)
        result= {
            'headers': {'Content-Type':'application/json'},
            'body': {'data':response["bookmark"]}
        }
        return response
    except:
        return {
            'statusCode': 404,
            'message':"dealerId does not exist"
        }