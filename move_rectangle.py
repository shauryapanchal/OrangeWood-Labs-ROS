#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import math

def move_straight(velocity_publisher, speed, distance):
    vel_msg = Twist()
    vel_msg.linear.x = speed
    vel_msg.angular.z = 0.0  # No rotation while moving straight

    start_time = rospy.Time.now().to_sec()
    current_distance = 0

    # Move the turtle until the desired distance is reached
    while current_distance < distance and not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg)
        current_time = rospy.Time.now().to_sec()
        current_distance = speed * (current_time - start_time)
        rospy.sleep(0.01)  # Short sleep for smoother movement

    # Stop the turtle after moving the distance
    vel_msg.linear.x = 0
    velocity_publisher.publish(vel_msg)
    rospy.sleep(1)

def rotate(velocity_publisher, angular_speed, angle):
    vel_msg = Twist()
    vel_msg.linear.x = 0.0
    vel_msg.angular.z = angular_speed  # Rotate in place

    start_time = rospy.Time.now().to_sec()
    current_angle = 0

    # Rotate the turtle until the desired angle is reached
    while current_angle < angle and not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg)
        current_time = rospy.Time.now().to_sec()
        current_angle = angular_speed * (current_time - start_time)
        rospy.sleep(0.01)  # Short sleep for smoother rotation

    # Stop the turtle after turning
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)
    rospy.sleep(1)

def move_turtle_in_rectangle():
    rospy.init_node('move_turtle_rectangle', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    # Parameters for the rectangle
    speed = 1.0  # Linear speed (m/s)
    distance1 = 2.0  # Distance for the first pair of parallel sides
    distance2 = 1.0  # Distance for the second pair of parallel sides
    angular_speed = 0.5  # Angular speed (rad/s)
    angle = math.pi / 2  # 90 degrees in radians

    # Move in a rectangle path
    for _ in range(2):
        # Move the first side
        move_straight(velocity_publisher, speed, distance1)
        # Turn 90 degrees
        rotate(velocity_publisher, angular_speed, angle)

        # Move the second side
        move_straight(velocity_publisher, speed, distance2)
        # Turn 90 degrees
        rotate(velocity_publisher, angular_speed, angle)

    rospy.loginfo("Turtle has completed a rectangle path and returned to its starting point.")

if __name__ == '__main__':
    try:
        move_turtle_in_rectangle()
    except rospy.ROSInterruptException:
        pass
