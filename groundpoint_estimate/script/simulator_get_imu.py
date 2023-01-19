import mmap
import time
import struct
import time
import math
import multiprocessing
import numpy as np
from matplotlib import pyplot as plt


WORD_SIZE = 72
READ_WORD_SIZE=56
MMAP_FILE_NAME = "hoge"
mm = mmap.mmap(-1, WORD_SIZE, tagname=MMAP_FILE_NAME)

class IMU:
    def __init__(self):#constructor

        self.count = 0
        self.ut = time.time()
        self.pre_time_stamp = 0

        self.acc=[0] * 3

        self.gyro_deg = [0] * 3
        self.gyro = [0] * 3
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.pregx = 0
        self.pregy = 0
        self.pregz = 0

        self.pre_filter_roll =0
        self.pre_filter_pitch=0
        self.pre_filter_yaw=0

        
        self.degree = 0

#バイナリデータの上位と下位を計算
    def BinaryCalc (self ,low_bit, high_bit):
        Low_data=low_bit
        High_data=high_bit << 8
        Data =Low_data + High_data

        if Data >= 32767:
            Data = Data -65535

        return Data

    
    def get_gyro_degree(self,gyro,dt):
        self.roll += (self.pregx + gyro[0])*dt / 2
        self.pregx = gyro[0]


        self.pitch += (self.pregy + gyro[1]) * dt / 2
        self.pregy = gyro[1]

        self.yaw += (self.pregz + gyro[2]) * dt / 2
        self.pregz = gyro[2]

        self.roll  += self.pitch * math.sin(gyro[2] * dt * math.pi/180) ;   
        self.pitch -= self.roll * math.sin(gyro[2] * dt* math.pi/180) ; 
        
        return self.roll , self.pitch , self.yaw


    def get_acc_degree(self,acc):

        ax = acc[0]
        ay = acc[1]
        az = acc[2]
         
        acc_pitch = math.degrees(math.atan2(ax, math.sqrt(ay * ay + az * az))) #* math.pi/180


        # roll        
        acc_roll  = -math.degrees(math.atan2(ay, az))# * math.pi/180
        if acc_roll >= 0:
            acc_roll = 180 - acc_roll
        if acc_roll < 0 :
            acc_roll = -180 - acc_roll

        return acc_roll,acc_pitch
    
    def GetSensorData(self ,recv_data ,calib_data ,debug = True):

        time_stamp = time.time() - self.ut
        dt=time_stamp - self.pre_time_stamp
        self.pre_time_stamp=time_stamp
    

        # get raw data
        self.acc[0] =recv_data[1]
        self.acc[1] =recv_data[2]
        self.acc[2] =recv_data[3]
        self.gyro[0] = math.degrees(recv_data[4])/6.2
        self.gyro[1] = math.degrees(recv_data[5])/6.2
        self.gyro[2] = math.degrees(recv_data[6])/6.2
   

        self.gyro_deg = self.get_gyro_degree(self.gyro,dt)
        acc_roll,acc_pitch = self.get_acc_degree(self.acc)

        # filter degree
        filter_roll = 0.99 * (self.pre_filter_roll + self.gyro[0] * dt) + 0.01 * acc_roll
        self.pre_filter_roll=filter_roll
        filter_pitch = 0.99 * (self.pre_filter_pitch + self.gyro[1] * dt) + 0.01 * acc_pitch
        self.pre_filter_pitch=filter_pitch

        if debug:
            print("time stamp, dt :"+f'{time_stamp:11.06f}'+f'{dt:11.06f}')
            print("recv raw data  :",recv_data )
            print("Acc x y z      :"+f'{self.acc[0]:11.06f}'+f'{self.acc[1]:11.06f}'+f'{self.acc[2]:11.06f}')
            print("Gyro x y z     :"+f'{self.gyro[0]:11.06f}'+f'{self.gyro[1]:11.06f}'+f'{self.gyro[2]:11.06f}')
            print("gyro deg       :"+f'{self.gyro_deg[0]:11.06f}'+f'{self.gyro_deg[1]:11.06f}'+f'{self.gyro_deg[2]:11.06f}')
            print("acc deg        :"+f'{acc_roll:11.06f}'+f'{acc_pitch:11.06f}') 
            print("filtering roll :"+f'{filter_roll:11.06f}')
            print("filtering pitch:"+f'{filter_pitch:11.06f}')
            print("\033[9A",end="")

    
        return [time_stamp, filter_roll, filter_pitch]

def read_imu(imu_data,calib_data):
    global mm ,WORD_SIZE,READ_WORD_SIZE
    imu = IMU()

    cnt = 0

    # アドレス0番地の値をインクリしていく
    while True:
        try:
            # cnt += 1
            # mmapWriteShort(0, cnt)
            # print(mmapReadShort(0))
            imu_data[0],imu_data[1],imu_data[2] = imu.GetSensorData(mmapReadShort(mm,READ_WORD_SIZE,0),calib_data,False)
            filter_data = imu_data[1]-calib_data[0],imu_data[2]-calib_data[1]
            # print(filter_data)
            time.sleep(0.01)
        except KeyboardInterrupt:
            mm.close()

def zero_calib(imu_data,calib_data):

    roll=[]
    pitch=[]
    for i in range(100):
        roll.append(float(imu_data[1]))
        pitch.append(float(imu_data[2]))
        time.sleep(0.01)
    calib_data[0] = np.mean(roll)
    calib_data[1] = np.mean(pitch)
    print(calib_data[0],calib_data[1])

def plot_imu(imu_data,calib_data):
    # global imu_data
    #plot init 
    t = np.zeros(100)
    roll = np.zeros(100)
    pitch =np.zeros(100)

    r = np.zeros(100)

    plt.ion()
    plt.figure()
    li_roll, = plt.plot(t, roll,label='roll')
    li_pitch, = plt.plot(t, pitch,label='pitch')
    li, = plt.plot(t, r)
    # plt.ylim(0, 5)
    plt.xlabel("time[s]")
    plt.ylabel("angle")

    while(1):
        t = np.append(t, float(imu_data[0]))
        t = np.delete(t, 0)
        roll = np.append(roll, float(imu_data[1])-calib_data[0])
        roll = np.delete(roll, 0)
        pitch = np.append(pitch , float(imu_data[2])-calib_data[1])
        pitch = np.delete(pitch , 0)
        li_roll.set_xdata(t)
        li_roll.set_ydata(roll)     
        li_roll.set_label("roll")      
        li_pitch.set_xdata(t)
        li_pitch.set_ydata(pitch)           
        li.set_xdata(t)
        li.set_ydata(r)           
        plt.xlim(min(t), max(t))
        plt.ylim(min(min(roll),min(pitch))-5, max(max(roll),max(pitch))+5)
        # plt.ylim(-30, 30)

        # print("roll pitch:"+str(float(imu_data[1])-calib_data[0])+str(float(imu_data[2])-calib_data[1]))
        # print("\033[1A",end="")

        plt.pause(0.01)

def mmapWriteShort(adr:int, data):
    '''
    指定のアドレスに値を書き込む(Shortデータ)
    '''
    global mm,WORD_SIZE,READ_WORD_SIZE

    try:
        val = mmapReadShort(mm,READ_WORD_SIZE,0)
        ddata = list(val)+data
        # bytes = ddata.to_bytes(WORD_SIZE, 'little',signed=True)
        bytes = struct.pack('ddddddddd', *ddata)
        for i in range(WORD_SIZE):
            mm[adr*WORD_SIZE + i] = bytes[i]
        
        print("write done")
    except Exception as e:
        print(e)

def mmapReadShort(mm, WORD_SIZE,adr:int):
    """指定のアドレスの値を読み込む(Shortデータ)

    Args:
        adr : Shared memory address
    # """    
    # global mm
    # try:
    mm.seek(adr*WORD_SIZE)
    bytes = mm.read(WORD_SIZE)
    # print(bytes[0:8])
    # val = int.from_bytes(bytes, 'little',signed=True)
    val = struct.unpack('ddddddd', bytes)
    # print(val)
    # val = bytes.decode('Shift-JIS')
    mm.seek(0)
    return val
    # except KeyboardInterrupt:
    #     print("error")
    #     return None



if __name__ == "__main__":
    # 名前付き共有メモリの作成
    # 1つ目の引数を−1にすることで、ファイルなしの共有メモリを生成できる
    # （tagname=Noneの場合は無名共有メモリとなる）
    calib_data = multiprocessing.Array('d', 2) 
    imu_data = multiprocessing.Array('d', 3)

    p1 = multiprocessing.Process(name="p1", target=read_imu, args=(imu_data,calib_data),daemon=False)
    p2 = multiprocessing.Process(name="p2", target=plot_imu, args=(imu_data,calib_data),daemon=False)

    p1.start()
    p2.start()

    while True :
        input()
        print("start estimation")
        zero_calib(imu_data,calib_data)
        print("move 1")
        mmapWriteShort(0,[-math.pi*0.1,0])
        time.sleep(5)
        print("move 2")
        mmapWriteShort(0,[-math.pi*0.1,-math.pi*0.10])
        time.sleep(5)
        print("move 3")
        mmapWriteShort(0,[0,-math.pi*0.1])
        time.sleep(5)
        print("move 4")
        mmapWriteShort(0,[-math.pi*0.1,-math.pi*0.10])
        time.sleep(5)
        mmapWriteShort(0,[0,0])