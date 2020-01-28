import os,requests,uuid,json



if __name__=='__main__':
    try:
        key_var_name = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'
        if not (key_var_name in os.environ):
            raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
        subscription_key = os.environ[key_var_name]
        endpoint_var_name = 'TRANSLATOR_TEXT_ENDPOINT'
        if not (endpoint_var_name in os.environ):
            raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
        endpoint = os.environ[endpoint_var_name]
    except Exception as e:
        print(e)
    else:


        #检测文本语言
        path = '/detect?api-version=3.0'
        constructed_url = endpoint + path

        headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json'}
        body = [{'text': 'The weather today is nice!'},{'text': 'Hello World!'}]
        request = requests.post(constructed_url, headers=headers, json=body)
        response = request.json()
        print(json.dumps(response,sort_keys=True,indent=4,
            ensure_ascii=False,separators=(',',': ')))
        print(response[0]['language'])

        #翻译文本
        path = '/translate?api-version=3.0'
        params = '&to=zh-Hans'
        constructed_url = endpoint + path + params
        request = requests.post(constructed_url, headers=headers, json=body)
        response = request.json()
        print(json.dumps(response,sort_keys=True,indent=4,
            ensure_ascii=False,separators=(',',': ')))
        print(response[0]['translations'][0]['text'])
        print(response[1]['translations'][0]['text'])
