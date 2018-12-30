from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,Http404
import os
import pytesseract
from PIL import Image, ImageDraw
import json
from mysite.settings import BASE_DIR
from distinguish.util import handle

pytesseract.pytesseract.tesseract_cmd = r'D:\yanggeng\Tesseract-OCR\tesseract.exe'

def index(request):
    return render(request, 'distinguish/index.html')


def results(request):
    # text = "You're looking at the results."
    text = request.GET.get("result")

    return render(request, 'distinguish/result.html', {'text': text})

@csrf_exempt
def upload(request):
    data = {
        "success": True,
        "data": {}
    }

    if request.method == "POST":
        upObj = request.FILES.get('picture')

        with open(os.path.join(BASE_DIR, 'static', 'moment', upObj.name), 'wb') as f:
            for chunk in upObj.chunks():
                f.write(chunk)

        path = os.path.join(BASE_DIR, 'static', 'moment', upObj.name)

        engineType = "2"
        disType = "1"
        try:
            disType = request.GET.get("distype")
            engineType = request.GET.get("engtype")
        except:
            pass


        text = ""

        if engineType == "2":
            if disType == "1" or disType == "2":
                text = handle.apiUtil.chiOCR(path)
            if disType == "3":
                image = Image.open(path)

                # 转灰度图
                image = image_grayscale_deal(image)
                # 二值化
                image = image_thresholding_method(image)
                # 锐化
                # image = image_binarizing(image,150)
                # image.show()
                # 降噪
                image = image_clear_noise(image)
                image.save(path)
                text = handle.apiUtil.handWrittingOCR(path)
            if disType == "4":
                text = handle.apiUtil.handWrittingOCR(path)

        elif engineType == "1":
            image = Image.open(path)

            if disType == "1":
                # 转灰度图
                image = image_grayscale_deal(image)
                # 二值化
                image = image_thresholding_method(image)
                text = pytesseract.image_to_string(image, lang="chi_sim")


            if disType == "2":
                text = pytesseract.image_to_string(image, lang="eng")

            if disType == "3":
                # 转灰度图
                image = image_grayscale_deal(image)
                # 二值化
                image = image_thresholding_method(image)
                # 锐化
                # image = image_binarizing(image,150)
                # image.show()
                # 降噪
                image = image_clear_noise(image)

                text = pytesseract.image_to_string(image,lang="eng")


            print(text)

        data['data']["result"] = text
        return HttpResponse(json.dumps(data), content_type="application/json")

    return Http404


def image_grayscale_deal(image):
    """
    图片转灰度处理
    :param image:图片文件
    :return: 转灰度处理后的图片文件
    """
    image = image.convert('L')
    # 取消注释后可以看到处理后的图片效果
    # image.show()
    return image

def image_binarizing(image,threshold):
    """
    锐化
    :param image:
    :param threshold: 阀值
    :return:
    """
    pixdata = image.load()
    w, h = image.size
    # 遍历所有像素，大于阈值的为黑色
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return image



def image_thresholding_method(image):
    """
    图片二值化处理
    :param image:转灰度处理后的图片文件
    :return: 二值化处理后的图片文件
    """
    # 阈值，控制二值化程度，自行调整（不能超过256）
    threshold = 200
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    # 图片二值化，此处第二个参数为数字一
    image = image.point(table, '1')
    return image


# 降噪
def image_clear_noise(image):
    """传入二值化后的图片进行降噪"""
    pixdata = image.load()
    w, h = image.size
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            count = 0
            if pixdata[x, y - 1] > 245:  # 上
                count = count + 1
            if pixdata[x, y + 1] > 245:  # 下
                count = count + 1
            if pixdata[x - 1, y] > 245:  # 左
                count = count + 1
            if pixdata[x + 1, y] > 245:  # 右
                count = count + 1
            if pixdata[x - 1, y - 1] > 245:  # 左上
                count = count + 1
            if pixdata[x - 1, y + 1] > 245:  # 左下
                count = count + 1
            if pixdata[x + 1, y - 1] > 245:  # 右上
                count = count + 1
            if pixdata[x + 1, y + 1] > 245:  # 右下
                count = count + 1
            if count > 4:
                pixdata[x, y] = 255
    return image