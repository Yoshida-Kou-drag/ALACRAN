import math

def ideal_val_calc(la_ground,ra_ground,body_ground,debug = False):
    a=(la_ground[1]-body_ground[1])/(la_ground[0]-body_ground[0])
    left_tilt=math.degrees(math.atan(a))
    a=(ra_ground[1]-body_ground[1])/(ra_ground[0]-body_ground[0])
    right_tilt=math.degrees(math.atan(a))

    b = abs(body_ground[1])
    c = abs(la_ground[1])
    a = math.sqrt(-math.cos(math.radians(170))*2*b*c+b**2+c**2)
    left_pitch = (a**2+b**2-c**2)/(2*a*b)
    left_pitch = math.acos(left_pitch)
    left_pitch = math.degrees(left_pitch)

    b = abs(body_ground[1])
    c = abs(ra_ground[1])
    a = math.sqrt(-math.cos(math.radians(170))*2*b*c+b**2+c**2)
    right_pitch = (a**2+b**2-c**2)/(2*a*b)
    right_pitch = math.acos(right_pitch)
    right_pitch = math.degrees(right_pitch)
    return left_tilt,right_tilt,left_pitch,right_pitch

if __name__ == "__main__":
    la_ground = [-83.4, 70]
    ra_ground = [83.4, 20]
    body_ground = [-16.6,-80]
    print(ideal_val_calc(la_ground,ra_ground,body_ground))
     
