import cv2
from pyzbar.pyzbar import decode

def decode_bar(im):
    try:
        decodedObj = decode(im)
        for obj in decodedObj:
            objdata = obj.data

        return objdata.decode("utf-8")
    except(Exception):
        return None

def findBarcode(source):

    im = cv2.imread(source)
    decoded = decode_bar(im)
    return decoded