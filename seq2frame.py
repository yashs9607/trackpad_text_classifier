import os
import numpy as np

no_sequences = 30
words = ['hello', 'world', 'i_am', 'yash']
DATA_PATH = '/home/yash/Desktop/Code/trackpad_text_detection/word_data/'
# x = [np.load("".join(DATA_PATH + i + '/' + str(j) + '.npy')) for i in words for j in range(no_sequences)]
# print(x)

for word in words:
    for sequence in range(no_sequences):
    # for sequence in range(no_sequences):
        try:
            os.makedirs(os.path.join(DATA_PATH, word + '_', str(sequence)))
        except:
            pass


m = 1919
n = 1079
# a = 178
# b = 100
scale = 10
(s1, s2) = (m // scale, n // scale)

for i, word in enumerate(words):
    for sequence in range(no_sequences):
        try:
        
            # x = np.load(("".join(DATA_PATH + word + '/' + str(shot) + '.npy')))
            x = np.load(os.path.join(DATA_PATH, word, str(sequence)+'.npy'))
            # np.save()
            
            # frame = []
            # temp = np.zeros((1919, 1079))
            # for coord in x[i*no_sequences + shot]:
            #     # print(coord)
            #     temp[int(coord[0])][int(coord[1])] = 1.0
            #     frame.append(np.array(temp))
            # shot.append(np.array(frame))
            # print(x)
            temp = np.zeros((s1, s2))
            for frame, coord in enumerate(x):
                temp[int(coord[0]//scale),int(coord[1]//scale)] = 1.0
                npy_path = os.path.join(DATA_PATH,word + '_', str(sequence), str(frame))
                # temp = np.array(temp)[::s1][::s2]
                np.save(npy_path, temp.astype('uint8'))
                # print(np.mean(temp))
                
        except:    
            pass
