import pygame
import time
import sys
sys.path.append('/home/pi/git/ALACRAN/raspi/B3M/')
import b3mCtrl
import pigpio
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
pi.set_mode(pwm_left, pigpio.output)
pi.set_mode(pwm_right, pigpio.output)
pi.set_mode(DIRpin_left, pigpio.output)
pi.set_mode(DIRpin_right, pigpio.output)

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