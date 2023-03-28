import sys

from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException

def main(param_dict):
    authenticator = IAMAuthenticator(param_dict["IAM_API_KEY"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(param_dict["COUCH_URL"])
        
    
    try:
        posted_review = Document(
            id=param_dict["review"]["id"],
            name=param_dict["review"]["name"],
            dealership=param_dict["review"]["dealership"],
            review=param_dict["review"]["review"],
            purchase=param_dict["review"]["purchase"],
            purchase_date=param_dict["review"]["purchase_date"],
            car_make=param_dict["review"]["car_make"],
            car_model=param_dict["review"]["car_model"],
            car_year=param_dict["review"]["car_year"]
        )
        
        uuid = service.get_uuids(count=1).get_result()
        thisUuid = uuid["uuids"][0]
        
        response = service.put_document(
            db='reviews',
            doc_id=thisUuid,
            document=posted_review,
        ).get_result()
        # result_by_filter=my_database.get_query_result(selector,raw_result=True)
        result= {
            'headers': {'Content-Type':'application/json'},
            'body': {'data':response}
        }
        return response
    except ApiException as ae:
        errorBody = {"error": ae.message}
        if ("reason" in ae.http_response.json()):
            errorBody["reason"] = ae.http_response.json()["reason"]
    except:
        return {
            'statusCode': 500,
            'message': "Something went wrong on the server"
        }
