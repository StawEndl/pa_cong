import PIL.Image as Image
import os, cv2, random
import numpy as np


def create_hphoto(fileNames, path):
    ind = random.randint(0, len(fileNames)-1)
    new_img = np.array(Image.open(path + fileNames[ind]).resize((256, 256)))
    for i in range(5):
        ind = random.randint(0, len(fileNames)-1)
        img = np.array(Image.open(path + fileNames[ind]).resize((256, 256)))
        # print(img.shape)

        new_img = np.hstack((new_img, img))
        # print(new_img.shape)
    return new_img


def create_big_photo(fileNames, path, save_path, index_photo):
    new_img = create_hphoto(fileNames, path)
    # print("new_img", new_img.shape)
    for _ in range(5):
        img = create_hphoto(fileNames, path)
        # print(img.shape)
        new_img = np.vstack((new_img, img))
        # print(new_img.shape)

    cv2.imwrite(save_path + str(index_photo) + ".jpg", new_img)
    # print(new_img.shape)
    # cv2.imshow("new_img", new_img)
    #
    # cv2.waitKey()

path = 'D:/paCong/background/'
save_path = 'D:/paCong/cat/'
filePath = path
fileNames = os.listdir(filePath)
# new_img = np.empty(shape=(256, 256, 3))
# ind = random.randint(0, len(fileNames))
# new_img = np.array(Image.open(path + fileNames[ind]))
# print(img1.shape)

for num_photo in range(5000):
    print(num_photo)
    create_big_photo(fileNames, path, save_path, num_photo)