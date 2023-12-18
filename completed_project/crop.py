import json
from PIL import Image
import numpy as np
import os


def crop():
    # 이미지 파일 경로
    # 현재 작업 디렉토리를 가져옵니다.
    CURRENT_DIR = os.getcwd()
    # static/images 폴더의 경로를 만듭니다.
    IMAGE_FOLDER = os.path.join(CURRENT_DIR, "static", "result")
    # 해당 디렉토리에 있는 모든 파일 목록을 가져옵니다.
    file_list = os.listdir(IMAGE_FOLDER)

    original_filename = None
    image_extention = None
    for filename in file_list:
        name_without_extension, extension = os.path.splitext(filename)
        if name_without_extension.lower() == "result":
            original_filename = filename
            image_extention = extension
            break

    # 이미지 파일 경로 획득
    IMAGE_PATH = os.path.join(IMAGE_FOLDER, original_filename)
    image = Image.open(IMAGE_PATH)

    # JSON 폴더 경로
    KEY_JSON_PATH = os.path.join(
        CURRENT_DIR, "static", "json", "original_keypoints.json"
    )
    # JSON 파일 열기
    with open(KEY_JSON_PATH) as json_file:
        data = json.load(json_file)

    # face_keypoints_2d 가져오기
    face_keypoints_2d = data["people"][0]["face_keypoints_2d"]

    # 크롭을 위한 특정 좌표 구하기
    left_x = face_keypoints_2d[3]
    left_y = face_keypoints_2d[4]
    chin_x = face_keypoints_2d[24]
    chin_y = face_keypoints_2d[25]
    right_x = face_keypoints_2d[45]
    right_y = face_keypoints_2d[46]

    # 얼굴 길이 및 크롭 이미지 길이 구하기
    face_width = right_x - left_x
    crop_width = face_width / 158 * 300
    crop_height = crop_width / 3 * 4

    # 크롭 이미지의 중앙 구하기
    crop_middle_x = (left_x + right_x) / 2
    crop_middle_y = (left_y + right_y) / 2

    # 크롭 이미지의 왼쪽 위 좌표 구하기
    crop_x = crop_middle_x - (crop_width / 2)
    crop_x = 0 if crop_x < 0 else crop_x
    crop_y = crop_middle_y - (crop_height / 2)
    crop_y = 0 if crop_y < 0 else crop_y

    # face keypoint들의 x, y 좌표값만 빼내는 과정
    n = 0
    indices = [3 * n + i for n in range(len(face_keypoints_2d) // 3) for i in (0, 1)]

    facekp = [face_keypoints_2d[i] for i in indices]
    # print("facekp:", facekp[0], facekp[1])

    # 크롭 이미지에 대응하는 키포인트들의 좌표값 생성
    cropkp = [x - crop_x if i % 2 == 0 else x - crop_y for i, x in enumerate(facekp)]
    # print("cropkp:", cropkp[0], cropkp[1])

    # json 폴더에 저장
    # JSON 파일로 저장할 경로와 파일명 지정
    CROP_JSON_PATH = os.path.join(CURRENT_DIR, "static", "json", "crop_keypoints.json")

    # 리스트를 JSON 형식으로 변환하여 파일로 저장
    with open(CROP_JSON_PATH, "w") as file:
        json.dump(cropkp, file)

    # 이미지 크롭 및 2_resize 폴더에 저장
    cropped_image = image.crop(
        (crop_x, crop_y, crop_x + crop_width, crop_y + crop_height)
    )

    # 저장할 이미지의 이름과 확장자를 설정
    cropped_filename = "crop" + image_extention
    CROP_FOLDER = os.path.join(CURRENT_DIR, "static", "crop")
    CROP_PATH = os.path.join(CROP_FOLDER, cropped_filename)
    cropped_image.save(CROP_PATH)

    return True


if __name__ == "__main__":
    result_bool = crop()
    print(result_bool)
