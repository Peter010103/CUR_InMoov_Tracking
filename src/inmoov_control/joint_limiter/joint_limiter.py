#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16MultiArray
from enum import Enum, IntEnum
import numpy as np
import yaml


class Joints(IntEnum):
    R_WRIST = 0
    R_THUMB = 1
    R_INDEX = 2
    R_MIDDLE = 3
    R_RINGFINGER = 4
    R_PINKY = 5
    R_BICEP = 6
    R_ARM_ROTATE = 7
    R_SHOULDER = 8
    R_OMOPLATE = 9
    L_THUMB = 10
    L_INDEX = 11
    L_MIDDLE = 12
    L_RINGFINGER = 13
    L_PINKY = 14
    L_WRIST = 15
    L_BICEP = 16
    L_ARM_ROTATE = 17
    L_SHOULDER = 18
    L_OMOPLATE = 19
    NECK = 20
    ROTHEAD = 21
    ROLLNECK = 22
    EYELID = 23
    JAW = 24
    EYEX = 25
    EYEY = 26
    TOPSTOM = 27
    MIDSTOM = 28
    LOWSTOM = 29


class JointTopic(IntEnum):
    SPINAL_COLUMN = 0
    L_ARM = 1
    R_ARM = 2
    L_HAND = 3
    R_HAND = 4
    FACE = 5


joints_list = np.zeros(shape=(30, 8))
joints_values = np.zeros(shape=(30, 3))
iterator = np.zeros(6)
output_array = np.zeros(30)


def setupAngleArray():
    for i in [Joints.R_WRIST, Joints.L_WRIST, Joints.R_ARM_ROTATE, Joints.L_ARM_ROTATE, Joints.NECK,
              Joints.ROTHEAD, Joints.ROLLNECK, Joints.EYEX, Joints.EYEY, Joints.TOPSTOM, Joints.MIDSTOM]:
        joints_list[i, :] += 90
    joints_list[Joints.L_SHOULDER, :] += 30
    joints_list[Joints.R_SHOULDER, :] += 30
    for i in [Joints.R_OMOPLATE, Joints.L_OMOPLATE, Joints.JAW]:
        joints_list[i, :] += 10
    joint_dict = {}
    with open("data.yaml", 'r') as stream:
        joint_dict = yaml.safe_load(stream)
    for i, val in enumerate(['R_WRIST',
                             'R_THUMB',
                             'R_INDEX',
                             'R_MIDDLE',
                             'R_RINGFINGER',
                             'R_PINKY',
                             'R_BICEP',
                             'R_ARM_ROTATE',
                             'R_SHOULDER',
                             'R_OMOPLATE',
                             'L_THUMB',
                             'L_INDEX',
                             'L_MIDDLE',
                             'L_RINGFINGER',
                             'L_PINKY',
                             'L_WRIST',
                             'L_BICEP',
                             'L_ARM_ROTATE',
                             'L_SHOULDER',
                             'L_OMOPLATE',
                             'NECK',
                             'ROTHEAD',
                             'ROLLNECK',
                             'EYELID',
                             'JAW',
                             'EYEX',
                             'EYEY',
                             'TOPSTOM',
                             'MIDSTOM',
                             'LOWSTOM']):
        joints_values[i, 0] = joint_dict[val]['closed']
        joints_values[i, 1] = joint_dict[val]['rest']
        joints_values[i, 2] = joint_dict[val]['open']


def average(li):
    for v in li:
        temp = np.sum(joints_list[v, :])
        temp = temp >> 3
        output_array[v] = temp


def leftArmCallback(data):
    joints_list[Joints.L_BICEP, iterator[JointTopic.L_ARM]] = data.data[0]
    joints_list[Joints.L_ARM_ROTATE, iterator[JointTopic.L_ARM]] = data.data[1]
    joints_list[Joints.L_SHOULDER, iterator[JointTopic.L_ARM]] = data.data[2]
    joints_list[Joints.L_OMOPLATE, iterator[JointTopic.L_ARM]] = data.data[3]
    iterator[JointTopic.L_ARM] = (iterator[JointTopic.L_ARM] + 1) % 8
    average([Joints.L_BICEP, Joints.L_ARM_ROTATE,
            Joints.L_SHOULDER, Joints.L_OMOPLATE])


def rightArmCallback(data):
    joints_list[Joints.R_BICEP, iterator[JointTopic.R_ARM]] = data.data[0]
    joints_list[Joints.R_ARM_ROTATE, iterator[JointTopic.R_ARM]] = data.data[1]
    joints_list[Joints.R_SHOULDER, iterator[JointTopic.R_ARM]] = data.data[2]
    joints_list[Joints.R_OMOPLATE, iterator[JointTopic.R_ARM]] = data.data[3]
    iterator[JointTopic.R_ARM] = (iterator[JointTopic.R_ARM] + 1) % 8
    average([Joints.R_BICEP, Joints.R_ARM_ROTATE,
            Joints.R_SHOULDER, Joints.R_OMOPLATE])

def spinalCallback(data):
    joints_list[Joints.NECK, iterator[JointTopic.SPINAL_COLUMN]] = data.data[0]
    joints_list[Joints.ROTHEAD,
                iterator[JointTopic.SPINAL_COLUMN]] = data.data[1]
    joints_list[Joints.ROLLNECK,
                iterator[JointTopic.SPINAL_COLUMN]] = data.data[2]
    iterator[JointTopic.SPINAL_COLUMN] = (
        iterator[JointTopic.SPINAL_COLUMN] + 1) % 8
    average([Joints.NECK,
            Joints.ROTHEAD, Joints.ROLLNECK])


def leftHandCallback(data):
    joints_list[Joints.L_THUMB, iterator[JointTopic.L_HAND]] = data.data[0]
    joints_list[Joints.L_INDEX, iterator[JointTopic.L_HAND]] = data.data[1]
    joints_list[Joints.L_MIDDLE, iterator[JointTopic.L_HAND]] = data.data[2]
    joints_list[Joints.L_RINGFINGER,
                iterator[JointTopic.L_HAND]] = data.data[3]
    joints_list[Joints.L_PINKY,
                iterator[JointTopic.L_HAND]] = data.data[4]
    iterator[JointTopic.L_HAND] = (iterator[JointTopic.L_HAND] + 1) % 8
    average([Joints.L_THUMB, Joints.L_INDEX, Joints.L_MIDDLE,
            Joints.L_RINGFINGER, Joints.L_PINKY])


def rightHandCallback(data):
    joints_list[Joints.R_THUMB, iterator[JointTopic.R_HAND]] = data.data[0]
    joints_list[Joints.R_INDEX, iterator[JointTopic.R_HAND]] = data.data[1]
    joints_list[Joints.R_MIDDRE, iterator[JointTopic.R_HAND]] = data.data[2]
    joints_list[Joints.R_RINGFINGER,
                iterator[JointTopic.R_HAND]] = data.data[3]
    joints_list[Joints.R_PINKY,
                iterator[JointTopic.R_HAND]] = data.data[4]
    iterator[JointTopic.R_HAND] = (iterator[JointTopic.R_HAND] + 1) % 8
    average([Joints.R_THUMB, Joints.R_INDEX, Joints.R_MIDDLE,
            Joints.R_RINGFINGER, Joints.R_PINKY])

def faceCallback(data):
    return

def clipOutputArray():
    output_array = np.clip(
        output_array, joints_values[:, 0], joints_values[:, 2])


def listener():
    rospy.init_node('joint_limiter', anonymous=True)
    joint_pub = rospy.Publisher(
        '/servo_angles', Int16MultiArray, queue_size=10)
    rate = rospy.Rate(10)  # Run at 10Hz
    joint_sub0 = rospy.Subscriber(
        '/joints/spinal_column', Int16MultiArray, spinalCallback)
    joint_sub1 = rospy.Subscriber(
        '/joints/arm/left', Int16MultiArray, leftArmCallback)
    joint_sub2 = rospy.Subscriber(
        '/joints/arm/right', Int16MultiArray, rightArmCallback)
    joint_sub3 = rospy.Subscriber(
        '/joints/hand/left', Int16MultiArray, leftHandCallback)
    joint_sub4 = rospy.Subscriber(
        '/joints/hand/right', Int16MultiArray, rightHandCallback)
    joint_sub5 = rospy.Subscriber(
        '/joints/face', Int16MultiArray, faceCallback)
    while True:
        data_to_send = Int16MultiArray()
        data_to_send.data = output_array
        joint_pub.publish(data_to_send)
        rate.sleep()


if __name__ == "__main__":
    setupAngleArray()
    listener()