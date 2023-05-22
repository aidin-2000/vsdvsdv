import websocket
import requests
import os,ast
dt = "tempdate"
dt1 = "tempdate"
srez="dd"
#european_sequence = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
european_sequence=[26, 3, 35, 12, 28, 7, 29, 18, 22, 9, 31, 14, 20, 1, 33, 16, 24, 5, 10, 23, 8, 30, 11, 36, 13, 27, 6, 34, 17, 25, 2, 21, 4, 19, 15, 32,0]

result=[]
tempfac=[ 'rfer']
tempfac2=['ff']
tempfac1=['fssf']
tempfac007=[]
facc=[]
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
        tv=str(data1["tv"])
        sv=str(data1["sv"])
        sd=str(data1["sd"])
        if sd!=dt1:
            facc=data1["cls"]
            
            #for i in range(0,37,1):
                #facc[i]['c']=european_sequence[i]
            srez=sv[6:7]
            dt1=sd
        if "rr" in data1:
            rr = data1["rr"]
            if dt != rr["dt"]:
                c = int(rr["c"])
                v = rr["v"]

                #print("Выпало число = " + str(find_range(v,facc)))
                send_Telegram(str(c))
                send_Telegram(str(v))

                dt = rr["dt"]
    if last["type"]=="factors":
        datafacfac=last['data']
        if datafacfac[len(datafacfac)-1]["dt"] != tempfac[0]:
            tempfac[0]=datafacfac[len(datafacfac)-1]["dt"]
            c=datafacfac[len(datafacfac)-1]["v"]
       
            #result = find_range(c,facc)
            tempfac007.append(c)
            if len(tempfac007)==150:
                send_Telegram(str(tempfac007))
                tempfac007.clear()
            if len(tempfac007)>150:
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
    
def find_range(number, ranges):
    for rng in ranges:
        if  number<= rng['vt'] and number >= rng['vf']:
            print(rng['vt'], number, rng['vf'],rng['c'])
            return rng['c']
    return None

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
