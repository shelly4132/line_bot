from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import urllib.request
import urllib.error 
import sys
import xml.etree.ElementTree as etree

targetURL = "http://opendata.cwb.gov.tw/opendataapi?dataid=F-C0032-001&authorizationkey=" + settings.AUTHORIZATION_KEY


# get the weather from place

def getWeather(place):
    try:
        weatherData = urllib.request.urlopen(targetURL, data=None)
    except urllib.error.HTTPError as e:
        print("HTTP error: " + str(e) + " URL: " + targetURL)
        sys.exit()

    tree = etree.parse(weatherData)
    root = tree.getroot()


    for location in root.findall('.//{urn:cwb:gov:tw:cwbcommon:0.1}location'):
        name  = location.find('.//{urn:cwb:gov:tw:cwbcommon:0.1}locationName').text
        if place in name:
            weather = location.find('.//{urn:cwb:gov:tw:cwbcommon:0.1}parameterName').text
            return weather



def replySentence(msg):
    if '天氣' in msg:
        if '臺北市' in msg:
            return '臺北市' + getWeather('臺北市')
        elif '新北市' in msg:
            return '新北市' + getWeather('新北市')
        elif '桃園市' in msg:
            return '桃園市' + getWeather('桃園市')
        elif '臺中市' in msg:
            return '臺中市' + getWeather('臺中市')
        elif '臺南市' in msg:
            return '臺南市' + getWeather('臺南市')
        elif '高雄市' in msg:
            return '高雄市' + getWeather('高雄市')
        elif '基隆市' in msg:
            return '基隆市' + getWeather('基隆市')
        elif '新竹縣' in msg:
            return '新竹縣' + getWeather('新竹縣')
        elif '新竹市' in msg:
            return '新竹市' + getWeather('新竹市')
        elif '苗栗縣' in msg:
            return '苗栗縣' + getWeather('苗栗縣')
        elif '彰化縣' in msg:
            return '彰化縣' + getWeather('彰化縣')
        elif '南投縣' in msg:
            return '南投縣' + getWeather('南投縣')
        elif '雲林縣' in msg:
            return '雲林縣' + getWeather('雲林縣')
        elif '嘉義縣' in msg:
            return '嘉義縣' + getWeather('嘉義縣')
        elif '嘉義市' in msg:
            return '嘉義市' + getWeather('嘉義市')
        elif '屏東縣' in msg:
            return '屏東縣' + getWeather('屏東縣')
        elif '宜蘭縣' in msg:
            return '宜蘭縣' + getWeather('宜蘭縣')
        elif '花蓮縣' in msg:
            return '花蓮縣' + getWeather('花蓮縣')
        elif '臺東縣' in msg:
            return '臺東縣' + getWeather('臺東縣')
        elif '澎湖縣' in msg:
            return '澎湖縣' + getWeather('澎湖縣')
        elif '金門縣' in msg:
            return '金門縣' + getWeather('金門縣')
        elif '連江縣' in msg:
            return '連江縣' + getWeather('連江縣')
        else:
            return '臺南市' + getWeather('臺南市')
    else:
        return msg


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    sentence = replySentence(event.message.text)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=sentence)
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
