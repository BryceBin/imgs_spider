from bs4 import BeautifulSoup
import os
import urllib.request




def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    web = urllib.request.Request(url=url, headers=headers)
    page = urllib.request.urlopen(web).read()
    return page


def get_main_img(soup):#获取封面图片的描述
    imgs = soup.findAll('img')#找到所有的img标签
    alt = []
    for img in imgs:
        if img.get('alt') != None:
             alt.append(img.get('alt'))
    return alt


def get_main_html(soup): #获取封面图片指向的url
    urls = soup.findAll('a') #找到所有的a标签
    htmls = []
    for url in urls:
        html = url.get('href')
        if html.startswith("http://www.win4000.com/meinv1"):
            htmls.append(html)
    return htmls


#获取图片网络地址并下载
def download(alt, htmls):
    nvs = zip(alt, htmls)
    myDict = dict((alt, htmls)for alt, htmls in nvs)
    i = 0  #计数器
    for alt1, html in myDict.items():
        path = 'D:\\learn\\python\\download_images\\'+alt1  #以图片描述命名文件夹
        if not os.path.isdir(path):#路径不存在则创建
            os.makedirs(path)
        page = get_html(html)
        soup = BeautifulSoup(page, 'html.parser')
        img_url = []  #存放每一组图片的网络地址
        img_url.append(soup.find('img', class_='pic-large').get('data-original'))#获取封面图片的网络地址
        num = soup.find('em').getText()  #获取每组图片的数量
        img_url.extend(get_imgs_url(html, num))

        count = 0
        for url in img_url:
            print("正在下载"+url)
            img_src = path + '\\' + str(count+1)+'.jpg'
            result = urllib.request.urlopen(url)
            data = result.read()
            with open(img_src, "wb") as code:
                code.write(data)
                code.close()
            count += 1
        i += 1
        print("第"+str(i)+"组完成")


def get_imgs_url(html, num):  #获取封面图片下一层的各个图片的网络地址，存放在srcs中
    srcs = []
    for i in range(int(num)-2):
        i += 2
        html1 = html[:34]+'_'+str(i)+html[34:]
        page = get_html(html1)
        soup = BeautifulSoup(page, 'html.parser')
        srcs.append(soup.find('img', class_='pic-large').get('data-original'))
    return srcs


if __name__ == '__main__':
    url = "http://www.win4000.com/meitu.html"
    page = get_html(url)
    soup = BeautifulSoup(page, 'html.parser')
    alt = get_main_img(soup)
    htmls = get_main_html(soup)
    download(alt, htmls)
