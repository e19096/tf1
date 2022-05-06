import pytest
import trucks
import os

test_event = {
    'version': '1.0',
    'resource': '/reservations',
    'path': '/serverless_lambda_stage/reservations',
    # 'resource': '/trucks',
    # 'path': '/serverless_lambda_stage/trucks',
    # 'httpMethod': 'POST',
    'httpMethod': 'GET',
    'headers': {
        'Content-Length': '0',
        'Host': 'l816j6tbjg.execute-api.us-east-2.amazonaws.com',
        'User-Agent': 'curl/7.54.0',
        'X-Amzn-Trace-Id': 'Root=1-61b6d4b4-573865131a4a2b49465f14c7',
        'X-Forwarded-For': '37.120.244.52',
        'X-Forwarded-Port': '443',
        'X-Forwarded-Proto': 'https',
        'accept': '*/*'
    },
    'multiValueHeaders': {
        'Content-Length': ['0'],
        'Host': ['l816j6tbjg.execute-api.us-east-2.amazonaws.com'],
        'User-Agent': ['curl/7.54.0'],
        'X-Amzn-Trace-Id': ['Root=1-61b6d4b4-573865131a4a2b49465f14c7'],
        'X-Forwarded-For': ['37.120.244.52'],
        'X-Forwarded-Port': ['443'],
        'X-Forwarded-Proto': ['https'],
        'accept': ['*/*']
    },
    # 'queryStringParameters': {
    #     # 'user_id': '99',
    #     'truck_id': '1',
    #     'start_dt': '2021-12-16T14:00:00Z',
    #     'end_dt': '2021-12-16T15:30:00Z',
    # },
    'queryStringParameters': None,
    # 'queryStringParameters': {
    #     'end_dt': '2021-12-15T09:30:00',
    #     'start_dt': '2021-12-15T08:00:00'
    # },
    'multiValueQueryStringParameters': {},
    'requestContext': {
        'accountId': '826400453259',
        'apiId': 'l816j6tbjg',
        'authorizer': {
            'claims': {
                'aud': '28427m4ef9sv96kd3gatpdhsmo',
                'auth_time': '1639530242',
                'cognito:username': 'david@roseapothecary.com',
                'event_id': 'b9593fb9-1fa6-47ce-9905-293abc534fe3',
                'exp': '1639533842',
                'iat': '1639530242',
                'iss': 'https://cognito-idp.us-east-2.amazonaws.com/us-east-2_OfO9zaVMY',
                'jti': 'debc2769-e6b7-46e7-8dc1-8c4393757863',
                'origin_jti': '992088fa-1392-4670-910f-498e9cde4721',
                'sub': '9cd757fc-0f7f-4547-8d62-1a52e5289ecb',
                'token_use': 'id'
            },
            'scopes': None
        },
        'domainName': 'l816j6tbjg.execute-api.us-east-2.amazonaws.com',
        'domainPrefix': 'l816j6tbjg',
        'extendedRequestId': 'KRYsSgpKCYcEPeg=',
        'httpMethod': 'GET',
        'identity': {
            'accessKey': None,
            'accountId': None,
            'caller': None,
            'cognitoAmr': None,
            'cognitoAuthenticationProvider': None,
            'cognitoAuthenticationType': None,
            'cognitoIdentityId': None,
            'cognitoIdentityPoolId': None,
            'principalOrgId': None,
            'sourceIp': '37.120.244.52',
            'user': None,
            'userAgent': 'curl/7.54.0',
            'userArn': None
        },
        'path': '/serverless_lambda_stage/trucks',
        'protocol': 'HTTP/1.1',
        'requestId': 'KRYsSgpKCYcEPeg=',
        'requestTime': '13/Dec/2021:05:05:56 +0000',
        'requestTimeEpoch': 1639371956889,
        'resourceId': 'GET /trucks',
        'resourcePath': '/trucks',
        'stage': 'serverless_lambda_stage'
    },
    'pathParameters': None,
    'stageVariables': None,
    'body': None,
    'isBase64Encoded': False
}

def test_lambda_handler():
    os.environ['DB_NAME'] = 'constituents_development'
    os.environ['DB_USER'] = 'postgres'
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_PORT'] = '5432'
    os.environ['DB_PASSWORD'] = 'postgres'

    response = trucks.handler(event=test_event, context={})
    import pdb; pdb.set_trace()
