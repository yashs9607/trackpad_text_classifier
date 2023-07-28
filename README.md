# trackpad_text_classifier
Takes handwritten imput from trackpad and classifies into text
[Screencast from 2023-07-28 16-18-45.webm](https://github.com/yashs9607/trackpad_text_classifier/assets/81021436/edd888e8-e701-47dd-8bf6-c2c7a968df5b)

<video width=300 height=600 src="https://github.com/yashs9607/trackpad_text_classifier/assets/81021436/edd888e8-e701-47dd-8bf6-c2c7a968df5b"></video>

## If you want to train it on your handwriting run gen_data.py to take samples.
  1. trackpad touch data is collected using libinput.
  2. change the words list to target label.
  3. currently has four labels each takes 30 samples. (change it from variable no_samples)
  4. USE DOWN ARROW KEY when you are finished giving a sample. (0,0) will be passed as input regardless of trackpad input.

## OR

## Try the model directly from demo.[Screencast from 2023-07-28 16-18-45.webm](https://github.com/yashs9607/trackpad_text_classifier/assets/81021436/5e453851-83ef-4f85-b7ba-a721e0205efc)

  1. demo uses model2_2.h5 weights which are trained on my data
  2. prediction will be out for previous input not the currently written word.

## IMPORTANT
  1. Mouse pointer is YET to be fixed while writing.
  2. every input (get_data or demo) only takes a fixed no. of inputs and then resets(roughly able to write a 4-5 letter word). adjust it from WINDOW_SIZE variable.
  3. Runs on a single thread which depends on the input from trackpad. move mouse pointer to execute the latest input.
