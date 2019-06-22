from __future__ import division
import pyaudio
import struct
import math
import datetime
import time
import audioop
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pylab import *

INITIAL_TAP_THRESHOLD = 300
INITIAL_TAP_THRESHOLD1 = 300
INITIAL_TAP_THRESHOLD2 = 300
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
RATE = 44100  
INPUT_BLOCK_TIME = 0.0001
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
printed = 1000
printed1 = 1000
printed2 = 1000
timeKonig = None
timeKonig1 = None
timeLogitech = None
detectedmic1 = False
detectedmic2 = False
detectedmic3 = False
A = 0.0
B = 0.0
D = 0.0
V = 330.0

def get_rms( block ):
    return audioop.rms(block, 2)
def middle(x, y, z):
    return sorted([x, y, z])[1]

def location(xsecond, x1, ysecond, y1, Tsecond, T1):
    A = (2.0*xsecond)/(Tsecond) - (2.0*x1)/(T1);
    B = (2.0*ysecond)/(Tsecond) - (2.0*y1)/(T1);
    D = (Tsecond - T1) + (((x1*x1)+(y1*y1))/(T1)) - (((xsecond*xsecond)+(ysecond*ysecond))/(Tsecond));

class TapTester(object):
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.stream1 = self.open_mic_stream1()
        self.stream2 = self.open_mic_stream2()
        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.tap_threshold1 = INITIAL_TAP_THRESHOLD1
        self.tap_threshold2 = INITIAL_TAP_THRESHOLD2

    def find_input_device(self):
        device_index = 0            
        for i in range( self.pa.get_device_count() ):     
            devinfo = self.pa.get_device_info_by_index(i)   
            print( "Device %d: %s"%(i,devinfo["name"]) )

            for keyword in ["mic","input"]:
                if keyword in devinfo["name"].lower():
                    print( "Found an input: device %d - %s"%(i,devinfo["name"]) )
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No preferred input found; using default input device." )

        return device_index

    def stop(self):
        self.stream.close()

    def open_mic_stream( self ):
        device_index = self.find_input_device()
        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = 0,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)        

        return stream
    def open_mic_stream1( self ):

        stream1 = self.pa.open(  format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = 1,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream1

    def open_mic_stream2( self ):

        stream2 = self.pa.open(  format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = 2,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream2
    def listen(self):
        block = self.stream.read(INPUT_FRAMES_PER_BLOCK, exception_on_overflow = False)
        amplitude = get_rms( block )
        global printed
        if amplitude > self.tap_threshold and printed < i:
            global timeKonig
            timeKonig = datetime.datetime.now()
            global detectedmic1
            detectedmic1 = True
            printed = i + 30000
        block1 = self.stream1.read(INPUT_FRAMES_PER_BLOCK, exception_on_overflow = False)
        amplitude1 = get_rms( block1 )           
        global printed1
        if amplitude1 > self.tap_threshold1 and printed1 < i:
            global timeKonig1
            timeKonig1 = datetime.datetime.now()
            global detectedmic2
            detectedmic2 = True
            printed1 = i + 30000
        block2 = self.stream2.read(INPUT_FRAMES_PER_BLOCK, exception_on_overflow = False)
        amplitude2 = get_rms( block2 )
        global printed2
        if amplitude2 > self.tap_threshold2 and printed2 < i:
            global timeLogitech
            timeLogitech = datetime.datetime.now()
            global detectedmic3
            detectedmic3 = True
            printed2 = i + 30000
        if detectedmic1 and detectedmic2 and detectedmic3:
            print "0: ", timeKonig
            print "1: ", timeKonig1
            print "2: ", timeLogitech
            timeLogitech = timeLogitech.microsecond + 6000
            timeKonig1 = timeKonig1.microsecond + 2700
            timeKonig = timeKonig.microsecond
            verschil1 = (timeKonig - timeKonig1)
            verschil2 = (timeKonig - timeLogitech)
            # if timeKonig > timeKonig1:
            #     if (timeKonig - timeKonig1).microseconds < 20000:
            #         print (timeKonig - timeKonig1).microseconds
            #         print (timeKonig - timeLogitech).microseconds
            # else:
            #     if timeKonig < timeKonig1:
            #         if (timeKonig1 - timeKonig).microseconds < 20000:
            #             print "2. ", (timeKonig1 - timeKonig).microseconds
            # print timeKonig
            # print timeLogitech
            # print timeKonig1
            print verschil1
            print verschil2

            mic0 = min(timeLogitech, timeKonig, timeKonig1)
            mic1 = middle(timeLogitech, timeKonig, timeKonig1)
            mic2 = max(timeLogitech, timeKonig, timeKonig1)

            x0 = 0.0
            y0 = 0.0
            x1 = -1.35;
            y1 = 2.34;
            x2 = 1.35;
            y2 = 2.34;
            if mic0 == timeLogitech:
                eerste = "Logitech"
            if mic1 == timeLogitech:
                tweede = "Logitech"
            if mic2 == timeLogitech:
                derde = "Logitech"

            if mic0 == timeKonig:
                eerste = "Konig"
            if mic1 == timeKonig:
                tweede = "Konig"
            if mic2 == timeKonig:
                derde = "Konig"

            if mic0 == timeKonig1:
                eerste = "Konig1"
            if mic1 == timeKonig1:
                tweede = "Konig1"
            if mic2 == timeKonig1:
                derde = "Konig1"

            mic1 = mic1 - mic0
            mic2 = mic2 - mic0

            mic1 = (mic1/1000000)*330
            mic2 = (mic2/1000000)*330

            # print "mic1: ", mic1
            # print "mic2: ", mic2

            A2 = (2.0*x2)/(mic2) - (2.0*x1)/(mic1);
            B2 = (2.0*y2)/(mic2) - (2.0*y1)/(mic1);
            D2 = (mic2 - mic1) + (((x1*x1)+(y1*y1))/(mic1)) - (((x2*x2)+(y2*y2))/(mic2));

            A0 = -(2.0*x1)/mic1;
            B0 = -(2.0*y1)/mic1;
            D0 =  0.0 - mic1 + (((x1*x1)+(y1*y1)) / mic1);

            # print A0
            # print B0
            # print D0
            # print A2
            # print B2
            # print D2

            finalX = (B0*D2 - B2*D0) / (A0*B2 - A2*B0);
            finalY = (A2*D0 - A0*D2) / (A0*B2 - A2*B0);

            print "(", finalX, "; ", finalY, ")"

            print "eerste mic=: ", eerste
            print "tweede mic=: ", tweede
            print "derde mic=: ", derde

            fig = figure()
            ax = fig.add_subplot(111)
            ax.axis('equal')
            ax.plot([1.35, 0], [2.34, 0], 'k-')
            ax.plot([-1.35, 0], [2.34, 0], 'k-')
            ax.plot([-1.35, 1.35], [2.34, 2.34], 'k-')
            ax.plot([0.5, 1.01, 0.1], [-0.01, 0.5, 0.88], 'w.') #base boundary
            grid()
            x = finalX
            y = finalY
            plt.scatter(x, y)
            ax.axhline(y=0, color='k')
            ax.axvline(x=0, color='k')
            savefig('foo.jpg', bbox_inches='tight')
            plt.show()

            sleep(2000);


            timeKonig1, timeKonig, timeLogitech = None, None, None
            detectedmic1, detectedmic2, detectedmic3 = False, False, False

    

if __name__ == "__main__":
    tt = TapTester()

    for i in range(10000000):
        tt.listen()
