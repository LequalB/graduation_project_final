from flask import Flask, request, render_template, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
import shutil
import subprocess

# 웹 서버 역할 Flask APP 생성
app = Flask(__name__)

# 업로드된 이미지를 저장할 디렉토리
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "upload")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# 업로드된 파일의 확장자를 검사하기 위한 함수
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# 라우팅 설정 - url을 통한 접속 > 응답을 담당
# 메인 페이지
@app.route("/")
def index():
    return render_template("index.html")


# index.html에서 업로드 담당
@app.route("/submit_upload", methods=["POST"])
def submit_upload():
    # 사용될 폴더들의 경로
    JSON_FOLDER = os.path.join(app.root_path, "static", "json")
    CROP_FOLDER = os.path.join(app.root_path, "static", "crop")
    RESULT_FOLDER = os.path.join(app.root_path, "static", "result")
    DOWNLOAD_FOLDER = os.path.join(app.root_path, "static", "download")

    # 새 이미지를 받기 위해 폴더 삭제 및 재생성
    shutil.rmtree(UPLOAD_FOLDER)
    shutil.rmtree(JSON_FOLDER)
    shutil.rmtree(CROP_FOLDER)
    shutil.rmtree(RESULT_FOLDER)
    shutil.rmtree(DOWNLOAD_FOLDER)
    os.makedirs(UPLOAD_FOLDER)
    os.makedirs(JSON_FOLDER)
    os.makedirs(CROP_FOLDER)
    os.makedirs(RESULT_FOLDER)
    os.makedirs(DOWNLOAD_FOLDER)

    # 파일 유효성 검사
    # 파일 자체가 없는데 업로드 버튼을 눌렀을 경우
    if "file" not in request.files:
        return redirect(url_for("index"))  # 'index' 함수로 리디렉트

    # 파일이 있을 경우
    file = request.files["file"]
    if file.filename == "":
        return redirect(url_for("index"))  # 'index' 함수로 리디렉트

    if file and allowed_file(file.filename):
        # 파일 이름을 'original.확장자'로 변경
        # 파일의 원래 확장자를 추출하여 사용
        filename = "original." + file.filename.split(".")[-1]
        # 파일을 저장할 경로
        UPLOADED_FILE = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(UPLOADED_FILE)

        # detect.py를 호출하여 결과 얻기
        detection_result = subprocess.run(
            ["python", "detection.py"], capture_output=True, text=True, check=True
        )

        detection_output = detection_result.stdout.strip().split("\n")
        detection_result_boolean = detection_output[-2].split(": ")[-1]
        detection_result_number = detection_output[-1].split(": ")[-1]

        print(f"Detection Result Boolean: {detection_result_boolean}")
        print(f"Detection Result Number: {detection_result_number}")

        # detection_result_boolean 값에 따라서 리디렉션
        if detection_result_boolean == "False":
            return render_template("fail.html", result_number=detection_result_number)
        else:
            return render_template("success.html")

    else:
        return redirect(url_for("index"))


# success.html에서 업로드 담당
@app.route("/submit_remove", methods=["POST"])
def submit_remove():
    remove_result = subprocess.run(
        ["python", "DIS\\IS-Net\\Inference.py"],
        capture_output=True,
        text=True,
        check=True,
    )

    crop_result = subprocess.run(
        ["python", "crop.py"], capture_output=True, text=True, check=True
    )
    crop_output = crop_result.stdout.strip()
    print(f"Crop Result Boolean: {crop_output}")

    return render_template("result.html")


@app.route("/download", methods=["POST"])
def download():
    r = int(request.form["number1"])
    g = int(request.form["number2"])
    b = int(request.form["number3"])

    data = f"{r} {g} {b}"

    background_result = subprocess.run(
        ["python", "background.py"],
        input=data,
        capture_output=True,
        text=True,
        check=True,
    )

    return send_file("static\\download\\download.jpg", as_attachment=True)


# Flask 앱 가동(run)
if __name__ == "__main__":
    app.run(debug=True)
