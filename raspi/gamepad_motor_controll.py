import pygame
import time
import sys
sys.path.append('/home/pi/git/ALACRAN/raspi/B3M/')
import b3mCtrl
import pigpio
import math
import serial

##########B3M初期化##########################
aaa = b3mCtrl.B3mClass()
aaa.begin("/dev/ttyUSB0",1500000)

idx= [1,2,3]

for id in range(len(idx)):
    print(aaa.setMode(idx[id],"FREE"))
    time.sleep(0.01)
    
    print(aaa.setMode(idx[id],"SPEED"))
    time.sleep(0.01)
    
    hoge = aaa.setRam(idx[id], 0, "DesiredVelosity")
    time.sleep(0.01)


print(aaa.setMode(4,"FREE"))
time.sleep(0.01)

print(aaa.setMode(4,"TORQUE"))
time.sleep(0.01)

hoge = aaa.setRam(4, 1000, "DesiredTorque")
time.sleep(0.01)


################maxon motor初期化###############
pwm_left = 19
pwm_right = 18
DIRpin_left = 16
DIRpin_right = 20

pi = pigpio.pi()
pi.set_mode(pwm_left, pigpio.OUTPUT)
pi.set_mode(pwm_right, pigpio.OUTPUT)
pi.set_mode(DIRpin_left, pigpio.OUTPUT)
pi.set_mode(DIRpin_right, pigpio.OUTPUT)

# pygame初期化
pygame.init()                             #pygameに必要な全てのモジュールが初期化される
joystick = pygame.joystick.Joystick(0)    #ジョイスティックオブジェクトを新規作成
joystick.init()                           #ジョイスティックの初期化


# ジョイスティックの出力数値を調整
def map_axis(val):
    val = round(val, 2)
    in_min = -1
    in_max = 1
    out_min = -100
    out_max = 100
    return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


# ジョイスティックの出力数値を調整(L2 R2ボタン)
def map_axis_t(val):
    val = map_axis(val)
    if val <= 0 and val >= -100:
        in_min = -100
        in_max = 0
        out_min = 0
        out_max = 50
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    else:
        in_min = 0
        in_max = 100
        out_min = 50
        out_max = 100
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def main():
    FB_val=0
    Lmotor_val=0
    Rmotor_val=0
    ctr_mode=0
    cnt=0
    while True:
        # イベントチェック
        if pygame.event.get():   #新しいイベントを追加する前にイベントのキューを空にする(ゲームは一連の流れになるため)
            if map_axis_t(joystick.get_axis(5)) == 0 and map_axis_t(joystick.get_axis(2)) == 0: #最初にR2L2が0になっていることを確認
                if joystick.get_button(0):    #現在のボタンの状態を取得する
                    ctr_mode=1
                    print("move_mode")
                elif joystick.get_button(1) :
                    ctr_mode=2
                    print("flipper_mode")
                    for id in range(len(idx)):
                        print(aaa.setMode(idx[id],"FREE"))
                        time.sleep(0.01)

                        print(aaa.setMode(idx[id],"SPEED"))
                        time.sleep(0.01)

                        hoge = aaa.setRam(idx[id], 0, "DesiredVelosity")
                        time.sleep(0.01)
                    
                    print(aaa.setMode(4,"FREE"))
                    time.sleep(0.01)
                    print(aaa.setMode(4,"TORQUE"))
                    time.sleep(0.01)
                    hoge = aaa.setRam(4, 1000, "DesiredTorque")
                    time.sleep(0.01)

                elif joystick.get_button(2) :
                    ctr_mode=3
                    print("turbo_mode")


            if ctr_mode == 1: #走行モード
                FB_val =map_axis_t(joystick.get_axis(5)) - map_axis_t(joystick.get_axis(2))
                Lmotor_val = (FB_val) * 5000
                Rmotor_val = (FB_val) * 5000

                if FB_val>=10:
                    if map_axis(joystick.get_axis(0))>=0:
                        Rmotor_val -= map_axis(joystick.get_axis(0))*3000
                    else:
                        Lmotor_val += map_axis(joystick.get_axis(0))*3000
                    # print(FB_val,Lmotor_val,Rmotor_val)
                elif FB_val<-10:
                    if map_axis(joystick.get_axis(0))>=0:
                        Rmotor_val += map_axis(joystick.get_axis(0))*3000
                    else:
                        Lmotor_val -= map_axis(joystick.get_axis(0))*3000
                    # print(FB_val,Lmotor_val,Rmotor_val)
                else:
                    Lmotor_val -= map_axis(joystick.get_axis(0))*3000
                    Rmotor_val += map_axis(joystick.get_axis(0))*3000
                
                if Lmotor_val >= 0:
                    pi.write(DIRpin_left, 0)
                elif Lmotor_val < 0:
                    pi.write(DIRpin_left, 1)
                if Rmotor_val >= 0:  
                    pi.write(DIRpin_right, 0)
                elif Rmotor_val < 0:  
                    pi.write(DIRpin_right, 1)

                pi.hardware_PWM(pwm_left,10000,abs(int(Lmotor_val)))
                pi.hardware_PWM(pwm_right,10000,abs(int(Rmotor_val)))
                print(pi.read(DIRpin_left),abs(Lmotor_val),abs(Rmotor_val))

                cnt=0

            elif ctr_mode ==2: #フリッパー操作モード
                tail =5000*(map_axis_t(joystick.get_axis(5)) - map_axis_t(joystick.get_axis(2)))
                flipperL = -map_axis(joystick.get_axis(1))
                flipperR = -map_axis(joystick.get_axis(4)) 
                print(flipperL,flipperR)

                if tail>=10:
                    hoge = aaa.setRam(idx[2], 10000, "DesiredVelosity")
                    time.sleep(0.01)
                elif tail<-10:
                    hoge = aaa.setRam(idx[2], -10000, "DesiredVelosity")
                    time.sleep(0.01)
                else:
                    hoge = aaa.setRam(idx[2], 0, "DesiredVelosity")
                    time.sleep(0.01)
                

                if flipperL >50:
                    print("LUP")
                    hoge = aaa.setRam(idx[0], -20000, "DesiredVelosity")
                    time.sleep(0.01)

                elif flipperL < -50:
                    print("LDOWN")
                    hoge = aaa.setRam(idx[0], 20000, "DesiredVelosity")
                    time.sleep(0.01)
                else :
                    hoge = aaa.setRam(idx[0], 0, "DesiredVelosity")
                    time.sleep(0.01)

                
                if flipperR > 50:
                    print("RUP")
                    hoge = aaa.setRam(idx[1], 20000, "DesiredVelosity")
                    time.sleep(0.01)
 
                elif flipperR < -50:
                    print("RDOWN")
                    hoge = aaa.setRam(idx[1], -20000, "DesiredVelosity")
                    time.sleep(0.01)
                else :
                    hoge = aaa.setRam(idx[1], 0, "DesiredVelosity")
                    time.sleep(0.01)
                
                cnt=0

            elif ctr_mode ==3: #ターボ走行モード
                FB_val =map_axis_t(joystick.get_axis(5)) - map_axis_t(joystick.get_axis(2))
                Lmotor_val = (FB_val) * 5000*2
                Rmotor_val = (FB_val) * 5000*2

                if FB_val>=10:
                    if map_axis(joystick.get_axis(0))>=0:
                        Rmotor_val -= map_axis(joystick.get_axis(0))*3000
                    else:
                        Lmotor_val += map_axis(joystick.get_axis(0))*3000
                    # print(FB_val,Lmotor_val,Rmotor_val)
                elif FB_val<-10:
                    if map_axis(joystick.get_axis(0))>=0:
                        Rmotor_val += map_axis(joystick.get_axis(0))*3000
                    else:
                        Lmotor_val -= map_axis(joystick.get_axis(0))*3000
                    # print(FB_val,Lmotor_val,Rmotor_val)
                else:
                    Lmotor_val -= map_axis(joystick.get_axis(0))*3000
                    Rmotor_val += map_axis(joystick.get_axis(0))*3000
                
                if Lmotor_val >= 0:
                    pi.write(DIRpin_left, 0)
                elif Lmotor_val < 0:
                    pi.write(DIRpin_left, 1)
                if Rmotor_val >= 0:  
                    pi.write(DIRpin_right, 0)
                elif Rmotor_val < 0:  
                    pi.write(DIRpin_right, 1)

                pi.hardware_PWM(pwm_left,10000,abs(int(Lmotor_val)))
                pi.hardware_PWM(pwm_right,10000,abs(int(Rmotor_val)))
                print(pi.read(DIRpin_left),abs(Lmotor_val),abs(Rmotor_val))
                
                cnt=0
            
            elif ctr_mode == 4: #アーム操縦モード
                #READコマンド
                #メモリーマップ(RAM)のアドレスを指定してデバイスからRAMデータを読み込みます。
                if cnt == 0:
                    def B3M_Read_CMD(servo_id, Data_size, Address):

                        #送信コマンドを作成
                        txCmd = [0x07,      #SIZE
                                0x03,      #CMD
                                0x00,      #OPTION
                                servo_id,  #ID
                                Address,   #ADDRRESS
                                Data_size]      #LENGTH

                        #チェックサムを用意
                        checksum = 0
                        for i in txCmd:
                            checksum += i
                            
                        #リストの最後にチェックサムを挿入する
                        txCmd.append(checksum & 0xff)
                        
                        #WRITEコマンドを送信
                        b3m.write(txCmd)
                        
                        #サーボからの返事を受け取る
                        rxCmd = b3m.read(5+Data_size)
                        
                        #もしリスト何になにも入っていなかったら正常に受信できていないと判断    
                        if len(rxCmd) == 0:
                            return False, 0

                        #問題なければデータを返す
                        #1Byteの場合
                        if Data_size == 1:
                            return True, rxCmd[4]

                        #2Byteの場合
                        elif Data_size == 2:
                            Value = [rxCmd[4], rxCmd[5]]
                            
                            #データの範囲にマイナスが含まれる場合
                            if (Address == 0x05     #最小位置制御
                                or Address == 0x07  #最大位置制御
                                or Address == 0x09  #中央値オフセット
                                or Address == 0x0B  #MCU温度リミット
                                or Address == 0x0E  #モーター温度リミット
                                or Address == 0x2A  #目標位置
                                or Address == 0x2C  #現在位置
                                or Address == 0x2E  #前回のサンプリングの位置
                                or Address == 0x30  #目標速度
                                or Address == 0x32  #現在速度
                                or Address == 0x34  #前回のサンプリングの速度
                                or Address == 0x3C  #目標トルク
                                or Address == 0x44  #現在のMCU温度
                                or Address == 0x46):#現在のモーター温度
                            
                                Value = int.from_bytes(Value, 'little', signed=True)

                            #データの範囲がプラスのみの場合
                            else:
                                Value = int.from_bytes(Value, 'little')
                            
                            return True, Value


                        #4Byteの場合    
                        elif Data_size == 4:
                            Value = [rxCmd[4], rxCmd[5], rxCmd[6], rxCmd[7]]
                            Value = int.from_bytes(Value, 'little')
                            return True, Value
                            
                        else:
                            return False, 0


                    #COMポートを開く
                    b3m = serial.Serial('/dev/ttyUSB0', baudrate=1500000, parity=serial.PARITY_NONE, timeout=0.5)

                    #ロボットアーム・ハンドのサーボID
                    idy = [6,7,8,9,10,11,12]
                    #サーボの現在角度
                    reDatas = [0,0,0,0,0,0,0]

                    for id in range(len(idy)):

                        #B3M_Read_CMD(servo_id, Data_size, Address)
                        #ID番号を読み込む(ID:0,1byte読み込み,アドレス：0x00(ID))
                        bl, reData = B3M_Read_CMD(idy[id], 1, 0x00)
                        print(bl, reData)

                        #現在位置を読み込む(ID:0,2byte読み込み,アドレス：0x2C(現在位置))
                        bl, reDatas[id-6] = B3M_Read_CMD(idy[id], 2, 0x2C)
                        print(bl, reDatas[id-6])

                        #通信速度を読み込む(ID:0,4byte読み込み,アドレス：0x01(通信速度))
                        bl, reData = B3M_Read_CMD(idy[id], 4, 0x01)
                        print(bl, reData)

                    angles = [n/100 for n in reDatas]
                    #各B3Mの角度を表示
                    print(angles)
                    
                    #ポートを閉じる
                    b3m.close()
                    
                    #アーム長さ
                    L1 = 352
                    L2 = 300

                    #現在関節角度
                    th0 = angles[6]
                    thA = (abs(angles[7]) + angles[8])/2
                    thB = round(thA, 2)
                    th1 = thB - 78
                    th2 = angles[9] - 84

                    # s =(L2cosθ2-L1cosθ1)
                    s = L2* (math.cos(math.radians(th2))) - L1* (math.cos(math.radians(th1)))
                    print(s)

                    #順運動学
                    x = s* (math.cos(math.radians(th0)))
                    X = round(x, 2)
                    y = L1* (math.sin(math.radians(th1))) + L2* (math.sin(math.sin(th2)))
                    Y = round(y, 2)
                    z = s* (math.sin(math.radians(th0)))
                    Z = round(z, 2)
                    
                    #手首座標出力
                    print(X, Y, Z)
                    
                    cnt +=1
                
                #ジョイスティックの押し込み判定
                armx = map_axis(joystick.get_axis(0))
                army = map_axis(joystick.get_axis(4)) 
                armz = map_axis(joystick.get_axis(1)) 
                print(armx, army, armz)
                
                #ジョイスティックの軸(-100 ~ 100)
                if armx > 50:
                    x -= 5
                    time.sleep(0.01)
                elif armx < -50:
                    x += 5
                    time.sleep(0.01)    
                else :
                    x += 0
                    time.sleep(0.01)
                    
                if army > 50:
                    y += 5
                    time.sleep(0.01)
                elif army < -50:
                    y -= 5
                    time.sleep(0.01)
                else :
                    y += 0
                    time.sleep(0.01)
                        
                if armz > 50:
                    z += 5
                    time.sleep(0.01)
                elif armz < -50:
                    z -= 5
                    time.sleep(0.01)
                else :
                    z += 0
                    time.sleep(0.01)
                
                
                b1 = y**2+s**2-(L2**2-L1**2)
                b2 = 2*L1(math.sqrt(y**2 + s**2))
                b3 = math.sqrt(x**2+z**2)
                c1 = x**2+y**2+z**2-(L2**2-L1**2)
                c2 = 2*L1*(math.aqrt(L2**2-L1**2))
                c3 = math.sqrt(x**2+z**2)
                
                #逆運動学(特異姿勢場合分け)
                if X == 0:
                    the0 = 90
                else :
                    the0 = math.degrees(math.atan(Z/X))
                    THE0 = round(the0, 2)

                if Y == 0:
                    the1 = 0
                else :
                    the1 = math.degrees(math.asin(b1/b2)) + math.degrees(math.atan(b3/Y))
                THE1 = round(the1, 2)

                if Z == -52:
                    the2 = 0
                else :
                    the2 = math.degrees(math.asin(c1/c2)) - math.degrees(math.atan(c3/Y))
                THE2 = round(the2, 2)
                
                #操作後座標のB3M角度
                print(THE0, THE1, THE2)
                
                #B3M用角度への変換
                angle6 = 100*THE0
                angle7 = -100*(THE1 + 78)
                angle8 = 100*(THE1 + 78)
                angle9 = 100*(THE2 + 84)
                
                print(angle6, angle7, angle8, angle9)
            
            
                #WRITEコマンド
                #メモリーマップ(RAM)のアドレス指定でデバイスのRAM上に書き込みます。
                def B3M_Write_CMD(servo_id, TxData, Address):

                    #送信コマンドを作成
                    txCmd = [0x08,      #SIZE
                            0x04,      #CMD
                            0x00,      #OPTION
                            servo_id,  #ID
                            TxData,    #DATA
                            Address,   #ADDRRESS
                            0x01]      #COUNT

                    #チェックサムを用意
                    checksum = 0
                    for i in txCmd:
                        checksum += i
                        
                    #リストの最後にチェックサムを挿入する
                    txCmd.append(checksum & 0xff)    

                    #WRITEコマンドを送信
                    b3m.write(txCmd)
                    
                    #サーボからの返事を受け取る
                    rxCmd = b3m.read(5)
                    
                    #もしリスト何になにも入っていなかったら正常に受信できていないと判断    
                    if len(rxCmd) == 0:
                        return False

                    #問題なければ返事を返す
                    return True


                #SET POSITIONコマンド
                #サーボモータに動作角と目標に到達するまでの時間を指定しポジションを変更します。
                def B3M_setPos_CMD(servo_id, pos, MoveTime):

                    #送信コマンドを作成
                    txCmd = [0x09,                  #SIZE
                            0x06,                  #CMD
                            0x00,                  #OPTION
                            servo_id,              #ID
                            pos & 0xff,            #POS_L
                            pos >> 8 & 0xff,       #POS_H
                            MoveTime & 0xff,       #TIME_L
                            MoveTime >> 8 & 0xff]  #TIME_H

                    #チェックサムを作成
                    checksum = 0
                    for i in txCmd:
                        checksum += i
                    
                    #リストの最後にチェックサムを挿入する
                    txCmd.append(checksum & 0xff)

                    #コマンドを送信
                    b3m.write(txCmd)

                    #サーボからの返事を受け取る
                    rxCmd = b3m.read(7)
                    
                    #もしリスト何になにも入っていなかったら正常に受信できていないと判断    
                    if len(rxCmd) == 0:
                        return False

                    #問題なければ返事を返す        
                    else:
                        return True
                        
                        '''
                        #現在値を戻り値にする場合は、下記の処理をreturnしてください。
                        rePos = [rxCmd[4], rxCmd[5]]
                        rePos = int.from_bytes(rePos, 'little')
                        
                        #サーボからは符号なしでポジションデータが返ってきます。0を中心とした数値に変換するため下記のように処理をします。
                        if (rePos > 32765):
                                rePos -= 65536

                        return rePos
                        '''


                #COMポートを開く
                b3m = serial.Serial('/dev/ttyUSB0', baudrate=1500000, parity=serial.PARITY_NONE, timeout=0.5)

                #B3Mサーボが動作するまでの準備
                #B3M_Write_CMD(servo_id, TxData, Address)

                #動作モード：Free (動作モードと特性を設定するため、設定書き換え中の誤動作を防止するため脱力にしておく)
                reData = B3M_Write_CMD(0xFF, 0x02, 0x28)
                print(reData)

                #位置制御モードに設定 (角度を指定して動作するモードです)
                reData = B3M_Write_CMD(0xFF, 0x02, 0x28)
                print(reData)

                #軌道生成タイプ：Even (直線補間タイプの位置制御を指定)
                reData = B3M_Write_CMD(0xFF, 0x01, 0x29)
                print(reData)

                #ゲインプリセット：No.0 (PIDのプリセットゲインを位置制御モード用に設定)
                reData = B3M_Write_CMD(0xFF, 0x00, 0x5C)
                print(reData)

                #動作モード：Normal （Freeの状態からトルクオン）
                reData = B3M_Write_CMD(0xFF, 0x00, 0x28)
                print(reData)

                #idangle = [[6, angle6], [7, angle7], [8, angle8], [9, angle9]]

                #for ida in range(len(idangle)):

                #ID0、500msかけて5000(50度)の位置に移動する
                reData = B3M_setPos_CMD(6, angle6, 1500)
                time.sleep(0.5)

                reData = B3M_setPos_CMD(7, angle7, 1500)
                reData = B3M_setPos_CMD(8, angle8, 1500)
                time.sleep(0.5)

                reData = B3M_setPos_CMD(9, angle9, 1500)
                time.sleep(0.5)

                #ポートを閉じる
                b3m.close()
                
                
            # gamepad_data = {
            #     "joy_lx": map_axis(joystick.get_axis(0)),
            #     "joy_ly": -map_axis(joystick.get_axis(1)),
            #     "joy_rx": map_axis(joystick.get_axis(3)),
            #     "joy_ry": -map_axis(joystick.get_axis(4)),
            #     "joy_lt": map_axis_t(joystick.get_axis(2)),
            #     "joy_rt": map_axis_t(joystick.get_axis(5)),
            #     "hat_x": joystick.get_hat(0)[0],
            #     "hat_y": joystick.get_hat(0)[1],
            #     "btn_a": joystick.get_button(0),
            #     "btn_b": joystick.get_button(1),
            #     "btn_x": joystick.get_button(2),
            #     "btn_y": joystick.get_button(3),
            #     "btn_lb": joystick.get_button(4),
            #     "btn_rb": joystick.get_button(5),
            #     "btn_back": joystick.get_button(6),
            #     "btn_start": joystick.get_button(7),
            #     "btn_guide": joystick.get_button(8),
            #     "btn_joyl": joystick.get_button(9),
            #     "btn_joyr": joystick.get_button(10)
            # }
            # print(gamepad_data)
            # print(type(map_axis(joystick.get_axis(0))))


if __name__ == '__main__':
    main()