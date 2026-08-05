import requests
from schemas.requests import TestRequest

def endpoint_test(url, payload):
    #tests the endpoint for calculating the probability of an output
    x = requests.post(url=f'{url}', json=payload.model_dump())

    result = {"status" : x.status_code}
    result['raw_response'] = x.text

    # 3. Only parse JSON if response was successful
    if x.status_code == 200:
        result['body'] = x.json()
    else:
        result['body'] = "Request failed!"

    return result