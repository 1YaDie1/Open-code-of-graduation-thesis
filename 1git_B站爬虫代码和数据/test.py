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


'''
                            《测试记录》
1、测试爬取第一个视频信息——打开的新视频会打开新页面，要注意切换页面，及时关闭不用的页面
2、关闭页面后，要给浏览器对象切换页面，不会自动切换。

'''
# -------------------------定义循环中的变量-------------------------
id = 0 # id编号
page_n = 1 # 某一页的第n个视频，从1开始
video_n = 0 # 满足爬取要求的视频数量，爬够20个，换下一页
common_list = [0,0,0,0,0]
# -------------------------定义循环中的变量-------------------------

p = 0


wait_select_present(5,'#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div > div.flex_center.mt_x50.mb_x50 > div > div > button:nth-child(11)')
browser.find_element(By.CSS_SELECTOR,'#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div > div.flex_center.mt_x50.mb_x50 > div > div > button:nth-child(11)').click()
# 模拟向下滚动，让爬虫获取页面所有信息
gun_dong_ye_mian(500, 2500)
time.sleep(1)
p += 1
print(p)

for i in range(4):
    wait_select_present(5,
                        '#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div.flex_center.mt_x50.mb_lg > div > div > button:nth-child(11)')
    browser.find_element(By.CSS_SELECTOR,
                         '#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div.flex_center.mt_x50.mb_lg > div > div > button:nth-child(11)').click()
    # 模拟向下滚动，让爬虫获取页面所有信息
    gun_dong_ye_mian(500, 2500)
    time.sleep(1)
    p += 1
    print(p)



