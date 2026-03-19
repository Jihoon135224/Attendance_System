import qrcode
import csv
import os

# QR 코드 저장 폴더 생성
if not os.path.exists("qrcodes"):
    os.makedirs("qrcodes")

# users.csv에서 사용자 정보 읽기
with open("users.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader, None)  # 헤더 스킵

    for row in reader:
        if not row or len(row) < 2:
            continue  # 빈 줄이나 컬럼 2개 미만이면 스킵
        if row[0].strip() == "" or row[1].strip() == "":
            continue  # student_id나 name이 비어있으면 스킵

        student_id, name = row[0].strip(), row[1].strip()
        qr_data = f"{student_id},{name}"
        qr = qrcode.make(qr_data)

        # QR 코드 파일 저장
        qr.save(f"qrcodes/{student_id}.png")

print("✅ QR 코드 생성 완료!")
