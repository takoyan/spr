#!/usr/bin/env python
# -*- coding: utf-8 -*-


import rospy
from std_msgs.msg import String
from pocketsphinx import LiveSpeech, get_model_path
import os
import sys
import numpy as np
from time import sleep
import pyaudio
from scipy import fromstring, int16

        

def talker():
    while stream.is_active():
        try:
            input=stream.read(CHUNK)
            num_data=fromstring(input, dtype="int16")/32768.0
            print(num_data.max())
            if(num_data.max()>=0.5):
                pub = rospy.Publisher('/spr_state2', String, queue_size=10)
                rospy.init_node('talker', anonymous=True)
                r = rospy.Rate(10) # 10hz
                while not rospy.is_shutdown():
                    speech = LiveSpeech(dic=os.path.join("/home/takoyan/catkin_ws/src/spr", 'ziso.dict'))
                    for i in speech:
                        input=stream.read(CHUNK)
                        num_data=fromstring(input, dtype="int16")/32768.0
                        print('MAX:'+str(num_data.max()))
                        if(num_data.max()>=0.001):
                            rospy.loginfo(i)
                            pub.publish(str(i))
                            r.sleep()


        except KeyboardInterrupt:
            break


p=pyaudio.PyAudio()
CHUNK=1024
input_device_index=0
stream=p.open(format=pyaudio.paInt16,
             channels=1,
             rate=44100,
             frames_per_buffer=CHUNK,
             input=True)
if __name__=='__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

