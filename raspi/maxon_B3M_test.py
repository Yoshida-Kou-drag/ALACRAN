import time
import sys
import termios
sys.path.append('./B3M/')
import b3mCtrl
import pigpio

##########B3M初期化##########################
aaa = b3mCtrl.B3mClass()
aaa.begin("/dev/ttyUSB0",1500000)

idx= [1,2]

for id in range(len(idx)):
    print(aaa.setMode(idx[id],"FREE"))
    time.sleep(0.01)
    
    print(aaa.setMode(idx[id],"SPEED"))
    time.sleep(0.01)
    
    hoge = aaa.setRam(idx[id], 0, "DesiredVelosity")
    time.sleep(0.01)


################maxon motor初期化###############
pwm_left = 18
pwm_right = 19
DIRpin_left = 16
DIRpin_right = 20

pi = pigpio.pi()
pi.set_mode(pwm_left, pigpio.OUTPUT)
pi.set_mode(pwm_right, pigpio.OUTPUT)
pi.set_mode(DIRpin_left, pigpio.OUTPUT)
pi.set_mode(DIRpin_right, pigpio.OUTPUT)



while True:
    fd = sys.stdin.fileno()

    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)

    new[3] &= ~termios.ICANON

    new[3] &= ~termios.ECHO

    try:
        termios.tcsetattr(fd,termios.TCSANOW,new)

        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd,termios.TCSANOW,old)

    print(ch)

    if ch=='w':
        print("Advance foward")
        pi.write(DIRpin_left, 1)
        pi.write(DIRpin_right, 1)
        pi.hardware_PWM(pwm_left,10000,200000)
        pi.hardware_PWM(pwm_right,10000,200000)
    elif ch=='s':
        print("Back")
        pi.write(DIRpin_left, 0)
        pi.write(DIRpin_right, 0)
        pi.hardware_PWM(pwm_left,10000,200000)
        pi.hardware_PWM(pwm_right,10000,200000)
    elif ch=='d':
        print("right")
        pi.write(DIRpin_left, 1)
        pi.write(DIRpin_right, 0)
        pi.hardware_PWM(pwm_left,10000,200000)
        pi.hardware_PWM(pwm_right,10000,200000)
    elif ch=='a':
        print("left")
        pi.write(DIRpin_left, 0)
        pi.write(DIRpin_right, 1)
        pi.hardware_PWM(pwm_left,10000,200000)
        pi.hardware_PWM(pwm_right,10000,200000)

    elif ch=='u':
        print("UP")
        hoge = aaa.setRam(idx[0], -20000, "DesiredVelosity")
        time.sleep(0.01)
    elif ch=='i':
        hoge = aaa.setRam(idx[1], 20000, "DesiredVelosity")
        time.sleep(0.01)
    elif ch=='j':
        print("Down")
        hoge = aaa.setRam(idx[0], 20000, "DesiredVelosity")
        time.sleep(0.01)
    elif ch=='k':
        hoge = aaa.setRam(idx[1], -20000, "DesiredVelosity")
        time.sleep(0.01)
    else :
        print("stop")
        pi.hardware_PWM(pwm_left,10000,0)
        pi.hardware_PWM(pwm_right,10000,0)
        hoge = aaa.setRam(idx[0], 0, "DesiredVelosity")
        time.sleep(0.01)
        hoge = aaa.setRam(idx[1], 0, "DesiredVelosity")
        time.sleep(0.01)

