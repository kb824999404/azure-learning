import requests
import matplotlib.pyplot as plt
import json 
from PIL import Image
from io import BytesIO
import os



if __name__=='__main__':
    #读取密钥和终结点
    if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
        print('subscription_key: '+subscription_key)
    else:
        print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()
    if 'COMPUTER_VISION_ENDPOINT' in os.environ:
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
        print('endpoint: '+endpoint)
    else:
        print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()
    
    thumbnail_url=endpoint+"vision/v2.1/generateThumbnail"

    image_url=input("Please input the url of the image: ")
    width=input("Width: ")
    height=input("Height: ")

    headers={'Ocp-Apim-Subscription-Key':subscription_key}
    params= {'width': width, 'height': height, 'smartCropping': 'true'}
    data={'url':image_url}
    respose=requests.post(thumbnail_url,headers=headers,params=params,json=data)
    respose.raise_for_status()

    image=Image.open(BytesIO(respose.content))
    plt.imshow(image)
    plt.axis("off")
    print("Thumbnail is {0}-by-{1}".format(*image.size))

    plt.show()


