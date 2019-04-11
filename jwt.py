import base64


def element(token):
    result = [x.strip() for x in token.split('.')]
    return result

def header():
    result = element(token)
    header = result[0]

    #header = "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ";

    for x in range(0,(32-len(header))):
        header += "="

    decode_1 = base64.b64decode(header)
    decode_2 = decode_1.decode()

    print(decode_2)

def body():
    # body = "eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ";
    result = element(token)
    body = result[1]

    for x in range(0, (116 - len(body))):
        body += "=";

    decode_1 = base64.b64decode(body)
    decode_2 = decode_1.decode()

    print(decode_2)

def signature():
    result = element(token)
    signature = result[2]
    print(signature)

if __name__== "__main__":
    token = "eyJBbGciOjIsIlRva2VuVHlwIjoxfQ.eyJVVUlEIjoiMDFkM3gzd20ybm5yZGZ6cDB0a2Eydnc5ZHgiLCJQZXJtaXNzaW9uIjozLCJFeHBpcmF0aW9uVGltZXN0YW1wIjoxODkzNDU2MDAwfQ.8lVhZo_W6KmGI2oi5JNHioDvPq2Yl86v4uae3RfKc-qoKUwHNxFtXO2NFmChsi35__t1uC_SD-Ay_MoateeDNg=="

    header()
    body()
    signature()
