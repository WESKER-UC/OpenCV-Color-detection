import cv2 as cv
import util as u
from PIL import Image


def Detect(color):
    inVid = cv.VideoCapture(1)

    while True:
        ret, frame = inVid.read()
        if not ret:
            continue
        smootherFrame=cv.GaussianBlur(frame, (5, 5), 0)
        hsvframe = cv.cvtColor(smootherFrame, cv.COLOR_BGR2HSV)
        ll, ul = u.get_limits(color)

        mask = cv.inRange(hsvframe, ll, ul)

        colorMask = Image.fromarray(mask)
        bBOX = colorMask.getbbox()

        if bBOX is not None:
            x1, y1, x2, y2 = bBOX
            frame = cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

        cv.imshow("frame", frame)
        
        if cv.waitKey(30) & 0xFF == ord('q'):
            break

    inVid.release()
    cv.destroyAllWindows()

def DetectMulti(*colors):
    inVid = cv.VideoCapture(1)

    while True:
        ret, frame = inVid.read()
        if not ret:
            continue

        smootherFrame = cv.GaussianBlur(frame, (5, 5), 0)
        hsvframe = cv.cvtColor(smootherFrame, cv.COLOR_BGR2HSV)

        bboxes = []

        for idx, color in enumerate(colors):
            ll, ul = u.get_limits(color)
            mask = cv.inRange(hsvframe, ll, ul)

            mask_img = Image.fromarray(mask)
            bbox = mask_img.getbbox()

            if bbox is not None:
                x1, y1, x2, y2 = bbox
                frame = cv.rectangle(frame, (x1, y1), (x2, y2), color, 3)

        cv.imshow("Detected Colors", frame)

        if cv.waitKey(30) & 0xFF == ord('q'):
            break

    inVid.release()
    cv.destroyAllWindows()


colList = [
    [0, 255, 0],     # Green
    [0, 0, 255],     # Red
    [0, 255, 255],   # Yellow
    [255, 0, 0],     # Blue
    [255, 255, 0],   # Cyan
    [255, 0, 255],   # Magenta
    [0, 165, 255],   # Orange
    [203, 192, 255], # Pink
    
          
    ]
print("Enter Number of Color to detect:",end="")
NumCol=int(input())
if(NumCol==1):
    print("Choose the color of the object You want to detect :")
    print("1.Green\n2.Red\n3.Yellow\n4.Blue\n5.Cyan\n6.Magenta\n7.Orange\n8.Pink")
    ch = int(input("Choice: "))


    
    color = colList[ch - 1]

    Detect(color)


else:
    print("1.Green\n2.Red\n3.Yellow\n4.Blue\n5.Cyan\n6.Magenta\n7.Orange\n8.Pink")
    print("Enter the color choices (e.g., 1,3,4 for Green, Yellow, Blue):",end="")
    indices = input().split(',')
    
    selected_colors = []
    for i in indices:
        try:
            selected_colors.append(colList[int(i)-1])
        except:
            print(f"Invalid index: {i}")
    
    if selected_colors:
        DetectMulti(*selected_colors)
    else:
        print("No valid colors selected.")
