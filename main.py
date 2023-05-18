import websocket
import requests
import os
dt = "tempdate"
dt1 = "tempdate"
srez="dd"
european_sequence = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
result=[]
tempfac=[ 'rfer']
tempfac2=['ff']
tempfac1=['fssf']
tempfac007=[]
def on_error(ws,error):
    print(str("Проблема с подключением к интернету! Подробнее : " + str(error)))
    print("Попытка подключится заново!")
    main()


def on_close(close_msg):
    print("Подключение закрыто! " + str(close_msg))


def on_message(ws,message):
    global dt,dt1,srez,result
    last = eval(message)

    if last["type"] == "round":
        data1 = last['data']
        tv=str(data1["tv"])
        sv=str(data1["sv"])
        sd=str(data1["sd"])
        if sd!=dt1:
            srez=sv[6:7]
            dt1=sd
        if "rr" in data1:
            rr = data1["rr"]
            if dt != rr["dt"]:
                c = int(rr["c"])
                print("Выпало число = " + str(c))
                send_Telegram(str(c))
                dt = rr["dt"]
    if last["type"]=="factors":
        datafacfac=last['data']
        if datafacfac[len(datafacfac)-1]["dt"] != tempfac[0]:
            tempfac[0]=datafacfac[len(datafacfac)-1]["dt"]
            c=datafacfac[len(datafacfac)-1]["v"]
            ccc=str(c)
            tempfac007.append(ccc)
            if len(tempfac007)==150:
                send_Telegram(str(tempfac007))
                tempfac007.clear()


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
    print("Старт")
    main()
