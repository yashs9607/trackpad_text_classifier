import subprocess
import os
import numpy as np

def abs_info():    
    pipe = subprocess.Popen(["libinput", "record", "/dev/input/event7"], stdout=subprocess.PIPE)
    ABS_INFO={}
    ABS_FLAG = -1
    with pipe.stdout as stream:
        while not pipe.poll():
            try:
                line = next(stream).decode().strip()
                if line.startswith('absinfo:'):
                    line = next(stream).decode().strip()
                    ABS_FLAG = 1
                elif line.startswith('properties:'):
                    ABS_FLAG=0
                
                if ABS_FLAG==1:
                    key, value = line.split(':')
                    ABS_INFO[int(key)] = eval(value)
                    
                elif ABS_FLAG==0:
                    break
                
            except KeyboardInterrupt:
                break
            
    pipe.kill()
    return ABS_INFO


ABS_INFO = abs_info()



DATA_PATH = os.path.join('word_data')
words = ['hello', 'world', 'i_am', 'yash']
no_sequences = 30

for word in words:
    try:
        os.makedirs(os.path.join(DATA_PATH, word))
    except:
        pass


SCALE = 2
MAX_LEN = ABS_INFO[0][1]/SCALE
MAX_WID = ABS_INFO[1][1]/SCALE
x=0
y=0

import pygame
from sys import exit
from time import time


for word in words:
    for sequence in range(no_sequences):
        pygame.init()
        screen = pygame.display.set_mode((MAX_LEN, MAX_WID))

        P_WID = 5
        P_HEI = 5

        temp = []
        finished=-1

        pipe = subprocess.Popen(["libinput", "record", "/dev/input/event7"], stdout=subprocess.PIPE)
        window = []
        WINDOW_SIZE=1500
        EVENTS_FLAG = -1
        
        
        with pipe.stdout as stream:
            while not pipe.poll():
                try:
                    line = next(stream).decode().strip()
                    if line.startswith('events:'):
                        EVENTS_FLAG = 1
                        continue
                    
                    if EVENTS_FLAG==1:
                        if line.startswith('#') or line.startswith('- evdev:'):
                            continue
                        
                        window.append(eval(line.split('#')[0].strip('- ')))
                        window = window[::-1][0:min(len(window), 1)]
                        e = window[0]
                        if e[2]==3:
                            if e[3]==0:
                                x = e[-1]/SCALE
                            if e[3]==1:
                                y = e[-1]/SCALE
                            
                            if finished == -1:
                                temp.append(np.array([x,y]))
                            else:
                                temp.append(np.array([0,0]))
                            
                            
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    finished = 1
                                    
                                if event.type == pygame.QUIT:
                                    exit()
                               
                            
                            if len(temp)==WINDOW_SIZE:
                                break
                    
                    if finished == -1:
                        pygame.display.set_caption(f'{word}, {sequence}')
                    else:
                        pygame.display.set_caption(f'{word}, {sequence} finished')
                    pygame.draw.rect(screen, (255, 0, 0), (x, y, P_WID, P_HEI))
                    # pygame.blit()
                    pygame.display.update()
                    
                except KeyboardInterrupt:
                    break
            pipe.kill()
            pygame.quit()      
            
        npy_path = os.path.join(DATA_PATH, word, str(sequence))
        np.save(npy_path, np.array(temp))
        
        