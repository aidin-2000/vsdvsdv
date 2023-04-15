import websocket
import datetime
import json

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
                print("c = "+str(rr["c"])+" :: v = "+str(rr["v"])+" :: sv = "+str(data1["sv"])+" :: tv = "+str(data1["tv"]))
                file=open("number1111111111.txt","a")
                file1=open("number222222222.txt","a")
                file2=open("number1111.txt","a")
                file3=open("number.txt","a")
                file3.write(str(rr["c"])+"\n")
                file3.close()

                streamKline11()

                if int(rr["c"])<10 :
                    print(str(rr["c"]))
                    file.write(str(rr["c"])+"\n")
                    file2.write(str(rr["c"])+"\n")
                    file1.write(str(rr["c"])+" "+str(rr["c"])+"\n")

                else:
                    nummm=str(rr["c"])
                    a1=nummm[0:1]
                    a2=nummm[1:2]
                    print(a1+" "+a2)
             
                    file.write(str(int(a1)+int(a2))+"\n")
                    file2.write(str(int(a1)+int(a2))+"\n")

                    file1.write(str(int(a1)+int(a2))+" "+str(rr["c"])+"\n")

                    
                file.close()
                file1.close()
                file2.close()

                
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
def streamKline11():
    previous_numbers = []
    f=open("number.txt")
    file1=open("number555555555.txt","w")

    for line in f:
        previous_numbers.append(int(line))
    for i in range(0,len(previous_numbers)-1,1):
        if int(previous_numbers[i])>int(previous_numbers[i+1]):
            file1.write(str(int(previous_numbers[i])-int(previous_numbers[i+1]))+"\n")
        else:
            file1.write(str(int(previous_numbers[i])-int(previous_numbers[i+1]))+"\n")

    f.close()
    file1.close()

streamKline()
