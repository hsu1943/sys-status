import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse


class DingTalk(object):
    def __init__(self, url, secret):
        self.__headers = {'Content-Type': 'application/json;charset=utf-8'}
        self.secret = secret
        if self.secret:
            res = self.sign()
            self.url = "{}&{}&{}".format(url, "timestamp={}".format(res['timestamp']), "sign={}".format(res['sign']))
        else:
            self.url = url

    def send_msg(self, text, mobiles):
        json_text = {
            "msgtype": "text",
            "text": {
                "content": text
            },
            "at": {
                "atMobiles": mobiles,
                "isAtAll": False
            }
        }
        return requests.post(self.url, json.dumps(json_text), headers=self.__headers).content

    def send_markdown(self, title, text, mobiles):
        json_text = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            },
            "at": {
                "atMobiles": mobiles,
                "isAtAll": False
            }
        }
        return requests.post(self.url, json.dumps(json_text), headers=self.__headers).content

    def sign(self):
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return {"sign": sign, "timestamp": timestamp}
