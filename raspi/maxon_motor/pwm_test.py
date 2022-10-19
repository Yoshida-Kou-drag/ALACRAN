import pigpio
import time

pwm_left = 18
pwm_right = 19
DIRpin_left = 16
DIRpin_right = 20

pi = pigpio.pi()
pi.set_mode(pwm_left, pigpio.OUTPUT)
pi.set_mode(pwm_right, pigpio.OUTPUT)
pi.set_mode(DIRpin_left, pigpio.OUTPUT)
pi.set_mode(DIRpin_right, pigpio.OUTPUT)

def deg_to_duty(degree):
    dc = 2.0 + (11.0-2.0)/180*(degree+90)
    return dc


# GPIO18: 50Hz、duty比7.25%
print("back")
pi.write(DIRpin_left, 0)
pi.write(DIRpin_right, 0)
pi.hardware_PWM(pwm_left,10000,200000)
pi.hardware_PWM(pwm_right,10000,200000)

time.sleep(3)

print("front")
pi.write(DIRpin_left, 1)
pi.write(DIRpin_right, 1)

time.sleep(3)

pi.set_mode(pwm_left,pigpio.INPUT)
pi.set_mode(pwm_right,pigpio.INPUT)
pi.set_mode(DIRpin_left,pigpio.INPUT)
pi.set_mode(DIRpin_right,pigpio.INPUT)
pi.stop()