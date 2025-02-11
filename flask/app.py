# 기존 환경 삭제
# conda env remove --name facenet
# 환경 생성
# conda create --name facenet python=3.8.20
# 환경 활성화
# conda activate facenet
# 콘다 패키지 일괄 설치
# conda install --file conda_requirements.txt
# pip 패키지 일괄 설치
# pip install -r pip_requirements.txt

import os
import cv2
import numpy as np
import torch
import logging
from facenet_pytorch import InceptionResnetV1, MTCNN
from scipy.spatial.distance import cosine
from PIL import ImageFont, ImageDraw, Image
import time
from flask import Flask, render_template, Response, request
import DBManager as db
import json
from datetime import datetime
import CheckOut

# 로그 설정
log_file = "dev.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

app = Flask(__name__)

# 전역 변수 설정
flag = False          # 새 얼굴 인식 여부 플래그
tmp_sno = ""
tmp_sname = ""
new_face = [None, None]  # [sno, embedding]

# 비동기 캡쳐용 변수들
global_latest_frame = None
global_latest_face_crop = None
global_latest_embedding = None

with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

DEV_MODE = config.get("DEV_MODE", True)

# 디바이스 설정
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 모델 및 얼굴 검출기 로드
try:
    model = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    # 보통 keep_all=True 면 여러 얼굴을 다 검출. 원하는 로직에 따라 조정
    mtcnn = MTCNN(
        keep_all=True,
        post_process=False,
        min_face_size=config.get("MTCNN", {}).get("min_face_size", 60),
        thresholds=config.get("MTCNN", {}).get("thresholds", [0.6, 0.7, 0.7]),
        device=device
    )
    embedder = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    logging.info("모델과 MTCNN 초기화 완료")
except Exception as e:
    logging.error(f"모델 초기화 실패: {e}")

# 임시 저장소 및 시간 설정
temp_storage = {}
temp_storage_duration = 60  # 초 단위

database_cache = None  # 캐싱된 데이터베이스

def load_database(refresh=False):
    """
    DB에서 사용자 정보를 로드하여 캐싱
    """
    global database_cache
    try:
        if database_cache is not None and not refresh:
            logging.info("캐싱된 데이터베이스 사용")
            return database_cache

        logging.info("DB에서 사용자 정보를 로드합니다")
        dbms = db.DBManager()
        dbflag = dbms.DBOpen(host="192.168.0.231", dbname="facenutdb", id="bteam", pw="ezen")
        if not dbflag:
            logging.error("데이터베이스 연결 오류")
            return {}
        sql = "SELECT embedding.sno, sname, embedding.embedding FROM studentinfo, embedding WHERE studentinfo.sno = embedding.sno"
        dbms.OpenQuery(sql)
        if dbms.GetTotal() > 0:
            database_cache = dbms.GetDf()  # 데이터 프레임 형태로 캐싱
        dbms.CloseQuery()
        dbms.DBClose()
        if database_cache is not None:
            logging.info(f"DB 로드 완료. 레코드 수: {len(database_cache)}")
        else:
            logging.info("DB 로드 결과가 없습니다.")
        return database_cache
    except Exception as e:
        logging.error(f"load_database() 예외: {e}")
        return {}

def name_search(phone):
    """
    전화번호로 사용자 sno, sname 조회
    """
    try:
        logging.info(f"전화번호로 사용자 검색: {phone}")
        dbms = db.DBManager()
        dbflag = dbms.DBOpen(host="192.168.0.231", dbname="facenutdb", id="bteam", pw="ezen")
        if not dbflag:
            logging.error("데이터베이스 연결 오류")
            return None, None

        sql = f"SELECT sno, sname FROM studentinfo WHERE phone = '{phone}'"
        dbms.OpenQuery(sql)
        if dbms.GetTotal() > 0:
            sno = dbms.GetValue(0, 'sno')
            sname = dbms.GetValue(0, 'sname')
        else:
            sno, sname = None, None
        dbms.CloseQuery()
        dbms.DBClose()

        if sno is not None:
            new_face[0] = sno  # 미리 할당
            logging.info(f"검색 결과: {sname} ({sno})")
        else:
            logging.info(f"검색 결과 없음 (phone={phone})")
        return sno, sname
    except Exception as e:
        logging.error(f"name_search() 예외: {e}")
        return None, None

@app.route("/search")
def search_ok():
    """
    전화번호로 사용자 검색 후 얼굴 임베딩 저장 로직
    """
    try:
        phone = request.args.get("phone")
        sno, sname = name_search(phone)
        logging.info(f"search_ok() => sno:{sno}, sname:{sname}, newface:{type(new_face[1])}")

        # new_face가 존재하면 DB에 저장
        if new_face and new_face[1] is not None:
            save_database(new_face)
            logging.info(f"새 얼굴을 저장합니다")
            load_database(refresh=True)
            logging.info(f"db를 새로 로드합니다")
        return render_template('facerecog.html', name=sname, no=sno)
    except Exception as e:
        logging.error(f"/search 엔드포인트 예외: {e}")
        return "에러 발생", 500

def recognize_face(database, threshold=0.6):
    """
    글로벌에 저장된 global_latest_embedding과 DB 임베딩을 비교하여
    threshold 이내면 사용자 sno, sname 반환
    """
    try:
        global flag
        # DB가 비어있으면 None
        if database is None or len(database) == 0:
            logging.warning("데이터베이스가 비어있습니다")
            return None

        # 이미 flag가 True라면 인식된 상태로 간주
        if flag:
            logging.debug("이미 얼굴이 인식되어 flag=True 입니다.")
            return None

        embedding = global_latest_embedding
        if embedding is None:
            return None

        min_distance = float('inf')
        match_name, match_no = None, None

        logging.info("DB와 얼굴 임베딩 비교 시작")
        for i in range(len(database)):
            item = database.iloc[i]
            sno, sname, db_embedding = item['sno'], item['sname'], item['embedding']
            # 문자열을 numpy 배열로 변환
            db_embedding = np.array(list(map(float, db_embedding.split(','))))
            #distance = cosine(embedding.cpu().numpy().flatten(), db_embedding)
            distance = cosine(embedding.cpu().detach().numpy().flatten(), db_embedding)
            if distance < min_distance:
                min_distance = distance
                match_name = sname
                match_no   = sno

        if min_distance < threshold:
            flag = True
            logging.info(f"인식 성공: {match_name} ({match_no}), 거리: {min_distance:.3f}")
            return (match_no, match_name)
        else:
            logging.info(f"일치하는 얼굴 없음, 최소 거리: {min_distance:.3f}")
            return None
    except Exception as e:
        logging.error(f"recognize_face() 예외: {e}")
        return None

def save_database(new_face):
    """
    새 얼굴 임베딩을 DB에 저장
    """
    global flag
    try:
        logging.info("새로운 얼굴 DB에 저장 시작")
        embedding = new_face[1]
        if embedding is None:
            logging.error("임베딩 값이 없습니다")
            return
        # 텐서일 경우 넘파이 변환
        if torch.is_tensor(embedding):
            embedding = embedding.cpu().detach().numpy().flatten()

        embedding_str = ','.join(map(str, embedding))
        sno = new_face[0]

        dbms = db.DBManager()
        dbflag = dbms.DBOpen(host="192.168.0.231", dbname="facenutdb", id="bteam", pw="ezen")
        if not dbflag:
            logging.error("데이터베이스 연결 오류")
            return

        sql = f'INSERT INTO embedding (embedding, sno) VALUES ("{embedding_str}", {sno})'
        dbms.RunSQL(sql)
        dbms.CloseQuery()
        dbms.DBClose()

        flag = False
        new_face[:] = [None, None]  # 리스트 초기화
        logging.info(f"새로운 얼굴 저장 완료: {sno}")
    except Exception as e:
        logging.error(f"save_database() 예외: {e}")

def is_recently_detected(temp_storage, threshold=0.6):
    """
    temp_storage에 유사 임베딩이 최근에 기록되어 있으면 True
    """
    try:
        current_time = time.time()
        emb = global_latest_embedding
        if emb is None:
            return False
        
        # 텐서일 경우 넘파이 변환
        if torch.is_tensor(emb):
            emb = emb.cpu().detach().numpy().flatten()

        for temp_embedding, timestamp in list(temp_storage.items()):
            distance = cosine(emb, temp_embedding)
            if distance < threshold:
                if current_time - timestamp < temp_storage_duration:
                    return True
                else:
                    del temp_storage[temp_embedding]
        return False
    except Exception as e:
        logging.error(f"is_recently_detected() 예외: {e}")
        return False

def draw_text(img, text, position, font_path, font_size=20, color=(255,255,255)):
    """
    PIL을 이용해 한글 텍스트를 OpenCV 이미지에 오버레이
    """
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    try:
        font = ImageFont.truetype(font_path, font_size, encoding="utf-8")
    except IOError:
        logging.warning("폰트 파일을 찾지 못해 기본 폰트 사용")
        font = ImageFont.load_default()
    draw.text(position, text, font=font, fill=color)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def visualize_embeddings(frame, embeddings):
    """
    임베딩 값을 히트맵 형태로 시각화하여 원본 프레임에 오버레이
    """
    if embeddings is None:
        return frame

    # 텐서 -> 넘파이
    if torch.is_tensor(embeddings):
        embeddings = embeddings.cpu().detach().numpy()
    # 2D 이상이면 0번째만 사용 (ex. shape=(1,512))
    if embeddings.ndim > 1:
        emb_vis = embeddings[0][:128]
    else:
        emb_vis = embeddings[:128]

    normalized = (emb_vis - emb_vis.min()) / (emb_vis.max() - emb_vis.min() + 1e-6)
    heatmap = (normalized * 255).astype(np.uint8)
    heatmap = heatmap.reshape(16, 8)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    heatmap = cv2.resize(heatmap, (200, 400))

    overlay_area = frame[10:410, 10:210]
    blended = cv2.addWeighted(overlay_area, 0.3, heatmap, 0.7, 0)
    frame[10:410, 10:210] = blended
    return frame

def get_camera():
    """
    웹캠 초기화
    """
    width = config.get("CAMERA_WIDTH", 1920)
    height = config.get("CAMERA_HEIGHT", 1080)
    try:
        cap = cv2.VideoCapture(0, cv2.CAP_MSMF)  # Windows에서 MSMF 드라이버 사용 예시
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        logging.info("웹캠 초기화 완료")
        if not cap.isOpened():
            logging.error("웹캠을 열 수 없습니다")
            return None
        return cap
    except Exception as e:
        logging.error(f"get_camera() 예외: {e}")
        return None

def gen_frames(mtcnn, embedder, device, config, DEV_MODE=False):
    """
    카메라에서 프레임을 읽어오고, 얼굴 검출, 임베딩, 인식 로직을 수행.
    제너레이터로서 JPEG 이미지를 yield 하여 Flask에서 스트리밍 가능하게 함.
    """
    global flag, tmp_sno, tmp_sname
    global global_latest_frame, global_latest_face_crop, global_latest_embedding

    font_path = config.get("FONT_PATH", "C:/Windows/Fonts/MALGUN.TTF")
    database = load_database()  # 캐싱된 DB 로드

    camera = get_camera()
    if camera is None:
        logging.error("카메라가 활성화되지 않았습니다")
        return

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                logging.error("웹캠 프레임 수신 실패")
                break
            frame = cv2.flip(frame, 1)  # 좌우 반전

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if DEV_MODE:
                detection = mtcnn.detect(rgb_frame, landmarks=True)
                boxes, probs, landmarks = detection
            else:
                boxes, probs = mtcnn.detect(rgb_frame)
                landmarks = None

            # 첫 번째 얼굴 임베딩 시각화를 위한 참조
            embedding_for_visual = None
            face_crop_local = None

            # boxes가 None이 아니면 (얼굴 검출됨)
            if boxes is not None:
                for idx, (box, prob) in enumerate(zip(boxes, probs)):
                    if prob < 0.90:
                        continue
                    x1, y1, x2, y2 = map(int, box)
                    w, h = x2 - x1, y2 - y1
                    # 크기가 너무 작으면 무시
                    if w < 160 or h < 160:
                        continue

                    # 프레임 중심 근처 얼굴만 처리 (원하는 로직에 따라 조절)
                    cx, cy = (x1 + x2)//2, (y1 + y2)//2
                    frame_cx, frame_cy = frame.shape[1]//2, frame.shape[0]//2
                    if abs(cx - frame_cx) > 200 or abs(cy - frame_cy) > 200:
                        continue

                    # 얼굴 영역 표시
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

                    # DEV_MODE: 좌표, 랜드마크 표시
                    if DEV_MODE:
                        coord_text = f"({x1},{y1})({x2},{y2})"
                        frame = draw_text(frame, coord_text, (x1, y1-25), font_path, 20, (255,255,0))
                        if landmarks is not None and landmarks[idx] is not None:
                            for point in landmarks[idx]:
                                px, py = int(point[0]), int(point[1])
                                cv2.circle(frame, (px, py), 2, (0, 0, 255), -1)

                    # 얼굴 크롭
                    face_crop = rgb_frame[y1:y2, x1:x2]
                    try:
                        face_crop_resized = cv2.resize(face_crop, (160, 160))
                    except Exception as e:
                        logging.warning("얼굴 영역 리사이즈 실패")
                        continue

                    face_tensor = torch.tensor(face_crop_resized.transpose(2,0,1), dtype=torch.float32).div(255).unsqueeze(0).to(device)
                    face_emb = embedder(face_tensor)
                    if face_emb is None:
                        continue

                    if DEV_MODE:
                        emb_vals = np.array_str(face_emb.cpu().detach().numpy().ravel()[:6], precision=2)
                        frame = draw_text(frame, f"embed: {emb_vals}", (x1, y2+20), font_path, 20, (255,0,255))

                    # 첫 번째 유효 얼굴 임베딩만 시각화
                    if embedding_for_visual is None:
                        embedding_for_visual = face_emb
                        face_crop_local = face_crop_resized

                    # ---- 여기서 얼굴 1개만 처리하고 싶으면 break를 걸 수도 있음 ----
                    # break

            # 임베딩 시각화
            # if embedding_for_visual is not None:
            #     frame = visualize_embeddings(frame, embedding_for_visual)

            # 전역 최신값 갱신
            global_latest_frame = frame.copy()
            if face_crop_local is not None:
                global_latest_face_crop = cv2.cvtColor(face_crop_local, cv2.COLOR_RGB2BGR)
            global_latest_embedding = embedding_for_visual

            # 화면 상단 제목
            # frame = draw_text(frame, 'FaceNet Real-time Embedding', (220, 40), font_path, 40, (255, 255, 255))
            # 히트맵 경계용 사각형
            # cv2.rectangle(frame, (5, 5), (215, 415), (255, 255, 255), 2)

            # 인식 로직
            result = recognize_face(database, threshold=0.30)
            if result:
                # 이미 threshold 이내의 사용자가 있다고 판정
                tmp_sno, tmp_sname = result
                label = f"{tmp_sname} ({tmp_sno})"
                # 주의: x1,y1,x2,y2가 마지막 얼굴의 값일 수 있음
                #       여러 얼굴이 있을 수 있으므로, 실제 인식된 얼굴 위치에 대한 처리가 필요.
                #       여기서는 "마지막에 처리된 얼굴 박스"에만 라벨 표시 예시.
                #       또는, result에서 어떤 box 인덱스가 매칭됐는지 추적해야 정확함.
                if boxes is not None and len(boxes) > 0:
                    # 예: 그냥 첫 얼굴 or 마지막 얼굴의 box를 사용
                    box = boxes[-1].astype(int)
                    x1, y1, x2, y2 = box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    frame = draw_text(frame, label, (x1, y1 - 30), font_path, 20, (0,255,0))
            else:
                if global_latest_embedding is not None:
                    # 새로운 얼굴 판단
                    if not is_recently_detected(temp_storage, threshold=0.30):
                        logging.info("새로운 얼굴 감지")
                        # 마지막 박스가 있다면 빨간 박스
                        if boxes is not None and len(boxes) > 0:
                            box = boxes[-1].astype(int)
                            x1, y1, x2, y2 = box
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                            frame = draw_text(frame, "새로운 얼굴", (x1, y1 - 30), font_path, 20, (0,0,255))

                        # 텐서 -> 넘파이
                        emb = global_latest_embedding
                        if torch.is_tensor(emb):
                            emb = emb.cpu().detach().numpy().flatten()
                        temp_storage[tuple(emb)] = time.time()
                        new_face[1] = global_latest_embedding
                        flag = True

            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                logging.warning("프레임 인코딩 실패")
                continue
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    except Exception as e:
        logging.error(f"gen_frames() 예외: {e}")
    finally:
        if camera:
            camera.release()
            logging.info("카메라 자원 해제")

# Flask 라우트: 메인 페이지
@app.route('/')
def index():
    global flag, tmp_sno, tmp_sname
    try:
        flag = False
        tmp_sname = ""
        tmp_sno = ""
        logging.info("메인 페이지 로드")
        return render_template('facerecog.html')
    except Exception as e:
        logging.error(f"/ 엔드포인트 예외: {e}")
        return "에러 발생", 500

# Flask 라우트: 실시간 비디오 스트리밍
@app.route('/video_feed')
def video_feed():
    """
    Flask route로서, gen_frames(...) 호출 결과를 multipart/x-mixed-replace 형태로 스트리밍
    """
    try:
        logging.info("비디오 피드 요청")
        return Response(
            gen_frames(mtcnn, embedder, device, config, DEV_MODE),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )
    except Exception as e:
        logging.error(f"/video_feed 엔드포인트 예외: {e}")
        return "에러 발생", 500

@app.route('/check_flag')
def check_flag():
    """
    JS 등에서 폴링하여 flag 여부와 인식된 사용자 정보(sno, sname)를 가져갈 수 있는 API
    """
    try:
        global flag, tmp_sno, tmp_sname
        data = {"flag": flag}
        if flag:
            if not tmp_sno:
                tmp_sno = 0
            data.update({'sno': int(tmp_sno), 'sname': tmp_sname})
        logging.info(f"check_flag() 응답: {data}")
        return Response(json.dumps(data, ensure_ascii=False), content_type='application/json; charset=utf-8')
    except Exception as e:
        logging.error(f"/check_flag 엔드포인트 예외: {e}")
        return "에러 발생", 500

@app.route('/recognized')
def get_name():
    """
    이미 인식된 사용자 정보 반영
    """
    try:
        global tmp_sno, tmp_sname
        name = request.args.get("name")
        no   = request.args.get("no")
        tmp_sno = no
        tmp_sname = name
        logging.info(f"인식된 사용자: {name} ({no})")
        return render_template('facerecog.html', name=name, no=no)
    except Exception as e:
        logging.error(f"/recognized 엔드포인트 예외: {e}")
        return "에러 발생", 500

@app.route('/unrecognized')
def new_face_detected():
    """
    새로운 얼굴로 판단되어 등록 등의 후속 처리가 필요한 경우
    """
    try:
        logging.info("미인식 얼굴 요청")
        return render_template('facerecog.html', name='new')
    except Exception as e:
        logging.error(f"/unrecognized 엔드포인트 예외: {e}")
        return "에러 발생", 500

@app.route('/checkout')
def checkout_attendance():
    try:
        camera = get_camera()
        if camera is None:
            logging.error("카메라 활성화 실패")
            return "에러 발생", 500

        ret, frame = camera.read()
        if not ret:
            logging.error("체크아웃 시 프레임 획득 실패")
            return "에러 발생", 500

        pic_now = datetime.now()
        filename = './picture/' + pic_now.strftime('%Y%m%d_%H%M%S') + '.jpg'
        cv2.imwrite(filename, frame)
        logging.info(f"사진 저장: {filename}")

        sno = request.args.get("sno")
        db_now = datetime.now()
        print("now 2 : ",db_now)
        event = CheckOut.auto_attendance(sno, db_now)
        print("출석을 판단중입니다.")
        CheckOut.add_attendance_record(sno, event, db_now)
        print("출석을 저장합니다.")
        
        dbms = db.DBManager()
        dbflag = dbms.DBOpen(host="192.168.0.231", dbname="facenutdb", id="bteam", pw="ezen")
        if not dbflag:
            logging.error("데이터베이스 연결 오류 (checkout)")
            return "에러 발생", 500
        sql = f"SELECT sname FROM studentinfo WHERE studentinfo.sno = {sno}"
        dbms.OpenQuery(sql)
        sname = dbms.GetValue(0, 'sname')
        dbms.CloseQuery()

        message = f"{sname}님 {event}하셨습니다."
        return message
    #     dbms = db.DBManager()
    #     dbflag = dbms.DBOpen(host="192.168.0.231", dbname="facenutdb", id="bteam", pw="ezen")
    #     if not dbflag:
    #         logging.error("데이터베이스 연결 오류 (checkout)")
    #         return "에러 발생", 500

    #     sql = "INSERT INTO attendance (sno, classno) SELECT sno, classno FROM studentinfo WHERE sno = " + sno
    #     dbms.RunSQL(sql)
    #     dbms.CloseQuery()

    #     sql = "SELECT studentinfo.sname as sname, attendance.checktime as checktime " \
    #           "FROM studentinfo, attendance " \
    #           "WHERE studentinfo.sno = attendance.sno " \
    #           "AND studentinfo.sno = " + sno + " AND date(checktime) = date(now())"
    #     dbms.OpenQuery(sql)
    #     count = dbms.GetTotal()
    #     sname = dbms.GetValue(0, 'sname')
    #     checktime = dbms.GetValue(0, 'checktime')
    #     if count == 1:
    #         reference_time = checktime.replace(hour=9, minute=10, second=0)
    #         if checktime > reference_time:
    #             message = f"{sname} 님 지각입니다."
    #         else:
    #             message = f"{sname} 님 정상출석입니다."
    #     else:
    #         message = f"{sname} 님 퇴실확인되었습니다."
    #     dbms.CloseQuery()
    #     dbms.DBClose()
    #     logging.info(f"체크아웃 결과: {message}")
    #     return message
    except Exception as e:
        logging.error(f"/checkout 엔드포인트 예외: {e}")
        return "에러 발생", 500

# 아래는 개발자 페이지 예시 =============================================
@app.route('/dev')
def dev_mode():
    global flag, tmp_sno, tmp_sname
    try:
        flag = False
        tmp_sname = ""
        tmp_sno = ""
        logging.info("개발자페이지 로드")
        return render_template('dev.html')
    except Exception as e:
        logging.error(f"/dev 엔드포인트 예외: {e}")
        return "에러 발생", 500

# 개발자 모드 페이지용 비디오 피드 ---------------------------------------
import video_feed_module as dev_feed

@app.route('/video_feed_dev')
def video_feed_dev():
    """
    /dev 페이지에서 사용할, 별도의 스트리밍 로직 (video_feed_module) 예시
    """
    try:
        logging.info("개발자 모드 비디오 피드 요청")
        # dev_feed에 get_video_feed_response(...)가 정의되어 있다고 가정
        return dev_feed.get_video_feed_response(mtcnn, embedder, device, config, DEV_MODE)
    except Exception as e:
        logging.error(f"/video_feed_dev 엔드포인트 예외: {e}")
        return "에러 발생", 500

if __name__ == '__main__':
    logging.info("Flask 서버 시작")
    app.run(host='0.0.0.0', port=5000, debug=True)
