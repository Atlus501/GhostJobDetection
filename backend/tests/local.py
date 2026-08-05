from payloads.endpoint_test import test_payload
from test_types.endpoint import endpoint_test

url = 'http://127.0.0.1:8000/test'

#tests the endpoint for calculating the probability of an output
result = endpoint_test(url=f'{url}', payload=test_payload)

print(result)