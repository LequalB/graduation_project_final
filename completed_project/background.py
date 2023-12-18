import json
from PIL import Image
import numpy as np
import os
import sys


def addBg():
    # 이미지 파일 경로
    # 현재 작업 디렉토리를 가져옵니다.
    CURRENT_DIR = os.getcwd()
    # static/images 폴더의 경로를 만듭니다.
    IMAGE_FOLDER = os.path.join(CURRENT_DIR, "static", "crop")
    # 해당 디렉토리에 있는 모든 파일 목록을 가져옵니다.
    file_list = os.listdir(IMAGE_FOLDER)

    # 이미지 파일 경로 획득
    IMAGE_PATH = os.path.join(IMAGE_FOLDER, "crop.png")
    image = Image.open(IMAGE_PATH)

    # stdin으로부터 데이터 읽기
    data = sys.stdin.read()
    r, g, b = map(int, data.split())

    background_color = (r, g, b, 255)

    newimg = Image.new("RGBA", image.size, background_color)

    newimg.paste(image, (0, 0), image)

    newimg.convert("RGB").save(
        "C:\\Users\\xodbs\\Documents\\judge\\static\\download\\download.jpg"
    )


if __name__ == "__main__":
    addBg()
