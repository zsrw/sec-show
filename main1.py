from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import psutil
import os

def openBrown():
    # port = {"port":8811}
    server = Server(r"E:\Work\crawler\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat")
    server.start()
    proxy = server.create_proxy()

    chrome_option = Options()
    chrome_option.add_argument('--proxy-server={0}'.format(proxy.proxy))
    # chrome_option.add_argument('--headless')
    # chrome_option.add_argument('--disable-gpu')
    chrome_option.binary_location = "D:\Program Files\Google Chrome\App\Google Chrome\chrome.exe"
    # r = requests.post('http://localhost:8080/proxy', data = {'trustAllServers':'true'})
    capabilities = webdriver.DesiredCapabilities().CHROME
    capabilities['acceptInsecureCerts'] = True
    driver = webdriver.Chrome(options=chrome_option, desired_capabilities=capabilities)
    base_url = "http://www.baidu.com"
    proxy.new_har("baidu", options={'captureHeaders': True, 'captureContent': True})
    time.sleep(1)
    driver.get(base_url)
    time.sleep(1)
    driver.find_element_by_id("kw").send_keys("hao123 天气")
    time.sleep(1)
    driver.find_element_by_id("su").click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="1"]/h3/a').click()
    time.sleep(10)
    result = proxy.har
    # proxy.wait_for_traffic_to_stop(1,60)
    # 导出成har文件
    with open('proxytest.har', 'w') as outfile:
        json.dump(proxy.har, outfile)
    # 从抓取遍历
    for entry in result['log']['entries']:
        _url = entry['request']['url']

        if "getCurrAnd15dAnd24h" in _url:
            print(_url)
            # 抓取请求方法和请求参数
            _method = entry['request']['method']
            _queryString = entry['request']['queryString']
            _responseContent = entry['response']['content']
            _response = _responseContent['text']
            print(_method)
            print(_response)
            print(_queryString)

    # proxy.close()  # 关闭java子进程，解决地址被占用的问题
    server.stop()
    driver.quit()
def killjava():
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        # print('pid-%s,pname-%s' % (pid, p.name()))
        if 'java.exe' in p.name():
            cmd = 'taskkill /f /im java.exe'
            os.system(cmd)
def run():
    try:
        raise openBrown()
    except BaseException as e:
        print(e)
    finally:
        killjava()
run()


