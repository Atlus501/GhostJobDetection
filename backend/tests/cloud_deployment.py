from payloads.endpoint_test import test_payload
from test_types.endpoint import endpoint_test
import requests

url = 'https://helloworld-portfolio-projects.click/health'
results = []

try:
    #tests the endpoint for calculating the probability of an output
    x = requests.get(url=f'{url}')
    results.append(x.json())
    print(x)

    url = 'https://helloworld-portfolio-projects.click/test/'
    x = endpoint_test(url=f'{url}', payload=test_payload)
    print(x)
    
except Exception as e:
    print(e)