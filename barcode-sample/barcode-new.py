import cv2
from pyzbar.pyzbar import decode

def decode_barcode(im) :
    # Find barcodes and QR codes
    decodedObjects = decode(im)
    # Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data)

    return decodedObjects

# Display barcode and QR code location
def display(im, decodedObjects):
    # Loop over all decoded objects
    for decodedObject in decodedObjects:
        print('decodedObject.Type : ', decodedObject.type)
        print('decodedObject.Data : ', decodedObject.data)
        rect = decodedObject.rect
        print ("left: " + str(rect.left))
        print ("top: " + str(rect.top))
        print ("width: " + str(rect.width))
        print ("height: " + str(rect.height))
        startX = rect.left
        startY = rect.top
        endX = (rect.left + rect.width)
        endY = (rect.top + rect.height)
        cv2.rectangle(im, (startX, startY), (endX, endY), (0, 255, 0), 3)
    return im

# Main
if __name__ == '__main__':
    # Read image
    im = cv2.imread("test2.png")
    decodedObjects = decode_barcode(im)
    im = display(im, decodedObjects)
    cv2.imshow("Results", im)
    cv2.waitKey(0)