import cv2
from numpy import array
from matplotlib import pyplot as plt


def write_image_to_bytes(image_path: str) -> bytes:

    with open(image_path, "rb") as image:
        image_to_bytes = image.read()

    return image_to_bytes


def read_image_from_bytes(image_bytes: bytes) -> None:
    image = cv2.imdecode(array(bytearray(image_bytes)), cv2.IMREAD_COLOR)
    image_2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    plt.imshow(image_2)
    plt.xticks([]), plt.yticks([])
    plt.show()
