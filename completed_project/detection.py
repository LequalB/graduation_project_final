import os
import json


class Detection:
    def __init__(self):
        self.faceData = None
        self.bodyData = None

    def set_face_data(self, data):
        self.faceData = data

    def set_body_data(self, data):
        self.bodyData = data

    def shoulder_check(self):
        if (
            self.bodyData[2 * 3] == 0
            or self.bodyData[0 * 3] == 0
            or self.bodyData[5 * 3] == 0
            or self.bodyData[1 * 3] == 0
        ):
            print("어깨를 감지하지 못했습니다.")
            return 1  # 비정상
        X = (self.bodyData[1 * 3] - self.bodyData[2 * 3]) / (
            self.bodyData[5 * 3] - self.bodyData[1 * 3]
        )  # 어깨 가로 비율
        Y = (self.bodyData[2 * 3 + 1] - self.bodyData[0 * 3 + 1]) / (
            self.bodyData[5 * 3 + 1] - self.bodyData[0 * 3 + 1]
        )  # 어깨 세로 비율

        if X > 1.2 or X < 0.9 or Y > 1.2 or Y < 0.9:
            print("어깨가 기울어져 있습니다.")
            return 1  # 비정상
        return 0  # 정상

    def eyebrow_check(self):
        for i in range(17, 27):
            if self.faceData[i * 3] == 0:
                print(i)
                print("눈썹이 보이지 않습니다.")
                return 1  # 비정상
        return 0  # 정상

    def eye_check(self):
        for i in range(37, 48):
            if self.faceData[i * 3] == 0:
                print(i)
                print("눈을 감지하지 못했습니다.")
                return 1
        if self.faceData[68 * 3] == 0 or self.faceData[69 * 3] == 0:
            print("눈동자를 감지하지 못했습니다.")
            return 1

        L1 = (self.faceData[41 * 3 + 1] - self.faceData[37 * 3 + 1]) / (
            self.faceData[38 * 3] - self.faceData[37 * 3]
        )  # 왼쪽 눈 세로 가로 비율
        R1 = (self.faceData[47 * 3 + 1] - self.faceData[43 * 3 + 1]) / (
            self.faceData[44 * 3] - self.faceData[43 * 3]
        )  # 오른쪽 눈 세로 가로 비율

        L2 = (self.faceData[68 * 3] - self.faceData[36 * 3]) / (
            self.faceData[39 * 3] - self.faceData[68 * 3]
        )  # 왼 눈동자 좌 우 비율 비교
        R2 = (self.faceData[69 * 3] - self.faceData[42 * 3]) / (
            self.faceData[45 * 3] - self.faceData[69 * 3]
        )  # 오른 눈동자 좌 우 비율 비교

        if L1 < 0.6 or R1 < 0.6:
            print("눈을 제대로 뜨지 않았습니다.")
            return 1
        if L2 < 0.8 or L2 > 1.1 or R2 < 0.8 or R2 > 1.1:
            print("고개가 정면이 아니거나 정면을 보고 있지 않습니다.")
            # return 1
        return 0  # 정상

    def mouth_check(self):
        for i in range(60, 68):
            if self.faceData[i * 3] == 0:
                print(i)
                print("입을 감지 하지 못했습니다.")
                return 1
        T1 = (self.faceData[66 * 3 + 1] - self.faceData[62 * 3 + 1]) / (
            self.faceData[64 * 3] - self.faceData[60 * 3]
        )  # 입 벌림 가로 세로 비율
        T2 = self.faceData[67 * 3 + 1] / self.faceData[61 * 3 + 1]  # 입 왼쪽 세로 비율
        T3 = self.faceData[65 * 3 + 1] / self.faceData[63 * 3 + 1]  # 입 오른쪽 세로 비율

        D1 = self.faceData[61 * 3 + 1] / self.faceData[63 * 3 + 1]  # 윗입술 좌우 세로 비율
        D2 = (self.faceData[63 * 3] - self.faceData[67 * 3]) / (
            self.faceData[65 * 3] - self.faceData[61 * 3]
        )  # 입술 좌우 위아래 교차 가로 비율
        D3 = self.faceData[64 * 3 + 1] / self.faceData[60 * 3 + 1]  # 입 좌우 세로 비율

        if T1 > 0.05 or T2 > 1.05 or T3 > 1.05:
            print("입이 열려 있습니다.")
            return 1
        if D1 < 0.95 or D1 > 1.05 or D2 < 0.95 or D2 > 1.05 or D3 < 0.95 or D3 > 1.05:
            print("입이 비뚤어져 있습니다.")
            # return 1  # 비정상
        return 0  # 정상

    def symmetry_check(self):
        if (
            self.bodyData[0 * 3] == 0
            or self.bodyData[14 * 3] == 0
            or self.bodyData[15 * 3] == 0
        ):
            print("얼굴을 인식하지 못했습니다.")
            return 1  # 비정상
        X = (self.bodyData[15 * 3] - self.bodyData[0 * 3]) / (
            self.bodyData[0 * 3] - self.bodyData[14 * 3]
        )  # 좌우 눈과 코 가로 비율
        Y = (self.bodyData[0 * 3 + 1] - self.bodyData[14 * 3 + 1]) / (
            self.bodyData[0 * 3 + 1] - self.bodyData[15 * 3 + 1]
        )  # 좌우 눈과 코 세로 비율

        if X < 0.7 or X > 1.3 or Y < 0.85 or Y > 1.15:
            print("고개가 올바르지 않습니다.")
            return 1
        return 0  # 정상


def run_openpose():
    command = "build\\x64\\Release\\OpenPoseDemo.exe --image_dir static\\upload --face --write_json static\\json\\ --model_pose COCO"
    result = os.system(command)
    person = Detection()

    # 불리언 값 반환
    result_boolean = True
    # 숫자 list 반환
    fail_list = []

    # 실패라면 0, 성공이라면 1
    check = 1

    if result == 0:
        print("결과값을 불러오는데 성공하였습니다.")
    else:
        print("결과값을 불러오는데 실패하였습니다.")
        fail_list.append(6)
        check = 0
        return result_boolean, fail_list

    with open("static\\json\\original_keypoints.json") as file:
        data = json.load(file)
        people = data["people"]
        if people:
            person.set_face_data(people[0]["face_keypoints_2d"])
            person.set_body_data(people[0]["pose_keypoints_2d"])

    if check != 0:
        if person.eyebrow_check():
            result_boolean = False
            fail_list.append(1)
            check = 0
        if person.shoulder_check():
            result_boolean = False
            fail_list.append(2)
            check = 0
        if person.symmetry_check():
            result_boolean = False
            fail_list.append(3)
            check = 0
        if person.eye_check():
            result_boolean = False
            fail_list.append(4)
            check = 0
        if person.mouth_check():
            result_boolean = False
            fail_list.append(5)
            check = 0
    print("정상적으로 종료되었습니다.")

    return result_boolean, fail_list


if __name__ == "__main__":
    result_bool, fail_list = run_openpose()
    print(f"Result Bool: {result_bool}")
    print(f"Result Num: {fail_list}")
