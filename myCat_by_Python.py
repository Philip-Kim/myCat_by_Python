import time
import threading
from socket import *
from gpiozero import LED

#실제 사용시에는 주석 해제
#cat = LED(15)

#테스트용, 실제 사용시에는 주석처리
class cat:
    @staticmethod
    def on():
        print("cat is on")
 
    @staticmethod
    def off():
        print("cat is off")

#시간에 맞춰 켜고 끄기
class timeCatThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        timeFlag = 0

        while True:
            mytime = int(time.strftime('%H')) + 9

            if (22 <= mytime < 26) and timeFlag == 0:
                cat.on()
                timeFlag = 1
            elif (mytime < 22 or 26 <= mytime) and timeFlag == 1:
                cat.off()
                timeFlag = 0

class remoteCatThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        host="0.0.0.0"
        port=59595

        while True:
            serverSocket = socket(AF_INET, SOCK_STREAM)
            serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

            serverSocket.bind((host,port))
            serverSocket.listen(1)

            connectionSocket,addr = serverSocket.accept()

            data = connectionSocket.recv(1)

            if (data.decode("utf-8") == "0"):
                cat.off()
            elif (data.decode("utf-8") == "1"):
                cat.on()

            serverSocket.close()


#메인시작

#초기화
cat.off()

#Thread 시작
thread1 = timeCatThread()
thread2 = remoteCatThread()
thread1.start()
thread2.start()
