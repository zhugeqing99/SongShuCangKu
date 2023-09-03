from bs4 import BeautifulSoup as bf
import re,json,winreg,requests,os,time,random

def get_proxy_address():
    try:
        # 打开注册表项
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\Microsoft\Windows\CurrentVersion\Internet Settings')
        
        # 读取代理服务器地址
        proxy_address, _ = winreg.QueryValueEx(reg_key, 'ProxyServer')
        
        # 关闭注册表项
        winreg.CloseKey(reg_key)
        
        return proxy_address
    except Exception as e:
        print(f"Error: {e}")
        return None


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Cookie': 'PHPSESSID=2hopg0kb7n6adkljtka9i3cqfi; minifyMenu=0; message_alert=Show; ahri=1; cpopacc=%7B%220_exoclick%22%3A1693677625%2C%221_exoclick%22%3A1693677739%2C%222_exoclick%22%3A1693677761%2C%22%22%3A1693677872%7D',
    'Pragma': 'no-cache',
    'Sec-Ch-Ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}


proxies={
'http':'http://{}'.format(get_proxy_address()),
'https':'http://{}'.format(get_proxy_address()),
}



def main(url:str,save_dir:str,comic_name):
    #构建存储路径:save_dir+comic_name
    save_dir=os.path.sep.join([save_dir,comic_name])

    #如果路径不存在就创建
    if(not os.path.exists(save_dir)):
        os.makedirs(save_dir)
    #根据主页URL构建浏览页面的URL
    id=url.split("?")[1]
    first_page_url="https://ahri8.top/readOnline2.php?{}&host_id=1&page=1&gallery_brightness=100&gallery_contrast=100".format(id)

    #请求浏览页面
    requests_data=requests.get(url=first_page_url,proxies=proxies,headers=headers)

    #获取图片列表并构建为json
    #图片列表是直接存储在页面上的一个javascript中的，使用如下正则表达式可以提取出来
    pattern = r'Original_Image_List =\s*\[[^\]]*\]'
    match = re.search(pattern, requests_data.text).group().split("=")[1]
    img_json=json.loads(match)
    
    #遍历每一个图片开始下载
    for item in img_json:

        #获取各种信息
        sort=item["sort"]
        comic_id=item["comic_id"]
        new_file_name=item["new_filename"]
        extension=item["extension"]

        #构建最终的图片URL
        img_url="https://img.ehentai.top/comic/thumbnail/105000/d-{}/{}_w1100.{}".format(comic_id,new_file_name,extension)

        #构建图片的存储路径
        img_save_path=os.path.sep.join([save_dir,"{}.{}".format(sort,extension)])

        #如果图片已经存在就跳过，不在就开始下载
        if(not os.path.exists(img_save_path)):

            #随机等待一会儿免得被封IP
            time.sleep(random.randint(1, 5))

            #下载图片
            img_data=requests.get(img_url,proxies=proxies,headers=headers).content

            #存储
            with open(img_save_path,"wb+") as f:
                f.write(img_data)
                f.flush()
                f.close()
                print("\r 下载进度：：{}/{}".format(img_json.index(item),len(img_json)),end='',flush=True)
        


if(__name__=="__main__"):
    #注意，这个脚本需要魔法
    MainPageUrl="https://ahri8.top/post.php?ID=104120"  #想下的本子首页URL
    Save_dir="c:\\test"                                 #注意，window下路径应该是双斜杠\\
    comic_name="纯爱カノジョ"                   #因为这个网站把名字加密了，，，python解密有点痛苦，还是先手动输入一下吧~
    main(MainPageUrl,Save_dir,comic_name)

