#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import re
import numpy as np
import math
import difflib
import sys
from time import sleep
import os
import pyaudio
from scipy import fromstring, int16



def callback(data):
    if(data.data != ''):
        data=re.findall(r'[a-z]*\S', data.data)
        data=np.array(data)
        print(data)
        
        max=0
        ans=0

        for q, a in qa_dict.items():
            que=re.findall(r'[a-z]*\S', q.encode('utf-8'))
            score=difflib.SequenceMatcher(None, que, data).ratio()
            #print('que:'+str(que) + 'score'+str(score))

            if(score>max and score>=0.5):
                max=score
                ans=a
            if ans is not 0:
                print ans
                print('\n')
                os.system('espeak "{}" -s 135'.format(ans))
            else:
                print'答えはみつかりません'
                os.system('espeak "no answer"')
                print('\n')

       # except KeyboardInterrupt:
            #break
        

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/spr_state2', String, callback)

    #spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

    
qa_dict={}
que=[]
qa_list=[]


if __name__ == '__main__':
    with open('/home/takoyan/catkin_ws/src/spr/quize.txt', 'r')as quize:
        qa_list=quize.readlines()
        for qa in qa_list:
            qa=qa.rstrip().decode('utf-8').split(',')
            qa_dict[qa[0]]=qa[1]
        listener()
