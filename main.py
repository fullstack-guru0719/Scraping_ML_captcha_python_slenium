from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from PIL import Image
import base64
import numpy as np
from matplotlib import pyplot as plt
import pytesseract
import cv2

import csv

dic = {
    't' : '1'
}

def filter(txt, dic):
    txt = txt.replace(' ', '')
    res = ''
    for c in txt:
        if c in dic:
            res += dic[c]
            continue
        res += c
    return res

def get_captcha(browser, element, filename='screenshot.png'):
    elem = browser.find_element(By.ID, element)
    loc = elem.location
    size = elem.size
    isSaved = browser.get_screenshot_as_file(filename)
    img = Image.open(filename)
    left = loc['x']
    top = loc['y']
    width = size['width']
    height = size['height']
    # box = (left, top, left+width, top+height)
    # area = img.crop(box)
    return filename, left, top, width, height
    

def get_captcha_text(driver):
    img_name, left, top, width, height = get_captcha(driver, 'ctl00_ContentPlaceHolder1_imgcaptcha')
    captcha_img = cv2.imread(img_name, 0)
    captcha_img = captcha_img[top:top+height, left:left+width]
    img = cv2.GaussianBlur(captcha_img, (5, 5), 0)
    th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 7)
    img = cv2.resize(th3, (200, 65))
    # plt.imshow(img,'gray')
    # plt.show()
    text = pytesseract.image_to_string(img, config="-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz")
    text = filter(text, dic)

    print(text)

    return text


if __name__ == '__main__':

    f = open('output.csv', 'w')
    writer = csv.writer(f)

    header_row = ['PAN', 'Aadhaar', 'Agent Name', 'Date of Birth', 'Insurer Type', 'Insurer', 'Agency Code', 'Date of Appointment', 'Status of agency', 'Status Change Date', 'License No. If any previously held']

    writer.writerow(header_row)

    pan_addresses = ["BEZPD4719P", "CQVPA1344L"]

    driver = webdriver.Chrome()
    
    for pan_address in pan_addresses:
        correct = False
        while not correct:
            driver.get('https://agencyportal.irdai.gov.in/PublicAccess/LookUpPAN.aspx')
            captcha_txt = get_captcha_text(driver)
            address_field = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_PAN_Details")
            address_field.send_keys(pan_address)
        
            captcha_field = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtcaptcha")
            captcha_field.send_keys(captcha_txt)

            submit_button = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$btn_lookup")
            submit_button.click()
            correct = True        
            if len(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_labelerror").text) > 1:
                correct = False

        
        if len(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_lblError").text) > 1:
            print(pan_address, " : No records found")
            writer.writerow([pan_address, '', '', '', '', '', '', '', '', ''])
        else:
            print("Records found")
            table = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_gdvPan")
            trs = table.find_elements(By.CSS_SELECTOR, 'tr')
            header_tr = trs[0]
            ths = header_tr.find_elements(By.CSS_SELECTOR, 'th')
            data = []
            header = []
            for th in ths:
                header.append(th.text)
            data.append(header)
            # writer.writerow(header)
            for tr in trs[1:]:
                tds = tr.find_elements(By.CSS_SELECTOR, 'td')
                row = []
                for td in tds:
                    row.append(td.text)
                data.append(row)
                print('Insurer Type', row[4])
                print('Status of agency', row[8])
                writer.writerow(row)
            print(pan_address, ' : ', data)
    f.close()


    


    while True:
        pass



