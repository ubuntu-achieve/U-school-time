import time
from warnings import filterwarnings
from selenium import webdriver
from msedge.selenium_tools import Edge
from msedge.selenium_tools import EdgeOptions

filterwarnings("ignore",category=DeprecationWarning)

url1 = 'https://sso.unipus.cn/sso/login?service=https%3A%2F%2Fu.unipus.cn%2Fuser%2Fcomm%2Flogin%3Fschool_id%3D'
url2 = 'https://u.unipus.cn/user/student'

reqr = ''
usr = ''
usr_name = input("请输入用户名：")
while usr_name == '000':
    print("进入测试模式！")
    web = input("请输入你使用的浏览器：(1或2)\n1代表Chrome\t2代表Edge\n")
    if '1' == web:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 去除selenium的浏览器警告
        try:
            driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
            sf = input("web启动器正常，是否仍要修改路径？(y/n)")
            if sf == 'y':
                usr = input("请输入你在电脑上的用户名：")
            driver.quit()
        except:
            print("web启动器出错，请将web启动器放在桌面再试")
            usr = input("请输入你在电脑上的用户名：")
            driver = webdriver.Chrome('C:\\Users\\' + usr + '\\Desktop\\chromedriver.exe', options=options)
            driver.quit()
    else:
        options = EdgeOptions()
        options.add_experimental_option('excludeSwitches', ['enable--logging'])
        try:
            driver = Edge(executable_path="edgedriver.exe", options=options)
            sf = input("web启动器正常，是否仍要修改路径？(y/n)")
            if sf == 'y':
                usr = input("请输入你在电脑上的用户名：")
            driver.quit()
        except:
            print("web启动器出错，请将web启动器放在桌面再试")
            usr = input("请输入你在电脑上的用户名：")
            driver = Edge('C:\\Users\\' + usr + '\\Desktop\\edgedriver.exe', options=options)
            driver.quit()
    print("若刚才有浏览器窗口闪过则表明程序成功调起，若仍不成功请尝试将web启动器换至对应版本！")
    reqr = input("是否退出调试模式？y/n")
    if reqr == 'y':
        usr_name = input("请输入用户名：")
        break
passwd = input("请输入密码：")
order = int(input("请输入每个单元的的期望挂机时长（单位为小时）："))
if reqr != 'y' or usr == '':
    web = input("请输入你使用的浏览器：(1或2)\n1代表Chrome\t2代表Edg\n")
    if '1' == web:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    else:
        options = EdgeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = Edge(executable_path="edgedriver.exe", options=options)
else:
    web = input("请输入你使用的浏览器：(1或2)\n1代表Chrome\t2代表Edge\n")
    if '1' == web:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome('C:\\Users\\' + usr + '\\Desktop\\chromedriver.exe', options=options)
    else:
        options = EdgeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = Edge('C:\\Users\\' + usr + '\\Desktop\\edgedriver.exe' ,options=options)
        
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
driver.get(url1)
driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/form/div[1]/input').send_keys(usr_name)
driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/form/div[2]/input').send_keys(passwd)
driver.find_element_by_xpath('//*[@id="login"]').click()
driver.get(url2)
driver.get(url2)  # 去除环境测试，不知道为什么要两次才能覆盖
driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div[2]/div/div[2]/div[1]/div/div[1]').click()
driver.find_element_by_xpath('//*[@id="classDiagNav"]/li').click()
driver.implicitly_wait(10)
time_all = driver.find_element_by_xpath('//*[@id="StudentReport"]/div/div/div/div[1]/div[2]/div[1]/div[1]')
print('总学习时长：',time_all.text)
alltxt = driver.find_element_by_xpath('//*[@id="StudentReport"]/div/div/div/div[3]').text
unint = 0
for i in alltxt.split('\n'):
    if 'Unit'in i:
        unint += 1 
print(f'共有{unint}个单元，请核对数目是否正确！')
times = []
for i in range(unint):
    times.append(driver.find_element_by_xpath('//*[@id="StudentReport"]/div/div/div/div[4]/table/tbody[' + str(i+1) + ']/tr[1]/td[2]').text)
    if times[i] == '':
        print(f'{i+1}单元未完成！')
    else:
        print(f'{i+1}单元时长为：{times[i]}')
driver.find_element_by_xpath('//*[@id="courseIndexNav"]/li').click()
driver.implicitly_wait(10)
url = driver.current_url
for i in range(len(times)):  # 开始挂机
    driver.implicitly_wait(10)
    if times[i] != '' and (int(times[i].split(':')[0])*60+int(times[i].split(':')[1])) < order*60:
        time.sleep(2)
        try:
            driver.find_element_by_xpath('//*[@id="menuBox"]/ul[' + str(i+1) + ']/li[2]/div[2]/div/span[2]/a/span').click()
        except :
            yx = True
            while yx == True:
                try:
                    driver.find_element_by_xpath('//*[@id="menuBox"]/ul[' + str(i+1) + ']/li[2]/div[2]/div/span[2]/a/span').click()
                    yx =False
                except :
                    yx = True
                    time.sleep(2)

        driver.implicitly_wait(10)
        try:
            driver.find_element_by_xpath('/html/body/div[3]/div/section/div[2]/div[2]/span').click()
        except:
            pass
        try:
            try:
                driver.find_element_by_xpath('/html/body/div[10]/div/div[1]/div/div/div[3]/div/button/div/div/span').click()
            except:
                try:
                    driver.find_element_by_xpath('/html/body/div[11]/div/div[1]/div/div/div[3]/div/button/div/div/span').click()
                except:
                    driver.find_element_by_xpath('/html/body/div[9]/div/div[1]/div/div/div[3]/div/button/div/div/span').click()
        except:
            pass
        gtime = order*60 -(int(times[i].split(':')[0])*60+int(times[i].split(':')[1]))
        total = gtime
        print(f"\r正在为{i+1}单元挂机，预计挂机时长为：{gtime}分钟", end='')
        while True:
            string = "挂机进行中，还有{:.2f}分钟完成".format(gtime)
            start = time.time()
            time.sleep(5)
            gtime -= (time.time() - start)/60
            try:
                driver.find_element_by_xpath('//*[@id="muti0"]').click()
                string += "(已触发按键1)"
            except:
                try:
                    driver.find_element_by_xpath('//*[@id="main-top"]/div[3]/div/div[2]/div[1]/div[1]/div/div/div[2]/div/div/span/input').click()
                    driver.find_element_by_xpath('//*[@id="main-top"]/div[3]/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div/span/input').click()
                    string += "(按键1触发失败，已触发按键2)"
                except:
                    driver.find_element_by_xpath('//*[@id="main-top"]/div[3]/div/div[2]/div[1]/div[1]/div/div/ul/li[1]/label/input').click()
                    driver.find_element_by_xpath('//*[@id="main-top"]/div[3]/div/div[2]/div[1]/div[1]/div/div/ul/li[2]/label/input').click()
                    string += "(按键2触发失败，已触发按键3)"
            print(f"\r{string}", end='')
            if gtime < 0:
                break
        print(f"\n{i+1}单元时长已达到")
        driver.implicitly_wait(10)
        time.sleep(2)
        driver.get(url)
        print("已切换到章节页面")
    elif times[i] != '':
        print(f"{i+1}单元时长已达到")
    else:
        print(f"{i+1}单元未学习")

driver.get(url)
driver.find_element_by_xpath('//*[@id="classDiagNav"]/li').click()
driver.implicitly_wait(10)
for i in range(unint):
    times.append(driver.find_element_by_xpath('//*[@id="StudentReport"]/div/div/div/div[4]/table/tbody[' + str(i+1) + ']/tr[1]/td[2]').text)
    if times[i] == '':
        print(f'{i+1}单元未完成！')
    else:
        print(f'{i+1}单元时长为：{times[i]}')
print("已刷完全部内容！")
driver.quit()
