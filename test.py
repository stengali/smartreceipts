import io
import os
import base64
import time
import datefinder
from google.cloud import vision
from semantic.dates import DateService
from multiprocessing import Process
from nltk.tokenize import  sent_tokenize, word_tokenize
from nltk.corpus import stopwords
# Instantiates a client
vision_client = vision.Client()

def detect_text(image):
    texts = image.detect_text()
    string_with_dates =""
    for text in texts:
        string_with_dates += text.description
        break

    #print string_with_dates
    #string_with_dates = "DATE  15-08-2013 TIME 19:06:56"
    #string_with_dates1 ="Logos: Texts: ARVIND LIFESTYLE BRANDS LIMITED DIVISION MEGAMART #1, CG Chinnappa Naidu Layout 30th Main Road, Katriguppe, Bangalore 85 Ph 080-42924444 VAT/TIN 29900867473 29900867473 CST Cashier Code SARATH Machine Code BGGF4 Loyalty No Cust. Name Bill No: BS3IN0062986 DATE 15-08-2013 TIME 19:06:56 Retail Invoice Qty Sr. Item Description Net Value Discount MRP Levis/Jacket/6902653247006 2362.15 960 3199 2 Common /Support/8907002208989 1 6.12 6.12 Total Item Qty 3205.12 Gross Bill Value 960 Discount Amt 123.15 VAT Amt Change Due Write off 0.27 Net Bill Amount 132 Refund Amount VAT SUMMARY UAT% Base Amt Vat Amt 5.50 2239.00 123.15 6.12 0.00 0.00 Tender (s) 1 Cash Amount 2368 You have availed a FABULOUS SAVINGS of"
    print string_with_dates
    for word in word_tokenize(string_with_dates):
        for m in datefinder.find_dates(word,False,False,True,None):
            print "IMPORTANT"+word +"---"+str(m)

def detect_logos(image):
    logos = image.detect_logos()
    for logo in logos:
        print("LOGOS -----" +logo.description)
        break

def uploadImageToMemory():
    """Detects logos in the file."""
    vision_client = vision.Client()

    file_name = os.path.join(
        os.path.dirname(__file__),
        'IMG_2666.JPG')

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image1 = vision_client.image(content=content)
    return image1

print int(round(time.time() * 1000))
image = uploadImageToMemory()
p1 = Process(target=detect_logos(image))
p1.start()
p2 = Process(target=detect_text(image))
p2.start()
p1.join()
p2.join()
print int(round(time.time() * 1000))

