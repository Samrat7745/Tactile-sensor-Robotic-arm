import time
import math
from gpiozero import Servo, Button

# Constants
pi = 3.1415926
L1 = 5  # Length between the first motor and the second motor (in cm)
L2 = 8  # Length between the second motor and the third motor (in cm)
L3 = 4  # Length between the third motor and the end of arm (in cm)

# Initialize servo motors
servo1 = Servo(2)
servo2 = Servo(3)
servo3 = Servo(4)

# Initialize buttons
btn1 = Button(6)
btn2 = Button(7)

def forward_kinematics():
    # Assume the values of the angles
    q1_deg = 50 
    q2_deg = 30
    q3_deg = 25
    q_deg = q1_deg + q2_deg + q3_deg

    q1 = math.radians(q1_deg)  # Convert the angle from degree to radian
    q2 = math.radians(q2_deg)  # Convert the angle from degree to radian
    q3 = math.radians(q3_deg)  # Convert the angle from degree to radian
    q = math.radians(q_deg)    # Convert the angle from degree to radian

    x_1 = L1 * math.cos(q1)
    x_2 = L2 * math.cos(q1 + q2)
    x_3 = L3 * math.cos(q1 + q2 + q3)
    x = x_1 + x_2 + x_3  # The expected value with respect to the X axis

    y_1 = L1 * math.sin(q1)
    y_2 = L2 * math.sin(q1 + q2)
    y_3 = L3 * math.sin(q1 + q2 + q3)
    y = y_1 + y_2 + y_3  # The expected value with respect to the Y axis

    # Move servos to the calculated angles
    servo1.value = q1_deg / 180.0 - 0.5
    servo2.value = q2_deg / 180.0 - 0.5
    servo3.value = q3_deg / 180.0 - 0.5

def inverse_kinematics():
    # Assume the point on X and Y axes, and the value of theta
    x = 5 
    y = 5 
    q_deg = 140
    q = math.radians(q_deg)  # Convert the angle from degree to radian

    x_inv = x - (L3 * math.cos(q)) 
    y_inv = y - (L3 * math.sin(q))

    x_sq = x ** 2 
    y_sq = y ** 2 
    L1_sq = L1 ** 2
    L2_sq = L2 ** 2

    q2 = math.acos((x_sq + y_sq - (L1_sq + L2_sq)) / (2 * L1 * L2))
    k1 = (L1 + L2 * math.cos(q2)) * x_inv
    k2 = (L2 * y_inv * math.sin(q2))

    q1 = math.acos((k1 + k2) / (x_sq + y_sq))
    q3 = q - (q1 + q2)

    q1_deg = math.degrees(q1)
    q2_deg = math.degrees(q2)
    q3_deg = math.degrees(q3)

    # Move servos to the calculated angles
    servo1.value = q1_deg / 180.0 - 0.5
    servo2.value = q2_deg / 180.0 - 0.5
    servo3.value = q3_deg / 180.0 - 0.5

# Main loop
while True:
    if btn1.is_pressed:  # if button 1 is pressed (forward kinematics)
        forward_kinematics()

    if btn2.is_pressed:  # if button 2 is pressed (inverse kinematics)
        inverse_kinematics()

    time.sleep(0.1)  # Delay to prevent excessive looping
