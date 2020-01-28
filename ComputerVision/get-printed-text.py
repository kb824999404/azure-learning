import requests
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import json 
from PIL import Image
from io import BytesIO
import os
import sys


if __name__=='__main__':
    #读取密钥和终结点
    if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
        # print('subscription_key: '+subscription_key)
    else:
        print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()
    if 'COMPUTER_VISION_ENDPOINT' in os.environ:
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
        # print('endpoint: '+endpoint)
    else:
        print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()
    
    local=False
    #有命令行参数'--local'则使用本地图片
    if len(sys.argv)>1:
        if '--local' in sys.argv:
            local=True
            

    ocr_url=endpoint+"vision/v2.1/ocr"

    #图片路径
    if local:
        image_path=input("Please input the path of the image: ")
        image_data = open(image_path, "rb").read()
    else:
        image_url=input("Please input the url of the image: ")

    if local:
        headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    else:
        headers={'Ocp-Apim-Subscription-Key':subscription_key}
        data={'url':image_url}

    params= {'language':'zh-Hans','detectOrientation':'true'}

    #Post请求
    if local:
        response = requests.post(ocr_url, headers=headers, params=params, data = image_data)
    else:
        response=requests.post(ocr_url,headers=headers,params=params,json=data)
    
    #分析响应数据
    response.raise_for_status()

    analysis=response.json()

    #所有词句及位置等信息
    line_infos=[region["lines"] for region in analysis["regions"]]
    word_infos=[]
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                word_infos.append(word_info)

    print(word_infos)


    plt.rcParams['font.sans-serif'] = ['SimHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(5,5))

    #显示图片
    if local:
        image=Image.open(BytesIO(image_data))
    else:
        image=Image.open(BytesIO(requests.get(image_url).content))

    ax=plt.imshow(image,alpha=0.5)

    #显示文字
    for word in word_infos:
        bbox=[int(num) for num in word["boundingBox"].split(",")]
        text=word["text"]
        origin=(bbox[0],bbox[1])
        patch=Rectangle(origin,bbox[2],bbox[3],fill=False,linewidth=2,color='y')
        ax.axes.add_patch(patch)
        # plt.text(origin[0],origin[1],text,fontsize=20)

    for word in word_infos:
        print(word['text'],end=',')

    plt.axis("off")
    plt.show()


