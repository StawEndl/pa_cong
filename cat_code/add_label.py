import PIL.Image as Image
import os, cv2, random
import numpy as np

path = "D:/paCong/roped_Affenpinscher/"
file_names = os.listdir(path)

save_path = "D:/paCong/0/"

for index in range(len(file_names)):
    print(index, file_names[index])
    img = cv2.imread(path + file_names[index])
    # img = cv2.imdecode(np.fromfile(path + file_names[index], dtype=np.uint8), -1)
    # print(img.shape)
    # cv2.imwrite(save_path + "new_photo" + str(index) +"#1#.jpg", img)
    cv2.imwrite(save_path + file_names[index][0:file_names[index].index(".")] + "#0#.jpg", img)