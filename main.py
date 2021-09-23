import cv2 as cv
import numpy as np
import os
import win32gui, win32ui, win32con

from time import time

def window_capture():
  window_name = "Rocket League (64-bit, DX11, Cooked)"

  hwnd = win32gui.FindWindow(None, window_name)

  if (hwnd == 0):
    print("Window not found")
    return

  window_rect = win32gui.GetWindowRect(hwnd)
  # Cut out black borders
  w = window_rect[2] - window_rect[0]
  h = window_rect[3] - window_rect[1]

  # Cut out window borders
  border_pixels = 8
  titlebar_pixels = 30
  w = w - (border_pixels * 2)
  h = h - (border_pixels * 2) - titlebar_pixels

  # Get the window image data
  wDC = win32gui.GetWindowDC(hwnd)
  dcObj = win32ui.CreateDCFromHandle(wDC)
  cDC = dcObj.CreateCompatibleDC()
  dataBitMap = win32ui.CreateBitmap()
  dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
  cDC.SelectObject(dataBitMap)
  cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

  # Save screenshot
  # dataBitMap.SaveBitmapFile(cDC, 'test.bmp')

  signedIntsArray = dataBitMap.GetBitmapBits(True)
  img = np.fromstring(signedIntsArray, dtype='uint8')
  img.shape = (h, w, 4)

  # Free Resources
  dcObj.DeleteDC()
  cDC.DeleteDC()
  win32gui.ReleaseDC(hwnd, wDC)
  win32gui.DeleteObject(dataBitMap.GetHandle())

  # Drop the alpha channel
  img = img[...,:3]

  img = np.ascontiguousarray(img)

  return img

loop_time = time()

while(True):
  # screenshot = pg.screenshot() # ~20fps
  # screenshot = ImageGrab.grab() # ~20fps
  screenshot = window_capture() # ~35fps
  screenshot = np.array(screenshot)
  # screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

  cv.imshow('screenshot', screenshot)

  print('FPS {}'.format(1 / (time() - loop_time)))
  loop_time = time()

  if cv.waitKey(1) == ord('q'):
    cv.destroyAllWindows()
    break

window_capture()
print('Done')