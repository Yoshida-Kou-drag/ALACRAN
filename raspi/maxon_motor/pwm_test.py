import pigpio
import time

gpio_pin0 = 18
gpio_pin1 = 19

pi = pigpio.pi()
pi.set_mode(gpio_pin0, pigpio.OUTPUT)

def deg_to_duty(degree):
    dc = 2.0 + (11.0-2.0)/180*(degree+90)
    return dc


# GPIO18: 50Hz、duty比7.25%
print(deg_to_duty(21)*10000)
pi.hardware_PWM(gpio_pin0,50,int(deg_to_duty(21)*10000))
pi.hardware_PWM(gpio_pin1,50,int(deg_to_duty(15)*10000))

time.sleep(5)

pi.stop()