#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Created on Feb 15, 2017

@author: Evan
'''
import sys
#sys.path.append('/home/qiuguoji/new_media_base/kernel')
#print(sys.path)
from core.settings import settings
import math
import os
import urllib
import urllib2
import cStringIO
from PIL import Image
import logging
import traceback
import threading
import datetime
import time

logger = logging.getLogger(__name__)

def check_remote_picture(url, is_raise=False,timeout=3,is_retry=True):
    print ('check_remote_picture.image.url=%s' % url)
    startTime = datetime.datetime.now()
    try:
        content = urllib2.urlopen(url,None,timeout).read()
    except:
        if is_retry:
            time.sleep(1)
            try:
                content = urllib2.urlopen(url,None,timeout).read()
            except:
                if is_retry:
                    time.sleep(3)
                    try:
                        content = urllib2.urlopen(url,None,timeout).read()
                    except:
                        if is_raise:
                            raise
                        else:
                            return -1
                elif is_raise:
                    raise
                else:
                    return -1
        elif is_raise:
            raise
        else:
            return -1
    try:
        byte_size = len(content)
        print ('check_remote_picture.image.filesize=%d' % byte_size)
        file = cStringIO.StringIO(content)
        img = Image.open(file)
        file.close()
        print ('check_remote_picture.image.format=%s, size=%s, mode=%s' % (img.format,img.size,img.mode))
        rate = float('%0.1f'%float(float(img.size[0])/float(img.size[1])))
        print ('check_remote_picture.image.rate=%f' % rate)
        print ('check_remote_picture.settings.keyvalue,picMinWidth=%s,picMinHeight=%s,rateRange=%s,sizeRange=%s' % (settings.PICMINWIDTH,settings.PICMINHEIGHT,settings.RATERANGE,settings.SIZERANGE))
        if img.size[0] < settings.PICMINWIDTH \
            or img.size[1] < settings.PICMINHEIGHT \
            or rate < list(eval(settings.RATERANGE))[0] \
            or rate > list(eval(settings.RATERANGE))[1] \
            or byte_size < list(eval(settings.SIZERANGE))[0] \
            or byte_size > list(eval(settings.SIZERANGE))[1]:
            return 0
    except:
        logger.info("check_remote_picture exception when check image, image_url: %s" % url)
        if is_raise:
            raise
        else:
            return -1
    finally:
        print ("check complete, costs time=%d" % ((datetime.datetime.now() - startTime).microseconds/1000))
    return 1
 

if __name__ == "__main__":
    #webUrl = input('please input remote pic url:')
    startTime = datetime.datetime.now()
    webUrl = 'http://pic5.qiyipic.com/image/20150317/f7/7b/13/v_50015485_m_601_m8_480_270.jpg'
    remotePicCheckRes = check_remote_picture(webUrl,True)
    print ("remotePicCheckRes:", remotePicCheckRes)
    print ("all image costs time=%d" % ((datetime.datetime.now() - startTime).microseconds/1000))













    
    
    

