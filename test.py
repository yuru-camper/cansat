import time
import cv2
import numpy as np
import PIL


image = cv2.imread("G:\\raspi_cansat\images\captured_40.jpg")
height = image.shape[0]
width = image.shape[1]
# image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
# image = image.transpose((2, 0, 1))
# image[2] = np.where((image[0] >= 115) & (image[0] <= 130), image[2], 0)
# image[2] = np.where(image[1] >= 150, image[2], 0)
# image[2] = np.where(image[2] >= 150, image[2], 0)
# image = image.transpose((1, 2, 0))
# image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)

image = cv2.cvtColor(image, cv2.COLOR_RGB2Lab)
# image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
image = image.transpose((2, 0, 1))

# image = image.transpose((1, 2, 0))
# image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)

cv2.imshow('window', image[1])
cv2.waitKey(0)
cv2.destroyAllWindows()
