import PIL.Image as Image
import os, cv2, random
import numpy as np
import glob
import xml.etree.ElementTree as ET
from skimage import exposure, img_as_float

def calculate_IoU(da1, da2):
    """
    computing the IoU of two boxes.
    Args:
        box: (xmin, ymin, xmax, ymax),通过左下和右上两个顶点坐标来确定矩形位置
    Return:
        IoU: IoU of box1 and box2.
    """
    pxmin, pymin, pxmax, pymax, _ = da1
    gxmin, gymin, gxmax, gymax = da2

    parea = (pxmax - pxmin) * (pymax - pymin)  # 计算P的面积
    garea = (gxmax - gxmin) * (gymax - gymin)  # 计算G的面积

    # 求相交矩形的左下和右上顶点坐标(xmin, ymin, xmax, ymax)
    xmin = max(pxmin, gxmin)  # 得到左下顶点的横坐标
    ymin = max(pymin, gymin)  # 得到左下顶点的纵坐标
    xmax = min(pxmax, gxmax)  # 得到右上顶点的横坐标
    ymax = min(pymax, gymax)  # 得到右上顶点的纵坐标

    # 计算相交矩形的面积
    w = xmax - xmin
    h = ymax - ymin
    if w <=0 or h <= 0:
        return 0

    area = w * h  # G∩P的面积
    # area = max(0, xmax - xmin) * max(0, ymax - ymin)  # 可以用一行代码算出来相交矩形的面积
    # print("G∩P的面积是：{}".format(area))

    # 并集的面积 = 两个矩形面积 - 交集面积
    IoU = area / (parea + garea - area)

    return IoU


def is_inter(xys_small, da2):
    # print(len(xys_small))
    for xy_small in xys_small:
        IoU = calculate_IoU( xy_small, da2)
        # print(IoU)
        if IoU != 0:
            return 1
    return 0

def get_xys_labels_small(path, change_size, x1, y1):
    data = []
    # -------------------------------------------------------------#
    #   对于每一个xml都寻找box
    # -------------------------------------------------------------#
    tree = ET.parse(path)
    # height = int(tree.findtext('./size/height'))
    # width = int(tree.findtext('./size/width'))
    # if height <= 0 or width <= 0:
    #     continue

    # -------------------------------------------------------------#
    #   对于每一个目标都获得它的宽高
    # -------------------------------------------------------------#
    for obj in tree.iter('object'):
        label = 0
        if obj.findtext('name') == "rope":
            label = 1
        xmin = int(int(obj.findtext('bndbox/xmin')) * change_size) + x1
        ymin = int(int(obj.findtext('bndbox/ymin')) * change_size) + y1
        xmax = int(int(obj.findtext('bndbox/xmax')) * change_size) + x1
        ymax = int(int(obj.findtext('bndbox/ymax')) * change_size) + y1


        data.append([xmin, ymin, xmax, ymax, label])

    return data
path_big = "D:/paCong/background_new/fengjing/"
fileNames_big = os.listdir(path_big)

path_sma = "D:/paCong/rope_pet_labeld/"
fileNames_sma = os.listdir(path_sma)

path_sma_label = "D:/paCong/label/"

save_path = "D:/paCong/big_small/"
max_num_small = 8

txt_path = "D:/paCong/yolov4-tf2-master/2007_val.txt"
txt_file = open(txt_path, "w")

for index_big_file_name in range(500):#len(fileNames_big)
    # index_big_file_name = random.randint(0, len(fileNames_big)-1)
    print(index_big_file_name)
    img_big = ""
    try:
        img_big = np.array(Image.open(path_big + fileNames_big[index_big_file_name]))
    except:
        continue
    img_big = cv2.cvtColor(img_big, cv2.COLOR_RGB2BGR)
    h_big, w_big, _ = img_big.shape

    xys_small = []
    num_small = random.randint(1, max_num_small)

    xys_labels_small = []
    got_num = 0
    for num in range(num_small):
        # print("max_num")
        # while True:
        #     print("while")
            # y1 = random.randint(0, h_big)
            # x1 = random.randint(0, w_big)

        ind_small_photo = random.randint(0, len(fileNames_sma)-1)
        img_sma = Image.open(path_sma + fileNames_sma[ind_small_photo])

        if not os.path.exists(path_sma_label + fileNames_sma[ind_small_photo][:fileNames_sma[ind_small_photo].find(".")] + ".xml"):
            continue

        # print(img_sma.size)
        time = 0
        change_size = 1
        while True:
            # print(time)
            if time == 20:
                break
            # print("while")
            change_size = random.randint(25, 400) / 100
            new_size = (int(img_sma.size[0] * change_size), int(img_sma.size[1] * change_size))
            # img_sma = img_sma.resize((int(img_sma.size[0]*change_size), int(img_sma.size[1]*change_size)))
            # img_sma = np.array(img_sma)

            # print((int(img_sma.shape[1]/2), int(img_sma.shape[0]/2)))
            # img_sma.resize((int(img_sma.shape[1]/2), int(img_sma.shape[0]/2), 3))


            # print(w_big , img_sma.shape[1])
            max_y = h_big - new_size[1]
            max_x = w_big - new_size[0]
            if max_x<=0 or max_y<=0:
                continue
            y1 = random.randint(0, max_y-1)
            x1 = random.randint(0, max_x-1)


            x2 = x1 + new_size[0]
            y2 = y1 + new_size[1]

            if x2 <= w_big and y2 <= h_big:
                img_sma = img_sma.resize(new_size)
                img_sma = np.array(img_sma)
                break

            time += 1

        if time == 10:
            continue

        if is_inter(xys_small, (x1, y1, x2, y2)) == 1:
            continue
        img_sma = cv2.cvtColor(img_sma, cv2.COLOR_RGB2BGR)

        light_change = random.randint(1, 37) * 0.1
        img_sma = exposure.adjust_gamma(img_sma, light_change)

        img_big[y1:y2, x1:x2] = img_sma
        # label = int(fileNames_sma[ind_small_photo].split("#")[1])
        label = 2
        xys_small.append((x1, y1, x2, y2, label))

        xys_labels_small.extend(get_xys_labels_small(path_sma_label + fileNames_sma[ind_small_photo][:fileNames_sma[ind_small_photo].find(".")] + ".xml", change_size, x1, y1))
        got_num += 1
        # print(xys_labels_small)
        # for (x1, y1, x2, y2, label) in xys_labels_small:
        #     color = (255, 255, 0)
        #     if label == 0:
        #         color = (0, 0, 255)
        #     cv2.rectangle(img_big, (x1, y1), (x2, y2), color, 2, 2)

    # print(xys_small)
    line = path_big + fileNames_big[index_big_file_name]
    for (x1, y1, x2, y2, label) in xys_labels_small:
        line += " " + str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2) + "," + str(label)
    line += "\n"
    txt_file.write(line)

    cv2.imwrite(save_path + fileNames_big[index_big_file_name], img_big)
    # cv2.imshow("cat", cv2.resize(img_big, (416, 416)))
    # cv2.waitKey()
    # break


    # IoU = calculate_IoU((1, -1, 3, 1), (0, 0, 2, 2))

txt_file.close()