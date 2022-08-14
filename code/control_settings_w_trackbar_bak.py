import cv2

Window_name = 'Control Camera'

def changeBrightness(x):
    brightness = cv2.getTrackbarPos('brightness',Window_name)
    brightness = (brightness - 0) * 255 / (255 - 0)
    print("Brightness now is:", brightness)
    cap.set(10,brightness)

def changeContrast(x):
    contrast = cv2.getTrackbarPos('contrast',Window_name)
    contrast = (contrast - 0) * 255 / (255 - 0)
    print("Contrast now is:", contrast)
    cap.set(11,contrast)

def changeSaturation(x):
    saturation = cv2.getTrackbarPos('saturation',Window_name)
    saturation = (saturation - 0) * 255 / (255 - 0)
    print("Saturation now is:", saturation)
    cap.set(12,saturation)

def changeGain(x):
    gain = cv2.getTrackbarPos('gain',Window_name)
    gain = (gain - 0) * 255 / (255 - 0)
    print("Gain now is:", gain)
    cap.set(14,gain)

def changeExposure(x):
    exposure = cv2.getTrackbarPos('exposure',Window_name)
    exposure = (exposure - 0) * 2047 / (2047 - 0)
    print("Exposure now is:", exposure)
    cap.set(15,exposure)

def changeSharpness(x):
    sharpness = cv2.getTrackbarPos('sharpness',Window_name)
    sharpness = (sharpness - 0) * 255 / (255 - 0)
    print("Sharpness now is:", sharpness)
    cap.set(20,sharpness)

def changedWhiteBalanceTemperature(self,value):
    white_balance_temperature = cv2.getTrackbarPos('white_balance_temperature',Window_name)
    white_balance_temperature = (value - 0) * 6500 / (6500 - 0)
    print("White Balance Temperature now is:", focus)
    self.capture.set(45, white_balance_temperature)

def changeFocus(x):
    focus = cv2.getTrackbarPos('focus',Window_name)
    focus = (focus - 0) * 250 / (250 - 0)
    print("Focus now is:", focus)
    cap.set(28,focus)

def changeZoom(x):
    zoom = cv2.getTrackbarPos('zoom',Window_name)
    zoom = (zoom - 0) * 500 / (500 - 0)
    print("Zoom now is:", zoom)
    cap.set(27,zoom)

cv2.namedWindow(Window_name)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_SETTINGS, 0)
cap.set(3,640)
cap.set(4,480)
print("FRAME_WIDTH", cap.get(3))
print("FRAME_HEIGHT", cap.get(4))
cap.set(5,30.0)
print("FPS", cap.get(5))
print("BRIGHTNESS", cap.get(10))
print("CONTRAST", cap.get(11))
print("SATURATION", cap.get(12))
print("GAIN", cap.get(14))
print("EXPOSURE", cap.get(15))
print("SHARPNESS", cap.get(20))
print("FOCUS", cap.get(28))
print("ZOOM", cap.get(27))
# create trackbars for color change
# get current brightness and contrast values
brightness = int(round(cap.get(10) * 255))
contrast = int(round(cap.get(11) * 255))
saturation = int(round(cap.get(12) * 255))
gain = int(round(cap.get(14) * 255))
exposure = int(round(cap.get(15) * 2047))
sharpness = int(round(cap.get(20) * 255))
wbtemperature = int(round(cap.get(20) * 6500))
focus = int(round(cap.get(28) * 250))
zoom = int(round(cap.get(27) * 500))
cv2.createTrackbar('Brightness',Window_name,brightness,128,changeBrightness)
cv2.createTrackbar('Contrast',Window_name,contrast,128,changeContrast)
cv2.createTrackbar('Saturation',Window_name,saturation,128,changeSaturation)
cv2.createTrackbar('Gain',Window_name,gain,255,changeGain)
cv2.createTrackbar('Exposure',Window_name,exposure,2047,changeExposure)
cv2.createTrackbar('Sharpness',Window_name,sharpness,255,changeSharpness)
cv2.createTrackbar('WB temperature',Window_name,wbtemperature,6500,changeSharpness)
cv2.createTrackbar('Focus',Window_name,focus,250,changeFocus)
cv2.createTrackbar('Zoom',Window_name,zoom,500,changeZoom)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # if the frame was not ret, then we have reached the end
    # of the stream
    if not ret:
        break

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # # Display the resulting frame
    # cv2.imshow(Window_name,gray)
    cv2.namedWindow(Window_name)
    cv2.imshow(Window_name,frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyWindows(Window_name)