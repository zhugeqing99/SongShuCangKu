import re,json,winreg,requests,os,time,random
import tkinter as tk
import threading



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
    
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',  
    'Pragma': 'no-cache',
    'Sec-Ch-Ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    "Cookis":"minifyMenu=0; Lang=SC; PHPSESSID=4mobpkt8lv0s66l2iob7o5hn45; message_alert=Show; ahri=1; cpopacc=%7B%220_exoclick%22%3A1694612097%2C%221_exoclick%22%3A1694611965%2C%222_exoclick%22%3A1694611970%2C%22%22%3A1694612362%7D"
}


proxies={
'http':'http://{}'.format(get_proxy_address()),
'https':'http://{}'.format(get_proxy_address()),
}


def LOG(log:str):
    # 将光标移动到多行输入框的结尾
    log_tex.tag_add(tk.SEL, "1.0", tk.END)
    log_tex.see(tk.END)

    # 在多行输入框的结尾处插入一段文本
    log_tex.insert(tk.END, log)

    # 将光标移动到多行输入框的结尾
    log_tex.tag_add(tk.SEL, "1.0", tk.END)
    log_tex.see(tk.END)


def main(url:str,save_dir:str,comic_name):
    # 设置按钮为不可点击状态
    button.config(state="disabled")

    #构建存储路径:save_dir+comic_name
    save_dir=os.path.sep.join([save_dir,comic_name])

    #如果路径不存在就创建
    if(not os.path.exists(save_dir)):
        LOG("存储路径{}不存在，已经创建！\n".format(save_dir))
        os.makedirs(save_dir)
    #根据主页URL构建浏览页面的URL
    id=url.split("?")[1]
    first_page_url="https://ahri8.top/readOnline2.php?{}&host_id=1&page=1&gallery_brightness=100&gallery_contrast=100".format(id)

    #请求浏览页面
    requests_data=requests.get(url=first_page_url,proxies=proxies,headers=headers)


    #获取图片列表并构建为json
    #图片列表是直接存储在页面上的一个javascript中的，使用如下正则表达式可以提取出来
    pattern = r'Original_Image_List =\s*\[[^\]]*\]'
    match = re.search(pattern, requests_data.text)
    if match:
        value = match.group().split("=")[1]
    else:
        button.config(state="normal")
        LOG("下载失败\n")
        return
       

    img_json=json.loads(value)
    
    LOG("共获取到{}张图片\n".format(len(img_json)))
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
                log_text="下载进度：：{}/{}\n".format(img_json.index(item),len(img_json))
                LOG(log_text)

    LOG("下完了~~~\n")
    # 设置按钮为可点击状态
    button.config(state="normal")
        


if(__name__=="__main__"):
    #注意，这个脚本需要魔法
    #MainPageUrl="https://ahri8.top/post.php?ID=104120"  #想下的本子首页URL
    #Save_dir="c:\\test"                                 #注意，window下路径应该是双斜杠\\
    #comic_name="纯爱カノジョ"                   #因为这个网站把名字加密了，，，python解密有点痛苦，还是先手动输入一下吧~
    #main(MainPageUrl,Save_dir,comic_name)

    def on_button_click():
        # 处理按钮点击事件
        thread=threading.Thread(target=main,args=([MainPageUrlentry.get(),SaveDirentry.get(),Nameentry.get()]))
        thread.start()

        pass

    # 创建主窗口
    window = tk.Tk()
    window.geometry("400x600")
    item_width=45
    tips_lable=tk.Label(window,text="这个工具需要开梯子\n另外漫画的名字需要手动输入一下\n原因是原始网站加密了这部分内容\n解密实在蛋疼")
    tips_lable.grid(row=0,column=0,pady=5,columnspan=2)
    # 创建输入框和按钮
    MainPageUrlLable=tk.Label(window,text="主页URL")
    MainPageUrlentry = tk.Entry(window,width=item_width)
    MainPageUrlentry.insert(tk.END,"https://ahri8.top/post.php?ID=xxxxxxx")

    SaveDirLable=tk.Label(window,text="存储路径")
    SaveDirentry = tk.Entry(window,width=item_width)
 

    NameLable=tk.Label(window,text="漫画名称")
    Nameentry = tk.Entry(window,width=item_width)

    
    button = tk.Button(window, text="点击", command=on_button_click,width=item_width)

    # 设置元素之间的间隔
    MainPageUrlLable.grid(row=1,column=0,pady=5)
    MainPageUrlentry.grid(row=1,column=1,pady=5)

    SaveDirLable.grid(row=2,column=0,pady=5)
    SaveDirentry.grid(row=2,column=1,pady=5)

    NameLable.grid(row=3,column=0,pady=5)
    Nameentry.grid(row=3,column=1,pady=5)

    button.grid(row=4,column=0,pady=5,columnspan=2)

    log_tex=tk.Text(window,width=item_width,height=25)
    log_tex.grid(row=5,column=0,pady=5,columnspan=2)

    # 进入主循环
    window.mainloop()

