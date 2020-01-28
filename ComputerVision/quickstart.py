from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time


#描述图像
def describeImage(client,remote_image_url):
    print("===== Describe an image - remote =====")

    description_results=client.describe_image(remote_image_url)
    print("Description of remote image: ")
    if(len(description_results.captions)==0):
        print("No description detected.")
    else:
        for caption in description_results.captions:
            print(" '{}' with confidence {:.2f}%".format(caption.text,caption.confidence*100))

#图像分类
def imageClassify(client,remote_image_url):
    print('===== Categorize an image - remote =====')
    remote_image_features=['categories']
    categorize_results_remote=client.analyze_image(remote_image_url,remote_image_features)

    print('Categories from remote image: ')

    if(len(categorize_results_remote.categories)==0):
        print('No categories detected.')
    else:
        for category in categorize_results_remote.categories:
            print(" '{}' winth confidence {:.2f}%".format(category.name,category.score*100))

#检测物体
def detectObject(client,remote_image_url):
    print('===== Detect Objects - remote =====')

    detect_objects_results_remote=client.detect_objects(remote_image_url)

    print('Detecting objects in remote image:')
    if(len(detect_objects_results_remote.objects)==0):
        print('No objects detected.')
    else:
        for object in detect_objects_results_remote.objects:
            print('object at location {}, {}, {}, {}'.format(object.rectangle.x,
            object.rectangle.x+object.rectangle.w,
            object.rectangle.y,object.rectangle.y+object.rectangle.h))

#读取文本
def readText(client,url):
    print('===== Batch Read File - remote =====')
    recongnize_printed_results=client.batch_read_file(url,raw=True)

    operation_loaction_remote=recongnize_printed_results.headers["Operation-Location"]

    operation_id=operation_loaction_remote.split("/")[-1]

    print('location: '+operation_loaction_remote)
    print('id: '+operation_id)

    #获取读取结果,每隔一秒钟检查一次操作
    while True:
        get_printed_text_results=client.get_read_operation_result(operation_id)
        if get_printed_text_results.status not in ['NotStarted','Running']:
            break
        time.sleep(1)
    
    if get_printed_text_results.status==TextOperationStatusCodes.succeeded:
        for text_result in get_printed_text_results.recognition_results:
            for line in text_result.lines:
                print(line.text)
                print(line.bounding_box)

    print()


    

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
    
    #实例化客户端
    computervisionclient=ComputerVisionClient(endpoint,CognitiveServicesCredentials(subscription_key))

    remote_image_url=input("Please input the url of the image: ")
    # describeImage(computervisionclient,remote_image_url)
    # imageClassify(computervisionclient,remote_image_url)
    # detectObject(computervisionclient,remote_image_url)
    readText(computervisionclient,remote_image_url)



    