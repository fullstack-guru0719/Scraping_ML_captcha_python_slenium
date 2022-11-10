import cv2
import numpy as np
from matplotlib import pyplot as plt
import pytesseract

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

img = cv2.imread('images/captcha200.png', 0)
img = cv2.GaussianBlur(img, (5, 5), 0)
th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 7)
img = cv2.resize(th3, (200, 65))

plt.imshow(img,'gray')
plt.show()

text = pytesseract.image_to_string(img, config="-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz")
text = filter(text, dic)

print(text)