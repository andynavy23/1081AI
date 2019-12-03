
###=== (5.1) 載入軟件包 ===###  
from flask import Flask, request, abort
from linebot import ( LineBotApi, WebhookHandler )
from linebot.exceptions import( InvalidSignatureError )
from linebot.models import *
import csv

###=== (5.2) 程式宣告 ===###  
app = Flask(__name__)  # __name__ 代表目前執行的模組

###=== (5.3) LINE介面密碼 ===### (參考3.3)
##== (1) Channel Access Token
line_bot_api = LineBotApi("cyhHv06/QDhSh9KpiYzhxQxJNcn4/UqgWazZxVDMG9fTTODbCiGLTX6otM03nf+NG/inIA43HS5aO1fdDifm3YGkpG4ZlPkDTO1Q4bfwNNSEYTkdMSqMwS/8H3mpJ+G+cQmbY4r69sY7XeWIiYyVawdB04t89/1O/w1cDnyilFU=")  #-- YOUR_CHANNEL_ACCESS_TOKEN
##== (2) Channel Secret
handler = WebhookHandler("44438605c6135fcaae7ef26a8840c83e")  #-- YOUR_CHANNEL_SECRET

###=== (5.4) 監聽來自 /callback 的 Post Request  ===###
@app.route("/callback", methods=['POST']) 
def callback():
    print(">>>>>>>>> 1.testing")  # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    print(">>>>>>>>> 2.testing")  # get request body as text
    body = request.get_data(as_text=True)
    print(">>>>>>>>> 3.testing"+body)
    app.logger.info("Request body: " + body)
    print(">>>>>>>>> 4.testing-body:"+body)
    # handle webhook body
    try:
        print(">>>>>>>>> 5.testing-try:...")
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

###=== (5.5) 處理訊息  ===###
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    if event.message.id == "100001":
        return
    text = event.message.text
    if (text=="Hi"):
        reply_text = "Hello"
        #Your user ID
    elif(text=="你好"): 
        reply_text = "你好啊..."
    elif(text=="機器人"):
        reply_text = "有！我是機器人，在！"
    elif(text=="讀取資料"):
        """
        with open('test.csv', newline='') as csvfile:
            rows = csv.reader(csvfile)
            content = " ".join(rows)
        """
        reply_text = "dd"
    else:  # 如果非以上的選項，就會學你說話
        reply_text = text
    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)

###=== (5.6) 執行程式  ===###
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
