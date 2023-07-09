import os
import numpy as np

# no_sequences = 30
# words = ['hello', 'world', 'i_am', 'yash']
# DATA_PATH = '/home/yash/Desktop/Code/trackpad_text_detection/word_data/'


def seq_frame(x, model):
    m = 1919
    n = 1079
    scale = 10
    (s1, s2) = (m // scale, n // scale)

    if model=='LSTM':
        # for i, word in enumerate(words):
        #     for sequence in range(no_sequences):
        try:
            # x = np.load(os.path.join(DATA_PATH, word, str(sequence)+'.npy'))
            temp = np.zeros((s1, s2))
            frames = []
            for frame, coord in enumerate(x):
                temp[int(coord[0]//scale),int(coord[1]//scale)] = 1.0
                # npy_path = os.path.join(DATA_PATH,word + '_', str(sequence), str(frame))
                # np.save(npy_path, temp.astype('uint8'))
                frames.append(temp.flatten().astype('uint8'))
                
            frames = np.array([frames[5*i] for i in range(1100//5)])
            return frames
        except:    
            pass
        
    elif model=='CNN':
        # try:
        # x = np.load(os.path.join(DATA_PATH, word, str(sequence)+'.npy'))
        temp = np.zeros((s1, s2))
        frames = []
        for frame, coord in enumerate(x):
            temp[int(coord[0]//scale),int(coord[1]//scale)] = 1.0
            # npy_path = os.path.join(DATA_PATH,word + '_', str(sequence), str(frame))
            # np.save(npy_path, temp.astype('uint8'))
            frames.append(temp.astype('uint8'))
            
        frames = np.array([frames[4*i] for i in range(1100//4)])
        # frames = np.array(frames)
        return frames
        # except:    
        #     pass