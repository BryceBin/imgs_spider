import csv
import urllib.request
import os
from PIL import Image


#获取QQ头像的接口
head_img_url = "http://q2.qlogo.cn/headimg_dl?bs=QQ号&dst_uin=QQ号&src_uin=QQ号&fid=QQ号&spec=100&url_enc=0&referer=bu_interface&term_type=PC"


def get_headImg_url(head_img_url):
    csv_reader = csv.reader(open('D:\\test.csv'))#读取文件
    headImg_list = []#存放头像网络地址
    name_list = []#存放备注名
    i = 0
    for qq_num in csv_reader:  # 获取头像地址和备注名
        # if i == 168:               ##在某个位置添加某个头像
        #     name_list.append('her')
        name_list.append(qq_num[0])
        headImg_list.append(head_img_url.replace('QQ号', qq_num[1]))
        i += 1

    for i in range(404):#下载头像到本地
        path = 'D:\\learn\\headImgs\\'#本地存放路径
        if not os.path.isdir(path):#路径不存在则创建
            os.makedirs(path)
        img_src = path+name_list[i]+'.jpg'
        img = urllib.request.urlopen(headImg_list[i]).read()
        with open(img_src,'wb') as f:
            f.write(img)
            f.close()
        print("第张"+str(i+1)+"下载完成")
    return  name_list


def imgs_paste(name_list):#图片拼接  20*20
    unit = 100
    toImg = Image.new('RGB',(unit*20,unit*20))
    path = 'D:\learn\headImgs\\'
    for i in range(400):
        fromImg = Image.open(path+name_list[i]+'.jpg')
        loc = ((int(i / 20) * 100), (i % 20) * 100)#确定位置
        toImg.paste(fromImg,loc)
    toImg.show()
    toImg.save('allHead.jpg')


if __name__ == '__main__':
    name_list = get_headImg_url(head_img_url)
    imgs_paste(name_list)

