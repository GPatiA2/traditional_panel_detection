import cv2
import numpy as np

class ImageLoader():

    def __init__(self) -> None:
        pass

    def load_image(self, image_path : str) -> np.array:

        return cv2.imread(image_path)

    def save_image(self, image_path : str, image : np.array) -> None:

        cv2.imwrite(image_path, image)
