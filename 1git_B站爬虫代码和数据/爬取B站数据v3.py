'''
-----------------------------------获取cookies-----------------------------------
# 1、首先模拟登录，获取B站cookies
# 导包
import time
import random
from selenium import webdriver # 谷歌浏览器插件
from selenium.webdriver.common.by import By # 定位策略
from selenium.webdriver.support.wait import WebDriverWait # 导入显式等待模块
from selenium.webdriver.support import expected_conditions as EC # 导入期望模块配合显式等待

# 网页打开时的配置代码
# 为谷歌浏览器对象修改配置（创建设置对象）
Options = webdriver.ChromeOptions()
# 不让浏览器关闭
Options.add_experimental_option("detach", True)

browser = webdriver.Chrome(executable_path='./chromedriver.exe', options=Options) # 创建谷歌浏览器对象
# 窗口最大化（因为B站每次加载显示的项目数量随页面改变）
browser.maximize_window()
URL = 'https://www.bilibili.com/'
browser.get(url=URL)

# 找到登录按钮
login_button = browser.find_element(By.CSS_SELECTOR,
                     '#i_cecream > div.bili-feed4 > div.bili-header.large-header > div.bili-header__bar > ul.right-entry > li:nth-child(1) > li > div > div > span')
# 点击登录按钮
login_button.click()

# 判断是否登录成功（显式等待60s直到用户名出现）
WebDriverWait(browser, 60).until(
    # 等待用户名出现
    EC.text_to_be_present_in_element(
        (By.CSS_SELECTOR,'#i_cecream > div.bili-feed4 > div.bili-header.large-header > div.bili-header__bar > ul.right-entry > li.v-popover-wrap.header-avatar-wrap > div.v-popover.is-bottom > div > div > a.nickname-item'),
        '疋瓞'
    ))
print('登录成功！')
# 登录成功以后获取cookie，将cookie保存到文件中
cookies = browser.get_cookies()
# cookie是字典，cookies是cookie的复数，是一个列表。
with open('Bili_cookies.txt', 'w', encoding='utf-8') as file:
    file.write(str(cookies))
print('cookies写入完成！')
browser.quit() # 关闭所有标签页
-----------------------------------获取cookies-----------------------------------
'''

# 2、使用cookies登录【cookies隔一段时间会失效】
# 导包
import csv
import time
import random
from selenium import webdriver # 谷歌浏览器插件
from selenium.webdriver.common.by import By # 定位策略
from selenium.webdriver.support.wait import WebDriverWait # 导入显式等待模块
from selenium.webdriver.support import expected_conditions as EC # 导入期望模块配合显式等待

# 网页打开时的配置代码
# 为谷歌浏览器对象修改配置（创建设置对象）
Options = webdriver.ChromeOptions()
# 不让浏览器关闭
Options.add_experimental_option("detach", True)

browser = webdriver.Chrome(executable_path='./chromedriver.exe', options=Options) # 创建谷歌浏览器对象
# 窗口最大化（因为B站每次加载显示的项目数量随页面改变）
browser.maximize_window()
URL = 'https://www.bilibili.com/'
browser.get(url=URL)

# 给浏览器添加cookie，添加完成后要刷新下页面
with open('Bili_cookies.txt','r') as file:
    cookies = eval(file.read()) # 将字符串识别为python代码
for i in cookies:
    browser.add_cookie(i)
browser.refresh() # 刷新页面才能显示cookies添加之后的效果

# 3、爬取信息
# -----------------------------------封装部分常用函数-----------------------------------
# 页面滚动函数，调用页面滚动js代码，让页面加载出所有信息，这样爬虫就能获取所有信息
def gun_dong_ye_mian(stp_1, max_s):
    y = 0
    while True:
        # 每次滚动500像素点
        y += stp_1
        # selenium调用页面滚动的方法
        # execute_script()可以执行js代码
        browser.execute_script(f'window.scrollTo(0, {y})')
        # 滚动一次休眠一次（防止被检测到是爬虫）
        time.sleep(random.randint(1, 2))
        # 猜测页面高度为6000像素点
        if y >= max_s:
            break

# 等待选择器出现的函数
# t_w: 规定等待时长
# select_str: 选择器
def wait_select_present(t_w, select_str):
    # 使用CSS选择器等待元素出现和加载完成
    elem = WebDriverWait(browser, t_w).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, select_str))
    )

# 跳转到新打开的页面
def switch_window(num):
    browser.switch_to.window(browser.window_handles[num])

# -----------------------------------封装部分常用函数-----------------------------------

# 在搜索框检索视频名称
video_name = '0基础学习python'
time.sleep(1)
browser.find_element(By.CSS_SELECTOR,'#nav-searchform > div.nav-search-content > input').send_keys(video_name) # 向输入框输入信息
browser.find_element(By.CSS_SELECTOR,'#nav-searchform > div.nav-search-btn > svg').click() # 点击搜索按钮

# 加休眠防止反扒
time.sleep(1)
switch_window(-1) # 切换到新页面

# 模拟向下滚动，让爬虫获取页面所有信息
gun_dong_ye_mian(500, 2500)

# 构造数据持久化的框架
file = open('爬取B站0基础学习python课程数据v3.csv', mode='w', encoding='utf-8', newline='')
# newline='' --> 如果不写，windows系统下csv文件每一行数据后面会有一行空行。
# 写列名
colName = ['id编号', '标题', '点赞数量', '投币数量', '收藏数量', '播放次数',
           '评论1','评论2','评论3','评论4','评论5']
csv.writer(file).writerow(colName)

'''
                            《测试记录》
1、测试爬取第一个视频信息——打开的新视频会打开新页面，要注意切换页面，及时关闭不用的页面
2、关闭页面后，要给浏览器对象切换页面，不会自动切换。
3、搜索结果中的第一页css选择器和其他页css选择器可能会不同。

'''
# -------------------------定义循环中的变量-------------------------
id = 0 # id编号
page_n = 1 # 某一页的第n个视频，从1开始
video_n = 0 # 满足爬取要求的视频数量，爬够20个，换下一页
common_list = [0,0,0,0,0]

n = 1 # 记录是第几页
# -------------------------定义循环中的变量-------------------------

# 爬取200条信息
while True:
    # 循环终止条件：id == 200
    if id == 200:
        break

    # 每一页爬够20条或者遍历超过30条，点击下一页继续
    if(video_n == 20)or(page_n > 30):
        video_n = 0
        page_n = 1
        n += 1
        # 点击下一页，进入下一页
        if n == 2: # 第一页
            wait_select_present(5,
                                '#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div > div.flex_center.mt_x50.mb_x50 > div > div > button:nth-child(11)')
            browser.find_element(By.CSS_SELECTOR,
                                 '#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div > div.flex_center.mt_x50.mb_x50 > div > div > button:nth-child(11)').click()
            # 模拟向下滚动，让爬虫获取页面所有信息
            gun_dong_ye_mian(500, 2500)
            time.sleep(1)
        else:
            wait_select_present(5,
                               '#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div.flex_center.mt_x50.mb_lg > div > div > button:nth-child(11)')
            browser.find_element(By.CSS_SELECTOR,
                                 '#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div.flex_center.mt_x50.mb_lg > div > div > button:nth-child(11)').click()
            # 模拟向下滚动，让爬虫获取页面所有信息
            gun_dong_ye_mian(500, 2500)
            time.sleep(1)

    # 查看视频是否是up主视频
    if n == 1: # 第一页
        wait_select_present(10,f'#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div > div.video.i_wrapper.search-all-list > div > div:nth-child({page_n}) > div > div.bili-video-card__wrap.__scale-wrap > div > div > p > a > svg')
        is_up = browser.find_element(By.CSS_SELECTOR,f'#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div > div.video.i_wrapper.search-all-list > div > div:nth-child({page_n}) > div > div.bili-video-card__wrap.__scale-wrap > div > div > p > a > svg').get_attribute('class')
    else: # 其他页
        wait_select_present(10,f'#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div.video-list.row > div:nth-child({page_n}) > div > div.bili-video-card__wrap.__scale-wrap > div > div > p > a > svg')
        is_up = browser.find_element(By.CSS_SELECTOR,f'#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div.video-list.row > div:nth-child({page_n}) > div > div.bili-video-card__wrap.__scale-wrap > div > div > p > a > svg').get_attribute('class')

    if is_up == 'bili-video-card__info--author-ico mr_2': # 是up主视频可以爬取
        id += 1
        # 点击视频
        if n == 1:
            wait_select_present(5,f'#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div > div.video.i_wrapper.search-all-list > div > div:nth-child({page_n}) > div > div.bili-video-card__wrap.__scale-wrap > a')
            browser.find_element(By.CSS_SELECTOR,f'#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div > div.video.i_wrapper.search-all-list > div > div:nth-child({page_n}) > div > div.bili-video-card__wrap.__scale-wrap > a').click()
        else:
            wait_select_present(5,f'#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div.video-list.row > div:nth-child({page_n}) > div > div.bili-video-card__wrap.__scale-wrap > a')
            browser.find_element(By.CSS_SELECTOR,f'#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div.video-list.row > div:nth-child({page_n}) > div > div.bili-video-card__wrap.__scale-wrap > a').click()
        switch_window(-1)  # 切换网页

        # 标题
        wait_select_present(5,'#viewbox_report > h1')
        v_title = browser.find_element(By.CSS_SELECTOR,'#viewbox_report > h1').text

        # # up主名称
        # wait_select_present(5,'#app > div.video-container-v1 > div.right-container.is-in-large-ab > div > div.up-panel-container > div.up-info-container > div.up-info--right > div.up-info__detail > div > div.up-detail-top > a')
        # v_up_name = browser.find_element(By.CSS_SELECTOR, '#app > div.video-container-v1 > div.right-container.is-in-large-ab > div > div.up-panel-container > div.up-info-container > div.up-info--right > div.up-info__detail > div > div.up-detail-top > a').text

        # # 关注数量：文本是被CSS样式隐藏的，使用JavaScript来获取元素的innerText
        # wait_select_present(5,'#app div.video-container-v1 div.up-info-container div.upinfo-btn-panel span.follow-btn-inner')
        # v_focus_num = browser.execute_script("return arguments[0].innerText;", browser.find_element(By.CSS_SELECTOR, '#app div.video-container-v1 div.up-info-container div.upinfo-btn-panel span.follow-btn-inner'))
        # v_focus_num = v_focus_num[-16:] # 获取最后16位

        # 点赞数量
        wait_select_present(5,'#arc_toolbar_report > div.video-toolbar-left > div:nth-child(1) > div > span')
        v_like_num = browser.find_element(By.CSS_SELECTOR, '#arc_toolbar_report > div.video-toolbar-left > div:nth-child(1) > div > span').text

        # 投币数量 #arc_toolbar_report > div.video-toolbar-left > div:nth-child(2) > div > span
        wait_select_present(5,'#arc_toolbar_report > div.video-toolbar-left > div:nth-child(2) > div > span')
        v_money_num = browser.find_element(By.CSS_SELECTOR, '#arc_toolbar_report > div.video-toolbar-left > div:nth-child(2) > div > span').text

        # 收藏数量
        wait_select_present(5,'#arc_toolbar_report > div.video-toolbar-left > div:nth-child(3) > div > span')
        v_collect_num = browser.find_element(By.CSS_SELECTOR, '#arc_toolbar_report > div.video-toolbar-left > div:nth-child(3) > div > span').text

        # 播放次数
        wait_select_present(5,'#viewbox_report > div > div > span.view.item')
        v_play_num = browser.find_element(By.CSS_SELECTOR, '#viewbox_report > div > div > span.view.item').text

        # 模拟向下滚动，让爬虫获取页面所有信息
        gun_dong_ye_mian(500, 2500)

        # 评论数据获取
        for i in range(5):
            try:
                wait_select_present(10,
                                    f'#comment > div > div > div > div.reply-warp > div.reply-list > div:nth-child({i+1}) > div.root-reply-container > div.content-warp > div.root-reply > span > span')
                common_list[i] = browser.find_element(By.CSS_SELECTOR,
                                                   f'#comment > div > div > div > div.reply-warp > div.reply-list > div:nth-child({i+1}) > div.root-reply-container > div.content-warp > div.root-reply > span > span').text
            except Exception as e:  # 如果出现了异常
                common_list[i] = 0

        browser.close()
        print('-' * 50,id)
        print('like:',v_like_num)
        print('money:',v_money_num)
        print('collect',v_collect_num)
        print('v_play_num',v_play_num)
        print('comment:',common_list)

        # 存放到csv
        col = [id, v_title, v_like_num, v_money_num, v_collect_num, v_play_num,
                   common_list[0],common_list[1],common_list[2],common_list[3],common_list[4]]
        csv.writer(file).writerow(col)
        video_n += 1
        switch_window(-1)

    page_n += 1

# 最后要关闭文件
file.close()


