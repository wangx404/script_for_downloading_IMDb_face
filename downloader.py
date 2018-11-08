# -*- coding: utf-8 -*-

import os, requests, math
import multiprocessing
import cv2

root_dir = 'IMDB_clean_face/' # dir to save face
temp_dir = 'IMDB_temp/' # dir to save raw image temporarily
csv_file = 'IMDb-Face.csv' # csv file contains image information
threads = 8 # processing number to download images
            # actually you can use numtil thread module in python rather than multiprocessing
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
# make a temporary dir for raw images
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

def getURLList():
    '''parse csv file, and return a list after simple-processing.'''
    with open(csv_file, 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [line.split(',') for line in lines]
    return lines[1:] # remove head line

def getCoordinate(rect):
    '''get face coordinates in format of xmin, ymin, xmax, ymax'''
    rect = rect.split(' ')
    rect = [int(p) for p in rect]
    return rect

def getHeightWidth(hw):
    '''get raw height and width of image'''
    hw = hw.split(' ')
    hw = [int(p) for p in hw]
    return hw

def faceCrop(img, xmin, ymin, xmax, ymax, scale_ratio=2):
    '''
    crop face from image, the scale_ratio used to control margin size around face.
    using a margin, when aligning faces you will not lose information of face
    '''
    if type(img) == str:
        img = cv2.imread(img)

    hmax, wmax, _ = img.shape
    x = (xmin + xmax) / 2
    y = (ymin + ymax) / 2
    w = (xmax - xmin) * scale_ratio
    h = (ymax - ymin) * scale_ratio
    # new xmin, ymin, xmax and ymax
    xmin = x - w/2
    xmax = x + w/2
    ymin = y - h/2
    ymax = y + h/2
    # 大小修正
    xmin = max(0, int(xmin))
    ymin = max(0, int(ymin))
    xmax = min(wmax, int(xmax))
    ymax = min(hmax, int(ymax))
    
    face = img[ymin:ymax,xmin:xmax,:]
    return face

def downloadImage(line, scale_ratio):
    '''download image and crop face from raw image'''
    name, index, image, rect, hw, url = line
    image_file = '_'.join([index, image])
    # make dir
    if not os.path.exists(os.path.join(root_dir, name)):
        os.makedirs(os.path.join(root_dir, name))
    # jump downloaded image
    if os.path.exists(os.path.join(root_dir, name, image_file)):
        return 
    
    # try download image
    temp_image_file = os.path.join(temp_dir, image_file)
    try:
        image_data = requests.get(url, headers=headers)
        if not image_data.ok: # there are some wrong urls
            return
        with open(temp_image_file, 'wb') as f:
            f.write(image_data.content)
    except Exception as e:
        print('Wrong with: ', url, '\nError info: ', e)
        return
    
    # check image size
    right_height, right_width = getHeightWidth(hw)
    img = cv2.imread(temp_image_file)
    real_height, real_width, _ = img.shape
    if (right_height != real_height) or (right_width != real_width):
        if abs(right_height/right_width - real_height/real_width) < 0.01:
            img = cv2.resize(img, (right_width, right_height))
        else:
            return # real image size not equal to record
    
    # crop face from image
    location = getCoordinate(rect)
    face = faceCrop(img, *location, scale_ratio)
    image_file = os.path.join(root_dir, name, image_file)
    cv2.imwrite(image_file, face)
    # delete temp image file to save disk space
    os.remove(temp_image_file)
        
def downloadImages(threads, thread_index):
    '''download images in one thread'''
    print('Thread %d start.' % thread_index)
    image_lines = getURLList()
    length = math.ceil(len(image_lines)/threads)
    image_lines = image_lines[thread_index*length: (thread_index+1)*length]
    for line in image_lines:
        try:
            downloadImage(line, 2.0)
        except Exception as e:
            print(line, e)
            continue

def multiThreadsDownloadImages(threads):
    '''using multiprocessing to download images'''
    pool = multiprocessing.Pool(processes=threads)
    for thread_index in range(threads):
        pool.apply_async(downloadImages, (threads, thread_index))
    pool.close()
    pool.join()
    
if __name__ == '__main__':
    multiThreadsDownloadImages(8)
