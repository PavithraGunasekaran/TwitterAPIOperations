# Do Percent encode
import base64
import collections
import hashlib
import hmac
import json
import random
import time
import urllib

# Do percent encode
def PercentEncode(s):
    return urllib.parse.quote(str(s), safe='_')


# To create a base64 encoding string
def CreateNonce():
    nonce = []
    for i in range(0, 24):
        nonce.append(str(random.randint(0, 9)))
    return base64.b64encode(''.join(nonce).encode('utf-8'))


# Collect the Signature Parameters i.e, append the url_parameters, status in signature_parameters
def CollectSignParams(signature_parameters, url_parameters, status):
    if status is not None:
        signature_parameters['status'] = status
    for k, v in url_parameters.items():
        signature_parameters[k] = v
    return signature_parameters


# Create the Signature Parameter string and do Percent encode for the URL
# Sort the parameters, append each encoded key and '=' to the output string
def CreateSignParamString(signature_parameters):
    signature_parameters = collections.OrderedDict(sorted(signature_parameters.items()))
    param_string = ''
    counter = 0
    length = len(signature_parameters)
    for k, v in signature_parameters.items():
        param_string = param_string + PercentEncode(k) + "=" + PercentEncode(v)
        if counter < length - 1:
            param_string = param_string + '&'
            counter = counter + 1
    return param_string


# form a OAuth signature string
def CreateOauthSignature(oauth_parameters, url, url_parameters, status, oauth_consumer_secret, oauth_token_secret):
    http_method = 'POST'
    signature_parameters = oauth_parameters.copy()
    signature_parameters = CollectSignParams(signature_parameters, url_parameters, status)
    signature_param_string = CreateSignParamString(signature_parameters)
    # print("signature param string : " + signature_param_string)
    # print("signature parameters : " + str(signature_parameters))
    # Form a signature base string
    signature_base_string = http_method.upper() + '&' + PercentEncode(url) + '&' + PercentEncode(signature_param_string)
    # print("signature base string : " + signature_base_string)
    signing_key = PercentEncode(oauth_consumer_secret) + '&' + PercentEncode(oauth_token_secret)
    signing_key = signing_key.encode('utf-8')
    signature_base_string = signature_base_string.encode('utf-8')

    ''' s1 = signature.digest()
     s2 = base64.urlsafe_b64encode(s1)
     print(s2)'''

    # signature = base64.encodebytes(signature).decode('utf-8')  # need to convert to string
    # return signature
    signature = hmac.new(signing_key, signature_base_string, hashlib.sha1).digest()
    # print("type of sionature : " + str(type(signature)))
    # print("hmac signature : " + str(signature))
    signature = base64.b64encode(signature).decode()
    # print("signature : " + str(signature))

    return signature


# Create Authorization header string
def CreateAuthstring(oauth_parameters):
    oauth_parameters = collections.OrderedDict(sorted(oauth_parameters.items()))
    auth_string = 'OAuth '
    counter = 0
    length = len(oauth_parameters)
    for k, v in oauth_parameters.items():
        auth_string = auth_string + PercentEncode(k) + '=' + '"' + PercentEncode(v) + '"'
        if counter < length - 1:
            auth_string = auth_string + ',' + ''
            counter = counter + 1
    return auth_string


def GetAuthentication():
    url_parameters = {'include_entities': 'true'}
    cred = open('credentials.json', 'r')  # Enter you credentials in credentials.json
    cred = json.loads(cred.read())
    oauth_parameters = {}
    oauth_consumer_key = cred['consumer_key']
    oauth_token = cred['token']
    oauth_version = '1.0'
    oauth_timestamp = str(time.time())
    oauth_nonce = CreateNonce()
    oauth_signature_method = 'HMAC-SHA1'
    oauth_parameters.update(
        {'oauth_consumer_key': oauth_consumer_key, 'oauth_token': oauth_token, 'oauth_version': oauth_version,
         'oauth_timestamp': oauth_timestamp, 'oauth_nonce': oauth_nonce,
         'oauth_signature_method': oauth_signature_method})
    oauth_consumer_secret = cred['consumer_secret']
    oauth_token_secret = cred['token_secret']
    oauth_signature = CreateOauthSignature(oauth_parameters, url, url_parameters, status, oauth_consumer_secret,
                                           oauth_token_secret)
    oauth_parameters.update({'oauth_signature': oauth_signature})
    # create authorization header string
    auth_string = CreateAuthstring(oauth_parameters)
    header_string = {
        "Accept": "*/*",
        "Connection": "close",
        "User-Agent": "OAuth gem v0.4.4",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": auth_string,
        "Content-Length": '76',
        "Host": "api.twitter.com"
    }
    return url_parameters, header_string
