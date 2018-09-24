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

model_path=get_model_path()    

def talker():
    rospy.init_node('talker', anonymous=True)
    #rospy.Subscriber('spr_state', String, start_speech)
    global flag
    global start
    flag=True
    start=False
    
    while 1:
        try:
            rospy.Subscriber('spr_state', String, start_speech)
            if(start==True):
                if(flag == True):
                    pub = rospy.Publisher('spr', String, queue_size=10)
                    rospy.init_node('talker', anonymous=True)
                    #while not rospy.is_shutdown():
                    print('Start!!!!!!!')
                    while(1):
                        #input=stream.read(CHUNK)
                        #num_data=fromstring(input, dtype="int16")/32768.0
                        #print(num_data.max())
                        #if(num_data.max()>=0.6):
                        speech = LiveSpeech(dic=os.path.join(model_path, 'ziso.dict'))
                            #no_serach==Trueならストップ
                        for i in speech:
                            rospy.loginfo(i)
                            print 'i:'+str(i)
                            pub.publish(str(i))
                            print('finish')
                            flag=False
                            break
                        break

                elif(flag==False):
                    print('Do not speak!!!')
                    speech=LiveSpeech(no_search=True)
                    #please_speak=rospy.Publisher('please_speak', String, queue_size=10)
                    #please_speak.Publish('please_speak')
                    rospy.Subscriber('restart_speech', String, restart_speech)
                    
        except KeyboardInterrupt:
            break

def start_speech(data):
    global start
    start=True
    return 

def restart_speech(data):
    global flag
    flag=True
    return 
            

"""
p=pyaudio.PyAudio()
CHUNK=1024
input_device_index=0
stream=p.open(format=pyaudio.paInt16,
             channels=1,
             rate=44100,
             frames_per_buffer=CHUNK,
             input=True)
"""
if __name__=='__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

