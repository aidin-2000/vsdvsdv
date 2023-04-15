import websocket
import json
import requests

temp=[ 'rfer']
dt="rvbrtvrtv"
def on_message(ws, message):
    global dt
    last=json.loads(message)
    if last["type"]=="round":
        data1=last['data']
        if "rr" in data1:
            rr=data1["rr"]
            if dt!=rr["dt"]:                
                if int(rr["c"])<10 :
                    print(str(rr["c"]))
                    send_Telegram(str(str(rr["c"])+" "+str(rr["c"])))
                else:
                    nummm=str(rr["c"])
                    a1=nummm[0:1]
                    a2=nummm[1:2]
                    print(a1+" "+a2)
                    send_Telegram(str(str(int(a1)+int(a2))+" "+str(rr["c"])))                
                dt=rr["dt"]
                
def on_error(ws, error):
    streamKline()
    print(error)

def on_close(close_msg):
    print("### closed ###" + close_msg)

def streamKline():
    websocket.enableTrace(False)
    socket = 'wss://ringotrade.com/ws/'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()
    
def send_Telegram(text: str):
    token = "5741206806:AAFHkbFfw3EkRp0aXRfWAkWLeAQztwHYtXc"
    url = "https://api.telegram.org/bot"
    channel_id = "-1001814924725"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")

streamKline()
