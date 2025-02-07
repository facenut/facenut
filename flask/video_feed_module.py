# video_feed_module.py

# 필요한 라이브러리들을 불러옵니다.
import cv2                       # OpenCV: 이미지/비디오 처리
import datetime                  # 날짜 및 시간 관련 처리
import numpy as np               # 행렬 및 수치 계산
import torch                     # 파이토치: 딥러닝 모델 처리
import logging                   # 로깅: 로그 메시지 기록
from facenet_pytorch import MTCNN  # 얼굴 검출 모델
from PIL import ImageFont, ImageDraw, Image  # PIL: 이미지에 텍스트 오버레이

# 전역 변수: 비동기 캡쳐용으로 사용되는 최신 프레임, 얼굴 영역, 임베딩 값을 저장합니다.
global_latest_frame = None
global_latest_face_crop = None
global_latest_embedding = None

def draw_text(img, text, position, font_path, font_size=20, color=(255,255,255)):
    """
    PIL을 이용해 한글을 포함한 텍스트를 이미지에 오버레이하는 함수입니다.
    
    매개변수:
        img: OpenCV 이미지 (numpy array)
        text: 오버레이할 텍스트 (문자열)
        position: 텍스트 위치 (x, y 좌표 튜플)
        font_path: 사용할 폰트 파일 경로 (예: "C:/Windows/Fonts/MALGUN.TTF")
        font_size: 폰트 크기 (기본값 20)
        color: 텍스트 색상 (BGR 튜플, 기본값 흰색)
    
    반환:
        텍스트가 추가된 OpenCV 이미지
    """
    # OpenCV 이미지를 PIL 이미지로 변환합니다.
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    try:
        # 지정한 폰트 파일을 불러옵니다.
        font = ImageFont.truetype(font_path, font_size, encoding="utf-8")
    except IOError:
        # 만약 폰트 파일을 찾지 못하면 기본 폰트를 사용하고 경고 로그를 남깁니다.
        logging.warning("폰트 파일을 찾지 못해 기본 폰트 사용")
        font = ImageFont.load_default()
    # 이미지에 텍스트를 그립니다.
    draw.text(position, text, font=font, fill=color)
    # PIL 이미지를 다시 OpenCV 이미지로 변환하여 반환합니다.
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def visualize_embeddings(frame, embeddings):
    """
    임베딩 값을 히트맵 형태로 시각화하여 원본 프레임에 오버레이합니다.
    
    매개변수:
        frame: 현재 처리 중인 OpenCV 프레임
        embeddings: 얼굴 임베딩 값 (텐서 또는 넘파이 배열)
    
    반환:
        히트맵이 오버레이된 프레임
    """
    # 임베딩 배열의 차원이 2차원 이상인 경우, 첫 번째 결과의 앞 128 요소 사용
    if embeddings.ndim > 1:
        emb_vis = embeddings[0][:128]
    else:
        emb_vis = embeddings[:128]
    # 임베딩 값이 파이토치 텐서인 경우, 넘파이 배열로 변환합니다.
    if torch.is_tensor(emb_vis):
        emb_vis = emb_vis.cpu().detach().numpy()
    # 임베딩 값을 0과 1 사이로 정규화합니다.
    normalized = (emb_vis - emb_vis.min()) / (emb_vis.max() - emb_vis.min() + 1e-6)
    # 0~255 범위의 값으로 변환하여 정수형 배열로 만듭니다.
    heatmap = (normalized * 255).astype(np.uint8)
    # 16행 8열의 배열로 재구성합니다. (16 x 8 = 128)
    heatmap = heatmap.reshape(16, 8)
    # OpenCV의 applyColorMap 함수를 사용해 컬러 히트맵으로 변환합니다.
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    # 히트맵의 크기를 프레임에 맞게 조정합니다.
    heatmap = cv2.resize(heatmap, (200, 400))
    # 프레임의 특정 영역(좌상단의 작은 사각형 영역)을 선택합니다.
    overlay_area = frame[10:410, 10:210]
    # 선택된 영역과 히트맵을 합성합니다. (가중치 0.3과 0.7을 사용)
    blended = cv2.addWeighted(overlay_area, 0.3, heatmap, 0.7, 0)
    # 합성된 이미지를 원래 프레임의 해당 영역에 다시 넣어줍니다.
    frame[10:410, 10:210] = blended
    return frame

def gen_frames(mtcnn, embedder, device, config, DEV_MODE):
    """
    웹캠으로부터 실시간 비디오 프레임을 읽어오고, 얼굴 검출 및 임베딩 처리 후
    결과를 JPEG 형식으로 인코딩하여 스트리밍할 수 있도록 제너레이터 형태로 반환합니다.
    
    매개변수:
        mtcnn: 얼굴 검출을 위한 MTCNN 모델
        embedder: 얼굴 임베딩을 생성하는 모델
        device: 모델이 실행될 디바이스 (예: "cpu" 또는 "cuda")
        config: 카메라, 폰트 등의 설정 정보가 담긴 딕셔너리
        DEV_MODE: 개발 모드 여부 (True면 추가 디버그 정보 출력)
    
    제너레이터:
        JPEG 형식의 프레임 바이트 스트림
    """
    global global_latest_frame, global_latest_face_crop, global_latest_embedding
    
    # 설정 파일에서 카메라 해상도와 폰트 경로 정보를 가져옵니다.
    width = config.get("CAMERA_WIDTH", 800)
    height = config.get("CAMERA_HEIGHT", 600)
    font_path = config.get("FONT_PATH", "C:/Windows/Fonts/MALGUN.TTF")
    
    # 웹캠을 초기화합니다.
    cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    logging.info("웹캠 초기화 완료")
    
    # 무한 루프를 돌면서 웹캠 프레임을 처리합니다.
    while True:
        ret, frame = cap.read()
        # 프레임을 제대로 읽지 못하면 에러 로그를 남기고 루프를 종료합니다.
        if not ret:
            logging.error("웹캠 프레임 수신 실패")
            break
        
        # ★ 좌우 반전: frame을 미러링 처리합니다.
        frame = cv2.flip(frame, 1)

        # OpenCV 프레임은 BGR 형식이므로, RGB 형식으로 변환합니다.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 개발 모드(DEV_MODE)가 True일 경우, 얼굴 검출 결과와 함께 랜드마크도 함께 받아옵니다.
        if DEV_MODE:
            detection = mtcnn.detect(rgb_frame, landmarks=True)
            boxes = detection[0]       # 얼굴의 경계 상자 (bounding boxes)
            probs = detection[1]       # 얼굴 검출 확률 (confidence)
            landmarks = detection[2]   # 얼굴 랜드마크 (눈, 코, 입 등)
            logging.debug(f"실시간 얼굴 검출: {len(boxes) if boxes is not None else 0}개")
        else:
            # 개발 모드가 아니면, 얼굴 검출 시 랜드마크는 제외합니다.
            boxes, probs = mtcnn.detect(rgb_frame)
            landmarks = None

        # 얼굴 임베딩 시각화를 위한 임시 변수
        embedding_for_visual = None
        # 얼굴 영역을 잘라낸 이미지를 저장할 변수
        face_crop_local = None

        # 얼굴이 검출되었다면 (boxes가 None이 아닐 때)
        if boxes is not None:
            # 검출된 얼굴 각각에 대해 반복합니다.
            for idx, (box, prob) in enumerate(zip(boxes, probs)):
                # 얼굴 검출 확률이 낮은 경우 무시합니다.
                if prob < 0.90:
                    continue
                # 경계 상자의 좌표를 정수형으로 변환합니다.
                x1, y1, x2, y2 = map(int, box)
                w, h = x2 - x1, y2 - y1
                # 얼굴 크기가 너무 작으면 (너비나 높이가 200보다 작으면) 무시합니다.
                if w < 200 or h < 200:
                    continue
                # 얼굴의 중심 좌표 계산
                cx, cy = (x1+x2)//2, (y1+y2)//2
                # 프레임 중심 좌표 계산
                frame_cx, frame_cy = frame.shape[1]//2, frame.shape[0]//2
                # 얼굴 중심과 프레임 중심 사이의 거리가 너무 멀면 무시합니다.
                if abs(cx-frame_cx) > 120 or abs(cy-frame_cy) > 120:
                    continue

                # 얼굴 영역 주위에 초록색 사각형을 그려 얼굴 검출 결과를 표시합니다.
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                
                # 개발 모드에서는 얼굴의 좌표 정보를 텍스트로 표시하고, 랜드마크(눈, 코, 입 등)를 원으로 표시합니다.
                if DEV_MODE:
                    coord_text = f"({x1},{y1}) ({x2},{y2})"
                    frame = draw_text(frame, coord_text, (x1, y1-25), font_path, 20, (255,255,0))
                    if landmarks is not None and landmarks[idx] is not None:
                        for point in landmarks[idx]:
                            px, py = int(point[0]), int(point[1])
                            cv2.circle(frame, (px, py), 2, (0, 0, 255), -1)
                
                # 검출된 얼굴 영역을 잘라냅니다.
                face_crop = rgb_frame[y1:y2, x1:x2]
                try:
                    # 얼굴 이미지를 임베딩 모델의 입력 크기에 맞게 (160x160) 리사이즈합니다.
                    face_crop_resized = cv2.resize(face_crop, (160, 160))
                except Exception as e:
                    logging.warning("얼굴 영역 리사이즈 실패")
                    continue
                
                # 리사이즈된 얼굴 이미지를 텐서로 변환합니다.
                # 이미지의 차원을 (채널, 높이, 너비)로 재배열하고, 정규화 (0~1 범위)합니다.
                face_tensor = torch.tensor(face_crop_resized.transpose(2, 0, 1), dtype=torch.float32).div(255).unsqueeze(0).to(device)
                # 임베딩 모델을 통해 얼굴의 임베딩 값을 추출합니다.
                face_emb = embedder(face_tensor)
                if face_emb is None:
                    continue
                # 개발 모드에서는 임베딩 값의 앞 몇 개 숫자를 텍스트로 표시합니다.
                if DEV_MODE:
                    emb_vals = np.array_str(face_emb.cpu().detach().numpy().ravel()[:6], precision=2)
                    frame = draw_text(frame, f"embed: {emb_vals}", (x1, y2+20), font_path, 20, (255,0,255))
                # 첫 번째로 유효한 얼굴 임베딩 값을 시각화 및 전역 변수 저장을 위해 선택합니다.
                if embedding_for_visual is None:
                    embedding_for_visual = face_emb
                    face_crop_local = face_crop_resized

        # 얼굴 임베딩이 있다면 히트맵으로 시각화하여 프레임에 오버레이합니다.
        if embedding_for_visual is not None:
            frame = visualize_embeddings(frame, embedding_for_visual)

        # 최신 프레임, 얼굴 영역, 임베딩 값을 전역 변수에 저장합니다.
        global_latest_frame = frame.copy()
        global_latest_face_crop = cv2.cvtColor(face_crop_local, cv2.COLOR_RGB2BGR) if face_crop_local is not None else None
        global_latest_embedding = embedding_for_visual

        # 프레임 중앙에 제목 텍스트를 오버레이합니다.
        frame = draw_text(frame, 'FaceNet Real-time Embedding', (220, 40), font_path, 40, (255, 255, 255))
        # 히트맵 영역을 둘러싸는 흰색 사각형을 그립니다.
        cv2.rectangle(frame, (5, 5), (215, 415), (255, 255, 255), 2)

        # 프레임을 JPEG 포맷으로 인코딩합니다.
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        # HTTP 스트리밍을 위한 멀티파트 형식으로 프레임 바이트를 반환합니다.
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def get_video_feed_response(mtcnn, embedder, device, config, DEV_MODE):
    """
    Flask의 Response 객체를 생성하여, 실시간 비디오 스트리밍 응답을 반환합니다.
    
    매개변수:
        mtcnn: 얼굴 검출 모델 (MTCNN)
        embedder: 얼굴 임베딩 생성 모델
        device: 모델 실행 디바이스 ("cpu" 또는 "cuda")
        config: 카메라, 폰트 등의 설정 정보
        DEV_MODE: 개발 모드 여부
    
    반환:
        Flask Response 객체 (multipart/x-mixed-replace MIME 타입)
    """
    from flask import Response
    return Response(
        gen_frames(mtcnn, embedder, device, config, DEV_MODE),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )
