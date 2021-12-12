import json

def handler(event, ctx):
    print("***")
    print(event)
    print("***")

    msg = "testing, hiii"
    if (event.queryStringParameters
        and "name" in event.queryStringParameters):
        msg = msg + " " + event.queryStringParameters["name"] + "!!"

    return {"statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": msg})}
