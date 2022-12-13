import math
import os
import sys
import serial
import signal
import struct
import time
import datetime
import threading
import select
import asyncio

#############init#######################
IPC_FIFO_NAME_READ = "node_ext"
IPC_FIFO_NAME_WRITE = "ext_node"

# input_fname = sys.argv[1]
# output_fname = sys.argv[2]
# emergency_fname = sys.argv[3]

# stmを変えたら次のコマンドで確認 ls /dev/serial/by_id/
# use_port = '/dev/serial/by-id/usb-STMicroelectronics_STM32_STLink_066EFF555775514867091844-if02'
use_port = '/dev/serial/by-id/usb-STMicroelectronics_STM32_STLink_066CFF555775514867031038-if02'
# use_port = '/dev/ttyACM0'
# use_port = '/dev/serial/by-id/usb-STMicroelectronics_STM32_STLink_0673FF504982494867085018-if02'
# use_port = 'COM4'

if not os.path.exists(IPC_FIFO_NAME_READ):
    os.mkfifo(IPC_FIFO_NAME_READ)  # Create Pipe to Read
else:
    #clears the pipe
    os.system("rm " + IPC_FIFO_NAME_READ)
    os.mkfifo(IPC_FIFO_NAME_READ)  # Create Pipe to Read

fifo_read = os.open(IPC_FIFO_NAME_READ, os.O_RDONLY | os.O_NONBLOCK)  # pipe is opened as read only and in a non-blocking mode
print('Pipe node_ext ready')

while True:
    while not os.path.exists(IPC_FIFO_NAME_WRITE):
        pass
    
    try:
        fifo_write = os.open(IPC_FIFO_NAME_WRITE, os.O_WRONLY)
        print("Pipe ext_node ready")
        break
    except:
        # Wait until Pipe B has been initialized
        # print("still trying")
        pass
# finally:
#     os.remove(IPC_FIFO_NAME_READ)
#     os.remove(IPC_FIFO_NAME_WRITE)


while True:
    try:
        _serial = serial.Serial(use_port)
        _serial.baudrate = 115200
        time_stamp = "["+str(datetime.datetime.now())+"] "  #タイムスタンプ
        os.write(fifo_write, bytes(time_stamp+"SAX10000Y10000X20000Y20000Z0000A0000L10000L20000", 'utf-8'))
        print("connected!")
        break
    except Exception as e:
        time_stamp = "["+str(datetime.datetime.now())+"] "  #タイムスタンプ
        os.write(fifo_write, bytes(time_stamp+"SBX10000Y10000X20000Y20000Z0000A0000L10000L20000", 'utf-8'))
        print("try connection...")
        time.sleep(1)


stm_sending = False #stmに送っている間はreadしない
exit_flag = False  #thread stop flag
error_flag = True #目標位置に達しているか
getpos_flag = False #positionを受け取ってtimeoutを発火させる(現状は何かしらの値を受け取ったら発火される)
timeout_flag = False #S1がtimeout時間内に目標値に達したか

XT1 = 10
Y_i = 0
X_i = 0
now_X = 0
now_Y = 0
now_arm_pos = [0,0,0,0]
##########################################

def error_write(msg): #S2エラーを上書き, S2は座標がタイムアウトまで似合わなかった場合に出力
    global now_arm_pos
    data_string = ""
    data_item=['X1','Y1','X2','Y2']   #添え字
    time_stamp = "["+str(datetime.datetime.now())+"] "  #タイムスタンプ
    ##########-------OUT.txtに書き込むデータの生成-------##########
    for i in range(0,4):
        data_string += data_item[i]+format(now_arm_pos[i],'04')

    os.write(fifo_write, bytes(time_stamp+msg+data_string+"Z0000A0000L10000L20000", 'utf-8'))

def timeout_handler(start_time):
    txbuf = list(range(20))
    timeout_scale=100      #大きくするとbreaktimeが縮む
    global X_i,Y_i,now_X,now_Y,error_flag,getpos_flag,timeout_flag
    
    print(X_i,Y_i,now_X,now_Y)
    ##最初の値を取得するまで待つ
    txbuf[0]=0xAA
    txbuf[19]=0xAA
    txbuf[1] = 0xCC
    for i in range(2,19):
        txbuf[i]=0xFF
    
    if not getpos_flag:
        error_write("S2")
        if _serial != None:
            send(txbuf)
        print("not respons for STM")

    break_time=int(math.sqrt((X_i-now_X)**2+(Y_i-now_Y)**2)/timeout_scale)
    break_time=5      #breaktime を距離依存にする場合はここをコメントアウトする
    print("break time :"+str(break_time))

    if time.time()-start_time>break_time:
        if(error_flag):
            print("Error : out of alignment")
            error_write("S2")

        else:
            print("In position!")



# def exitHandler(signal, frame):
#     exit_flag=True
#     print("file closed")
#     # f_in.close()
#     _serial.close()
#     sys.exit(0)

# signal.signal(signal.SIGINT, exitHandler)

#####------RASPI->STM --------####################################
def get_message(fifo):
    '''Read n bytes from pipe.'''
    return os.read(fifo, 106)

def send(buf):
    print("stm send data",buf)
    while True:
        if _serial.out_waiting == 0:
            break
    for b in buf:
        a = struct.pack( 'B', b )
        _serial.write(a)
    _serial.flush()

def stm_send( buf ):
    global XT1,Y_i,X_i,stm_sending
    stm_sending=True
    C_i = int(buf[1:3])
    X_i = int(buf[4:8])
    Y_i = int(buf[9:13])
    Z_i= int(buf[14:18])
    A1_i = int(buf[20:24])
    A2_i = int(buf[26:30])
    L1_i = int(buf[32:36])
    L2_i = int(buf[38:42])
    XT1_i = int(buf[81:85])
    # if XT1_i != 0:
    #     XT1 = XT1_i

    
    txbuf = list(range(18))
    txbuf.insert(0,0xAA) #先頭と最後にAAを加える
    txbuf.append(0xAA)
    ##[AA ,cmd,AA]

    ##send command
    if C_i != 0:#コマンドがある場合コマンドを先に送信し座標データを送る
        txbuf[1] = C_i
        for i in range(2,19):
            txbuf[i]=0xFF
        send(txbuf)
        time.sleep(1)
    
    ##send pos
    txbuf[1]=0
    txbuf[2]=0
    txbuf[3]=0
    txbuf[4]=0
    txbuf[5],txbuf[6]=X_i.to_bytes(2, byteorder="little",signed=True)
    txbuf[7],txbuf[8]=Y_i.to_bytes(2, byteorder="little",signed=True)
    txbuf[9],txbuf[10]=Z_i.to_bytes(2, byteorder="little",signed=True)
    txbuf[11],txbuf[12]=A1_i.to_bytes(2, byteorder="little",signed=True)
    txbuf[13],txbuf[14]=A2_i.to_bytes(2, byteorder="little",signed=True)
    txbuf[15],txbuf[16]=L1_i.to_bytes(2, byteorder="little",signed=True) 
    txbuf[17],txbuf[18]=L2_i.to_bytes(2, byteorder="little",signed=True)
    
    # print(txbuf)
    send(txbuf)
    stm_sending=False

######--------STM->RASPI->web----------#################################

def write_output(Rxdata):  #Rxdata is binaly  :ex)b'\xFF\x34\x34...'
    global XT1,Y_i,X_i,error_flag,now_X,now_Y,now_arm_pos,getpos_flag,timeout_flag
    # for i in range(0,int(len(Rxdata)/2)):
    #     data.append(int(Rxdata[i*2:2+(i*2)],16)) ##'FF','FF'-> 255,255

    data_string=""
    data_item=['X1','Y1','X2','Y2','Z','A1','A2','L1','L2']   #添え字
    time_stamp = "["+str(datetime.datetime.now())+"] "  #タイムスタンプ

    getpos_flag = True
    if int.from_bytes(Rxdata[2:4], byteorder='little') != 0xFFFF: #コマンドじゃなければOUT.txtに座標を書き込む
        ##########-------OUT.txtに書き込むデータの生成-------##########
        for i in range(1,19):
            if i%2 == 0:
                # data[i]=data[i]<<8
                data_string += data_item[int(i/2)-1]
                data_string += format(int.from_bytes(Rxdata[i-1:i+1], byteorder='little', signed=True),'04')

        ########ステータスの判定######
        now_X = int.from_bytes(Rxdata[5:7], byteorder='little', signed=True)
        now_Y = int.from_bytes(Rxdata[7:9], byteorder='little', signed=True)
        now_arm_pos = [int.from_bytes(Rxdata[1:3], byteorder='little', signed=True),int.from_bytes(Rxdata[3:5], byteorder='little', signed=True),int.from_bytes(Rxdata[5:7], byteorder='little', signed=True),int.from_bytes(Rxdata[7:9], byteorder='little', signed=True)]

        if abs(X_i-now_X)>=XT1 or abs(Y_i-now_Y)>=XT1: #許容誤差を超えている間はS1
            data_string = "S1"+data_string
            error_flag=True
        else :                                        #目標位置に達するとS0
            data_string = "S0"+data_string
            error_flag=False
        

        if os.path.exists(IPC_FIFO_NAME_WRITE):
            os.write(fifo_write, bytes(time_stamp+data_string, 'utf-8'))
            print("write web",time_stamp+data_string)

    
    # elif int.from_bytes(Rxdata[1], byteorder='little') != 98: #ストールガード
        # error_write("SE")
    
def Task1(): #STM->web
    global stm_sending,getpos_flag,_serial
    while not exit_flag:
        try:
            if(_serial == None):
                _serial = serial.Serial(use_port)
                print("reconnect")
                _serial.baudrate = 115200
                time_stamp = "["+str(datetime.datetime.now())+"] "  #タイムスタンプ
                os.write(fifo_write, bytes(time_stamp+"SAX10000Y10000X20000Y20000Z0000A0000L10000L20000", 'utf-8'))
                 
        
            if not stm_sending and _serial != None:
                # print("reading data")
                Rxdata = _serial.read(20)
                if int.from_bytes(Rxdata[1:3], byteorder='little') == 0xFFFF:
                    print("send error")
                    error_write("S2")
                    continue

                print("read binaly",Rxdata)
                if len(Rxdata) != 0:
                    write_output(Rxdata)
                    Rxdata=0
                # print("file write done")

        except Exception as e:
            if _serial != None:
                _serial.close()
                _serial = None
                print("Disconnecting")
            
            time_stamp = "["+str(datetime.datetime.now())+"] "  #タイムスタンプ
            if os.path.exists(IPC_FIFO_NAME_WRITE):
                os.write(fifo_write, bytes(time_stamp+"SBX10000Y10000X20000Y20000Z0000A0000L10000L20000", 'utf-8'))
            print(e)
            time.sleep(1)
                # _serial.open()


t1 = threading.Thread(target = Task1)
t1.daemon = True
t1.start()


try:
    poll = select.poll()
    poll.register(fifo_read, select.POLLIN)
    start_time=time.time()

    while True: #web->STM
        try:
            # input("enter")
            # f_in = open(input_fname, 'r+')
            # read_data = f_in.readline()

            print("pooling")
            if (fifo_read, select.POLLIN) in poll.poll(1000):  # Poll every 1 sec
                print("received web")
                msg = get_message(fifo_read)                   # Read from Pipe A
                print("read node",msg.decode("utf-8"))
                stm_send(msg.decode("utf-8"))
                start_time=time.time()

            else:
                if os.path.exists(IPC_FIFO_NAME_WRITE):
                    timeout_handler(start_time)


            # if  read_data:
            #     f_in.truncate(0)
            #     getpos_flag = False
            #     stm_send(read_data.strip())
            #     timeout_handler()

            #     read_data=0

        except KeyboardInterrupt:
            print("keybord interrupt main")
            os.remove(IPC_FIFO_NAME_READ)
            os.remove(IPC_FIFO_NAME_WRITE)
            sys.exit(0)
            break
        # except Exception as e:
        #     print(e)
        #     print("error main")
        #     # _serial.open()
        #     time.sleep(1)
finally:
    poll.unregister(fifo_read)