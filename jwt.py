import base64


def get_element(token):
    result = [x.strip() for x in token.split('.')]
    return result

def get_header():
    result = get_element(token)
    header = result[0]

    for x in range(0,(32-len(header))):
        header += "="

    header_value = (base64.b64decode(header)).decode()
    print("Header is : " + header_value)

def get_body():
    result = get_element(token)
    body = result[1]

    for x in range(0, (116 - len(body))):
        body += "=";

    body_value = (base64.b64decode(body)).decode()
    print("Body is : " + body_value)

def get_signature():
    result = get_element(token)
    signature = result[2]
    print("Signature is : " + signature)

if __name__== "__main__":
    token = "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ.8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg=="

    get_header()
    get_body()
    get_signature()