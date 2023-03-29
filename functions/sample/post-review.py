import sys

from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException

def main(param_dict):
    authenticator = IAMAuthenticator(param_dict["IAM_API_KEY"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(param_dict["COUCH_URL"])
        
    
    try:
        response = service.post_document(
            db='reviews',
            document=param_dict["review"],
        ).get_result()
        # result_by_filter=my_database.get_query_result(selector,raw_result=True)
        result= {
            'headers': {'Content-Type':'application/json'},
            'body': {'data':response}
        }
        return result
    except ApiException as ae:
        errorBody = {"error": ae.message}
        if ("reason" in ae.http_response.json()):
            errorBody["reason"] = ae.http_response.json()["reason"]
        
        return errorBody
    except:
        return {
            'statusCode': 500,
            'message': "Something went wrong on the server"
        }
