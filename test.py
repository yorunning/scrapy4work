# -*-coding:utf8-*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import re
import asyncio
import aiomysql

'''
opt = webdriver.ChromeOptions()
opt.headless = False
# opt.add_argument('--headless')

driver = webdriver.Chrome(options=opt)

cookie_str = 'BIDUPSID=FA6C59C530F639429AE093A17D93A4D5; PSTM=1516263117; BD_UPN=123353; __cfduid=deb5c89b708a1252563e76112979ebde71525602518; BAIDUID=4E7D7C29CE939B4E56614804235CA7A6:FG=1; BDUSS=XAxY2p5NGF2dXN1bklxelRoaVlnaGhGYmRwajNXTjQwMnVZYTNUSUUxcy1sNE5iQVFBQUFBJCQAAAAAAAAAAAEAAACaWKpRyLvJ2VY1ODcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD4KXFs-ClxbN; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; BD_CK_SAM=1; PSINO=2; locale=zh; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_645EC=d806gHFxPqRJx%2FQkagBXq2mHZBHdvZbaPqfK8FcC76UTDqfaO8FGSCXTBZtsJQv2TQ87; BD_HOME=1; H_PS_PSSID=1461_26964_21082_26925_22072; sug=3; sugstore=1; ORIGIN=2; bdime=0'

driver.get('https://www.baidu.com')

for line in cookie_str.split(';'):
    name=line.split('=')[0].strip()
    value=line.split('=')[1]
    driver.add_cookie({'name': name, 'value': value})

# driver.add_cookie({i.split("=")[0]:i.split("=")[1] for i in cookie_str.split(";")})

driver.get('https://www.baidu.com')

time.sleep(3)



# input=driver.find_element_by_id('kw')
# input.send_keys('python')
# input.send_keys(Keys.ENTER)
#
# wait=WebDriverWait(driver,10)
# wait.until(EC.presence_of_element_located((By.ID,'content_left')))
#
# print(driver.current_url)
# print(driver.get_cookies())
# print(driver.page_source)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 's-more-bar')))

button = driver.find_element_by_xpath('//div[@class="s-more-bar"]')

button.click()

driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')

time.sleep(3)


print(driver.page_source)

'''

loop = asyncio.get_event_loop()


async def save():
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='car990226',
        db='yorunw',
        charset='utf8',
        loop=loop
    )

    sql = "insert into test(title) values('123123')"

    async with await conn.cursor() as cursor:
        await cursor.execute(sql)
        await conn.commit()

    conn.close()


loop.run_until_complete(save())



[print(f'\'{l}\'') for l in'\u602a\u6211\u773c\u778e\n\u7535\u89c6\u5267\u770b\u591a\u4e86\n\u9b54\u6014\u4e86\u5427\n\u4e0d\u770b\u770b\u81ea\u5df1\u4ec0\u4e48\u6837\n\u7b97\u4e86\n\u61d2\u5f97\u8bf4\u810f\u5b57'.split('\n')]

i=dict()