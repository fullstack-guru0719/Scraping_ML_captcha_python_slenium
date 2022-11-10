from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

from PIL import Image
import base64

import matplotlib.pyplot as plt



def screenshot(browser, element, index, filename='screenshot.png'):
    """docstring for screenshot"""
    elem = browser.find_element(By.ID, element)
    loc = elem.location
    size = elem.size
    isSaved = browser.get_screenshot_as_file(filename)
    # data = base64.b64decode(screenshot)
    img = Image.open(filename)

    # box = (left, upper, right, lower)
    left = loc['x']
    top = loc['y']
    width = size['width']
    height = size['height']
    box = (left, top, left+width, top+height)
    area = img.crop(box)

    # plt.imshow(area)
    # plt.show()

    area.save('images/captcha' + str(index) + '.png')
    

driver = webdriver.Chrome()
driver.get('https://agencyportal.irdai.gov.in/PublicAccess/LookUpPAN.aspx')

index = 0
while True:

    screenshot(driver, 'ctl00_ContentPlaceHolder1_imgcaptcha', index)

    driver.refresh()
    
    index += 1