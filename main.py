import websocket
import requests
dt = "tempdate"
dt1 = "tempdate"
def on_error(ws,error):
    print(str("Проблема с подключением к интернету! Подробнее : " + str(error)))
    print("Попытка подключится заново!")
    main()


def on_close(close_msg):
    print("Подключение закрыто! " + str(close_msg))


def on_message(ws,message):
    global dt,dt1,srez,result,facc
    last = eval(message)

    if last["type"] == "round":
        data1 = last['data']
        sd=str(data1["sd"])
        if sd!=dt1:
            dt1=sd
        if "rr" in data1:
            rr = data1["rr"]
            if dt != rr["dt"]:
                c = int(rr["c"])
                send_Telegram(str(c))
                dt = rr["dt"]
    
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
    
def main():
    websocket.enableTrace(False)
    socket = 'wss://ringotrade.com/ws/'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()

if __name__ == '__main__':
    main()
