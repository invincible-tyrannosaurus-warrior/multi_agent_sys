# -*- coding: utf-8 -*-


import os
from zai import ZhipuAiClient
import urllib3
import httpx
import ssl
import requests
from urllib3.exceptions import InsecureRequestWarning
import base64

###############################################################################
# CONFIGURATION AND SSL BYPASS SETUP
###############################################################################

## Disable SSL warnings
urllib3.disable_warnings(InsecureRequestWarning)

## Set environment variables for SSL bypass
os.environ.update({
    'PYTHONHTTPSVERIFY': '0',
    'CURL_CA_BUNDLE': '',
    'REQUESTS_CA_BUNDLE': '',
    'SSL_CERT_FILE': '',
})

## Global SSL context override
ssl._create_default_https_context = ssl._create_unverified_context

## Create a custom session with SSL verification disabled
session = requests.Session()
session.verify = False

## Custom httpx client with SSL disabled and proxy support
custom_client = httpx.Client(
    verify=False,
    timeout=300.0,
    transport=httpx.HTTPTransport(
        proxy="http://xxx",
        verify=False
    )
)


###############################################################################
# 调用GLM4.5V进行照片分析
###############################################################################

def analyze_image_with_glm45v(img_path, prompt):
    client = ZhipuAiClient(
        api_key="your api key",
        http_client=custom_client
    )
    with open(img_path, "rb") as img_file:
        img_base = base64.b64encode(img_file.read()).decode("utf-8")
    response = client.chat.completions.create(
        model="glm-4.5v",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_base
                        }
                    },
                    # 修改内容，使GLM4.5V生成pass/unpass，如果unpass生成指导性意见
                    {
                        "type": "text",
                        "text": f"""
                            the uploaded image represents current code script's milestone. 
                            Your task is to judge whether the current milestone satisfies the requirements in
                            the following coding prompt.
                            Coding prompt: {prompt}.
                        """
                    }
                ]
            }
        ],
        thinking={
            "type": "enabled"
        }
    )
    return response.choices[0].message