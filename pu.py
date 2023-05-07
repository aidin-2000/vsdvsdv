import websocket
import requests
import os
dt = "tempdate"
dt1 = "tempdate"
srez="dd"
european_sequence = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
result=[]
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
                write_to_files(c)
                rangeSequenceSub()
                pp1="rangeЧисло.txt"
                pp2="Числа1-Число2.txt"
                oo1="rangeNumber.txt"
                oo2="Выпавшие_числа.txt"
                find_distance_Main(pp1,pp2)
                find_distance_Main(oo1,oo2)

                find_next_Main()
                start=2
                endr=37
                n8=[]
                n9=[]
                kk=0
                if start==1:
                    if c in result:
                        kk=1
                        print("Успешно!")
                        send_Telegram("Успешно!")
                    else:
                        kk=0
                        print("Провалена!")
                        send_Telegram("Провалена!")
                    with open("test.txt", "a") as number_file:
                        number_file.write(str(kk) + "\n")

                    for i in range(1,endr,1):
                        rangeSequence(i)
                    for i in range(1,endr,1):
                        n1=getNumbers(c,i,-1)
                        n8+=n1
                    seq=[]
                    for i in range(0,37,1):
                        if i not in n8:
                            seq.append(i)
                    print(seq)
                    send_Telegram(str(seq))
                    result=seq
                    #print(n9)
                dt = rr["dt"]

def write_to_files(c):
    with open("Выпавшие_числа.txt", "a") as number_file:
        number_file.write(str(c) + "\n")
  
def getNumbers(c,n,vv):
    rangeSequenceArr = []
    with open("растояние"+str(n)+".txt") as file:
        for line in file:
            rangeSequenceArr.append(int(line))
    seq=rangeSequenceArr[int(vv):]
    seqArr=seq[:35]
    nextArr=get_european_sequence(int(c))
    stavka=[]
    st=[]
    for i in range(0,37,1):
        if i not in seq:
            stavka.append(i)
            st.append(nextArr[i])
    #print(stavka)
    #print(nextArr)
    return seq

def rangeSequence(n):
    previous_numbers = []
    with open("Выпавшие_числа.txt") as file:
        for line in file:
            previous_numbers.append(int(line))
    european_sequence = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
 
    with open("растояние"+str(n)+".txt", "w") as number_file:
        for i in range(n,len(previous_numbers),1):
            a1=previous_numbers[i]
            a2=n#previous_numbers[i-n]
            index1=european_sequence.index(a1)
            index2=european_sequence.index(a2)
            distance = abs(index2 - index1)

            if index2>index1:
                distance=37-distance#*-1
            #if distance <-15:
                #distance=37-abs(distance)
            #if distance>=22:
                #distance=distance-37
            number_file.write(str(distance) + "\n")
    #print("Дистанция от числа "+str(a2) +" до числа "+str(a1)+" = "+str(distance))
#european_sequence = [9, 31, 14, 20, 1, 33, 16, 24, 5, 10, 23, 8, 30, 11, 36, 13, 27, 6, 34, 17, 25, 2, 21, 4, 19, 15, 32, 0, 26, 3, 35, 12, 28, 7, 29, 18, 22]

def rangeSequenceSub():
    previous_numbers = []
    with open("Выпавшие_числа.txt") as file:
        for line in file:
            previous_numbers.append(int(line))
    with open("Числа1-Число2.txt", "w") as number_file:
        for i in range(0,len(previous_numbers)-1,1):
            a1=previous_numbers[i]
            a2=previous_numbers[i+1]
            number_file.write(str(int(a1)-int(a2)) + "\n")

def get_european_sequence(start_number):
    """
    Возвращает последовательность чисел в европейской рулетке, начиная с заданного числа.
    """
    start_index = european_sequence.index(start_number)
    sequence = european_sequence[start_index:] + european_sequence[:start_index]
    return sequence

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
    

def find_distance(lst, x):
   
    indices = [i for i, elem in enumerate(lst) if elem == x] # находим все индексы элемента x в списке lst
    if len(indices) < 2: # если элемент x встречается менее 2 раз, то расстояние равно 0
        return 0
    else:
        rng=[]
        for i in range(1,len(indices),1):
            rng.append(indices[i]-indices[i-1])
        return rng # вычисляем расстояние между первым и последним индексом элемента x в списке lst
def find_distance_Main(path1,path2):
    lst=[]
    os.remove(path1)
    with open(path2) as file:
        for line in file:
            lst.append(int(line))
    my_list = lst
    new_list = sorted(list(set(my_list)))
    for num in new_list:
        distance = find_distance(lst,num)
        if distance!=0:
            with open(path1, "a") as number_file:
                number_file.write(str(distance)+" "+ str(num) + "\n")
  
def find_next(lst, x):
    
    indices = [i for i, elem in enumerate(lst) if elem == x] # находим все индексы элемента x в списке lst
    if len(indices) < 2: # если элемент x встречается менее 2 раз, то расстояние равно 0
        return 0
    else:
        rng=[]
        for i in indices:
            if i<len(lst)-1:
                rng.append(lst[i+1])
        return rng # вычисляем расстояние между первым и последним индексом элемента x в списке lst
def find_next_Main():
    lst=[]
    os.remove("nextЧисло.txt")
    with open("Выпавшие_числа.txt") as file:
        for line in file:
            lst.append(int(line))
    my_list = lst
    new_list = sorted(list(set(my_list)))
    for num in new_list:
        distance = find_next(lst,num)
        if distance!=0:
           with open("nextЧисло.txt", "a") as number_file:
                number_file.write(str(distance)+" "+ str(num) + "\n")

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
