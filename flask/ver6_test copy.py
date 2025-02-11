import pymysql
import datetime
from datetime import timedelta
import DBManager as db

# =============================================================================
# 테스트를 위한 DB 초기화 함수
# =============================================================================
def setup_test_db():
    """
    테스트를 위해 기존 'attendance' 테이블을 삭제하고 새롭게 생성합니다.
    이 함수는 깨끗한 테스트 환경을 제공하기 위한 용도로만 사용하세요.
    """
    dbms = db.DBManager()
    dbflag = dbms.DBOpen(
        host="localhost",
        dbname="facenetdb",
        id="root",
        pw="ezen"
    )
    if not dbflag:
        print("데이터베이스 연결 오류입니다")
        return
    # 기존 테이블이 존재하면 삭제
    dbms.RunSQL("DROP TABLE IF EXISTS attendance")
    # attendance 테이블 생성 (id는 AUTO_INCREMENT 기본키)
    create_table_sql = """
    CREATE TABLE attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        sno VARCHAR(10) NOT NULL,
        classno VARCHAR(10) NOT NULL,
        event VARCHAR(20) NOT NULL,
        checktime DATETIME NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    print("[DB 초기화] 'attendance' 테이블이 생성되었습니다.")
    dbms.RunSQL(create_table_sql)
    dbms.CloseQuery()
    dbms.DBClose()

# =============================================================================
# 1. DB 연동 함수: 출결 기록 추가, 조회, 업데이트
# =============================================================================
def add_attendance_record(sno, classno, event, checktime=None):
    """
    출결 기록을 DB에 추가하는 함수.
    테이블 'attendance'에는 (sno, classno, event, checktime)를 저장합니다.
    """
    dbms = db.DBManager()
    dbflag = dbms.DBOpen(
        host="localhost",
        dbname="facenetdb",
        id="root",
        pw="ezen"
    )
    if not dbflag:
        print("데이터베이스 연결 오류입니다")
        return
    
    #sql = f"INSERT INTO attendance (sno, classno, event, checktime) VALUES ('{sno}', '{classno}', '{event}', '{checktime}')"
    sql = f"INSERT INTO attendance (sno, classno, event) VALUES ('{sno}', '{classno}', '{event}')"
    dbms.RunSQL(sql)
    dbms.CloseQuery()
    dbms.DBClose()
    print(f"[추가] {checktime.time()} - {sno}/{classno} : {event}")

def get_today_attendance_records(sno, classno, date):
    """
    특정 학생(sno)과 강의(classno)의, 지정 날짜(date)의 출결 기록 리스트를 조회합니다.
    날짜는 date 객체를 사용하며, DB에서는 'YYYY-MM-DD' 형식으로 비교합니다.
    """
    dbms = db.DBManager()
    dbflag = dbms.DBOpen(
        host="localhost",
        dbname="facenetdb",
        id="root",
        pw="ezen"
    )
    if dbflag == False :
        print("데이터베이스 연결 오류입니다")
        return {}
    else :
        sql = f"""
            SELECT * FROM attendance 
            WHERE sno='{sno}' AND classno='{classno}' AND DATE(checktime)='{date}'
            ORDER BY checktime ASC
        """
        #dbms.cursor = dbms.con.cursor()
        #dbms.cursor.execute(sql)
        #records = dbms.cursor.fetchall()
        dbms.OpenQuery(sql)
        records = dbms.GetList()
        dbms.CloseQuery()
        dbms.DBClose()
        return records

def update_attendance_record(record_id, new_event):
    """
    특정 출결 레코드(record_id)의 event 컬럼을 new_event로 업데이트합니다.
    """
    dbms = db.DBManager()
    dbflag = dbms.DBOpen(
        host="localhost",
        dbname="facenetdb",
        id="root",
        pw="ezen"
    )
    if not dbflag:
        print("데이터베이스 연결 오류입니다")
        return

    sql = f"UPDATE attendance SET event='{new_event}' WHERE id='{record_id}'"
    dbms.RunSQL(sql)
    dbms.CloseQuery()
    dbms.DBClose()
    print(f"[업데이트] id {record_id} → {new_event}")

def get_all_attendance_records(date):
    """
    지정 날짜(date)의 전체 출결 기록을 조회합니다.
    """
    dbms = db.DBManager()
    dbflag = dbms.DBOpen(
        host="localhost",
        dbname="facenetdb",
        id="root",
        pw="ezen"
    )
    if dbflag == False :
        print("데이터베이스 연결 오류입니다")
        return {}
    else :
        sql = f"SELECT * FROM attendance WHERE DATE(checktime)='{date}' ORDER BY sno, classno, checktime ASC"
        #dbms.cursor = dbms.con.cursor()
        #dbms.cursor.execute(sql)
        #records = dbms.cursor.fetchall()
        dbms.OpenQuery(sql)
        records = dbms.GetList()
        dbms.CloseQuery()
        dbms.DBClose()
        return records

# =============================================================================
# 2. 조퇴 가능 시각 및 효과적 출석시간 계산 함수
# =============================================================================
def compute_allowed_early_leave(initial_arrival_dt):
    """
    최초 입실 시각(initial_arrival_dt)을 기준으로 조퇴(또는 최종 출결) 가능 시각을 계산합니다.
    수업: 09:00~18:00, 점심: 13:00~14:00, 실제 수업시간 8시간, 50% 출석 = 4시간.
    """
    today = initial_arrival_dt.date()
    lunch_start_dt = datetime.datetime.combine(today, datetime.time(13, 0, 0))
    lunch_end_dt   = datetime.datetime.combine(today, datetime.time(14, 0, 0))
    required_attendance = timedelta(hours=4)
    if initial_arrival_dt < lunch_start_dt:
        attended_morning = lunch_start_dt - initial_arrival_dt
        needed_afternoon = required_attendance - attended_morning
        if needed_afternoon < timedelta(0):
            needed_afternoon = timedelta(0)
        allowed = lunch_end_dt + needed_afternoon
    else:
        allowed = initial_arrival_dt + required_attendance
    return allowed

def compute_effective_attendance(initial, final):
    """
    최초 입실 시간(initial)과 최종 퇴실(또는 조퇴) 시간(final)으로,
    점심시간(13:00~14:00)을 제외한 실제 출석시간을 계산합니다.
    """
    today = initial.date()
    lunch_start_dt = datetime.datetime.combine(today, datetime.time(13, 0, 0))
    lunch_end_dt   = datetime.datetime.combine(today, datetime.time(14, 0, 0))
    if final <= lunch_start_dt:
        effective = final - initial
    elif initial < lunch_start_dt and final <= lunch_end_dt:
        effective = lunch_start_dt - initial
    elif initial < lunch_start_dt and final > lunch_end_dt:
        effective = (lunch_start_dt - initial) + (final - lunch_end_dt)
    else:
        effective = final - initial
    return effective

# =============================================================================
# 3. 실시간 출결 판별 함수 (자동 입력)
# =============================================================================
def auto_attendance(sno, classno, current_dt, is_final=True):
    """
    학생의 현재 탭 시각(current_dt)과 DB상의 기존 기록을 바탕으로,
    출결 이벤트를 자동 판별하여 반환합니다.
    
    [판별 규칙]
      - 수업 시간: 09:00 ~ 18:00  
        → 수업 시작+10분: 09:10, 수업 종료-10분: 17:50.
      - **첫 번째 기록 (count == 0):**
          - current_dt ≤ 09:10 → "출석입니다"
          - 09:10 초과 ~ 18:00 미만 → "지각입니다"
          - 만약 current_dt ≥ 18:00이면 → "수업시간이 아닙니다"
      - **두 번째 기록 (count == 1):** (2-tap 최종 입력)
          - 만약 current_dt가 오전(13:00) 이전이면 → "결석입니다"
          - elif current_dt ≥ 17:50 → "퇴실입니다"
          - else (수업 중, 13:00 이상, 17:50 미만):
                첫 기록(입실) 기준 allowed = compute_allowed_early_leave(첫 기록)
                if current_dt < allowed → "결석입니다"
                else → "조퇴입니다"
          - 단, is_final이 False이면 "기록"을 반환합니다.
      - **세 번째 기록 (count == 2):**
          - (보통 외출/복귀용 placeholder)
          - is_final이 False이면 → "기록" 반환
          - else → if current_dt ≥ 17:50 then "퇴실입니다", else "조퇴입니다"
      - **네 번째 기록 (count == 3):** (4-tap 시나리오 최종 입력)
          - is_final이 False이면 → "기록"
          - else: if current_dt < 17:50 → "조퇴입니다", else → "퇴실입니다"
      - **다섯 번째 기록 (count == 4):**
          - 만약 기존 4번째 기록이 "조퇴입니다"이면,
              → 해당 기록을 "중복입력"으로 업데이트한 후 이번 입력은 "퇴실입니다"
          - 그렇지 않으면 → "이미 출결 처리가 완료되었습니다"
      - **기록이 5건 이상이면** → "이미 출결 처리가 완료되었습니다"
    """
    today = current_dt.date()
    start_dt = datetime.datetime.combine(today, datetime.time(9, 0, 0))
    end_dt   = datetime.datetime.combine(today, datetime.time(18, 0, 0))
    final_threshold = end_dt - timedelta(minutes=10)  # 17:50
    lunch_start_dt = datetime.datetime.combine(today, datetime.time(13, 0, 0))
    
    records = get_today_attendance_records(sno, classno, today)
    count = len(records)
    
    if count == 0:
        # 첫 탭: 입실 판단
        if current_dt <= start_dt + timedelta(minutes=10):
            event = "출석"
        elif current_dt < end_dt:
            event = "지각"
        else:
            event = "불인정"
    
    elif count == 1:
        # 두번째 탭 (2-tap 최종 입력)
        if not is_final:
            event = "기록"
        else:
            if current_dt < lunch_start_dt:
                event = "결석"
            elif current_dt >= final_threshold:
                event = "퇴실"
            else:
                print(type(records))
                print(records)
                #exit()
                initial_arrival = records[0]['checktime']
                allowed = compute_allowed_early_leave(initial_arrival)
                if current_dt < allowed:
                    event = "결석"
                else:
                    event = "조퇴"
    
    elif count == 2:
        # 세번째 탭 (보통 외출/복귀용 placeholder)
        if not is_final:
            event = "기록"
        else:
            if current_dt >= final_threshold:
                event = "퇴실"
            else:
                event = "조퇴"
    
    elif count == 3:
        # 네번째 탭 (4-tap 시나리오 최종 입력)
        if not is_final:
            event = "기록"
        else:
            if current_dt < final_threshold:
                event = "조퇴"
            else:
                event = "퇴실"
    
    elif count == 4:
        # 다섯번째 탭: 기존 4번째 기록이 "조퇴입니다"면 중복 처리 후 "퇴실입니다"
        recs = get_today_attendance_records(sno, classno, today)
        recs.sort(key=lambda r: r['checktime'])
        if recs[-1]['event'] == "조퇴":
            update_attendance_record(recs[-1]['id'], "중복")
            event = "퇴실"
        else:
            event = "퇴실"
    
    else:
        event = "퇴실"
    
    return event

# =============================================================================
# 4. 배치 업데이트 함수: 외출/복귀 기록 업데이트
# =============================================================================
def update_return_events_for_student(sno, classno, date):
    """
    특정 학생, 강의, 날짜의 출결 기록이
    [출석(또는 지각), 기록, 기록, (조퇴 또는 퇴실)] 형태라면,
    두번째 기록을 "외출입니다", 세번째 기록을 "복귀입니다"로 업데이트합니다.
    """
    records = get_today_attendance_records(sno, classno, date)
    # records.sort(key=lambda r: r['checktime'])
    
    if len(records) == 4:
        first_event = records[0]['event']
        last_event  = records[-1]['event']
        if first_event in ["출석", "지각"] and last_event in ["조퇴", "퇴실"]:
            print(f"\n[업데이트 전] {sno}-{classno} {date}의 기록:")
            for r in records:
                print(r)
            # 두번째 기록을 "외출입니다", 세번째 기록을 "복귀입니다"로 업데이트
            update_attendance_record(records[1]['id'], "외출")
            update_attendance_record(records[2]['id'], "복귀")
            # 업데이트 후 결과 확인
            updated = get_today_attendance_records(sno, classno, date)
            print(f"\n[업데이트 후] {sno}-{classno} {date}의 기록:")
            for r in updated:
                print(r)
        else:
            print(f"{sno}-{classno} {date}: 기록 패턴 불일치")
    else:
        print(f"{sno}-{classno} {date}: 기록 건수가 4건이 아니어서 업데이트하지 않음 (현재 {len(records)}건)")

def batch_update_attendance_records():
    """
    전체 출결 기록을 (학생, 강의, 날짜)별로 그룹화하여,
    [출석(또는 지각), 기록, 기록, (조퇴 또는 퇴실)] 형태이면
    두번째, 세번째 기록을 각각 "외출입니다", "복귀입니다"로 업데이트합니다.
    """
    today = datetime.date.today()
    all_records = get_all_attendance_records(today)
    groups = {}
    for rec in all_records:
        key = (rec['sno'], rec['classno'], rec['checktime'].date())
        groups.setdefault(key, []).append(rec)
    
    for key, recs in groups.items():
        sno, classno, date = key
        recs.sort(key=lambda r: r['checktime'])
        if len(recs) == 4:
            if recs[0]['event'] in ["출석", "지각"] and recs[-1]['event'] in ["조퇴", "퇴실"]:
                update_attendance_record(recs[1]['id'], "외출")
                update_attendance_record(recs[2]['id'], "복귀")
                print(f"\n[배치 업데이트] {sno}-{classno} {date} 최종 기록:")
                updated = get_today_attendance_records(sno, classno, date)
                for r in updated:
                    print(r)
            else:
                print(f"{sno}-{classno} {date}: 기록 패턴 불일치")
        else:
            print(f"{sno}-{classno} {date}: 기록 건수 {len(recs)}건 → 업데이트 대상 아님")

# =============================================================================
# 5. 최종 출결 기록 확정 배치 함수 (예: 자정 실행)
# =============================================================================
def finalize_attendance_records():
    """
    자정 등에 실행되어, 각 학생의 최종 출결 기록을 확정합니다.
    각 그룹(학생, 강의, 날짜)별로 최초 입실 시간과 최종 기록 시각을
    비교하여, 점심시간 제외 효과적 출석시간이 4시간 미만이면 최종 기록을
    "수업 불인정"으로 업데이트합니다.
    """
    today = datetime.date.today()
    all_records = get_all_attendance_records(today)
    groups = {}
    for rec in all_records:
        key = (rec['sno'], rec['classno'], rec['checktime'].date())
        groups.setdefault(key, []).append(rec)
    
    print("\n[최종 출결 확정 배치] 실행")
    for key, recs in groups.items():
        sno, classno, date = key
        recs.sort(key=lambda r: r['checktime'])
        final_record = recs[-1]
        # 최종 입력이 "기록" 등 확정 상태가 아니라면 건너뜁니다.
        if final_record['event'] == "기록":
            print(f"{sno}-{classno} {date}: 최종 입력이 완료되지 않아 확정 대상 아님.")
            continue
        initial = recs[0]['checktime']
        final = final_record['checktime']
        effective = compute_effective_attendance(initial, final)
        print(f"{sno}-{classno} {date}: 효과적 출석시간 = {effective}")
        if effective < timedelta(hours=4):
            update_attendance_record(final_record['id'], "불인정")
            print(f"{sno}-{classno} {date}: 출석시간 4시간 미만 → '수업 불인정'으로 업데이트")
        else:
            if final_record['event'] == "외출":
                update_attendance_record(final_record['id'], "조퇴")
            print(f"{sno}-{classno} {date}: 출석시간 충분 → 기존 최종 기록({final_record['event']}) 유지")

# =============================================================================
# 6. 테스트 케이스 실행
# =============================================================================
if __name__ == "__main__":
    # 1) 테스트를 위해 DB 초기화 (attendance 테이블 재생성)
    setup_test_db()

    # 오늘 날짜와 강의 번호 지정
    now = datetime.datetime.now()
    today = datetime.date.today()
    classno = "1"
    
    print("\n=== 실시간 출결 입력 테스트 ===\n")
    
    # ----- 학생 a: 출석, 퇴실 (2-tap 시나리오) -----
    # 첫 탭: 08:55 → 09:10 이전 → "출석입니다"
    event = auto_attendance("1", classno, now)
    add_attendance_record("1", classno, event, now)
    # 두번째 탭: 18:05 → 17:50 이상 → "퇴실입니다"
    dt = datetime.datetime.combine(today, datetime.time(18, 5))
    event = auto_attendance("1", classno, dt)
    add_attendance_record("1", classno, event, dt)

    # ----- 학생 a: 출석, 퇴실 (2-tap 시나리오) -----
    # 첫 탭: 08:55 → 09:10 이전 → "출석입니다"
    dt = datetime.datetime.combine(today, datetime.time(8, 55))
    event = auto_attendance("1", classno, dt)
    add_attendance_record("1", classno, event, dt)
    # 두번째 탭: 18:05 → 17:50 이상 → "퇴실입니다"
    dt = datetime.datetime.combine(today, datetime.time(18, 5))
    event = auto_attendance("1", classno, dt)
    add_attendance_record("1", classno, event, dt)
    
    # ----- 학생 b: 지각, 퇴실 (2-tap 시나리오) -----
    # 첫 탭: 09:15 → "지각입니다"
    dt = datetime.datetime.combine(today, datetime.time(9, 15))
    event = auto_attendance("2", classno, dt)
    add_attendance_record("2", classno, event, dt)
    # 두번째 탭: 18:05 → "퇴실입니다"
    dt = datetime.datetime.combine(today, datetime.time(18, 5))
    event = auto_attendance("2", classno, dt)
    add_attendance_record("2", classno, event, dt)
    
    # ----- 학생 c: 출석, 조퇴 (2-tap 시나리오) -----
    # 첫 탭: 08:55 → "출석입니다"
    dt = datetime.datetime.combine(today, datetime.time(8, 55))
    event = auto_attendance("3", classno, dt)
    add_attendance_record("3", classno, event, dt)
    # 두번째 탭: 14:05 → 조퇴 가능 시간 경과 후 → "조퇴입니다"
    dt = datetime.datetime.combine(today, datetime.time(14, 5))
    event = auto_attendance("3", classno, dt)
    add_attendance_record("3", classno, event, dt)
    
    # ----- 학생 d: 출석, 외출, 복귀, 퇴실 (4-tap 시나리오) -----
    # 첫 탭: 08:55 → "출석입니다"
    dt = datetime.datetime.combine(today, datetime.time(8, 55))
    event = auto_attendance("4", classno, dt)
    add_attendance_record("4", classno, event, dt)
    # 두번째 탭: 14:30, 중간 입력 (외출 의도, is_final=False) → "기록"
    dt = datetime.datetime.combine(today, datetime.time(14, 30))
    event = auto_attendance("4", classno, dt, is_final=False)
    add_attendance_record("4", classno, event, dt)
    # 세번째 탭: 15:10, 중간 입력 (복귀 의도, is_final=False) → "기록"
    dt = datetime.datetime.combine(today, datetime.time(15, 10))
    event = auto_attendance("4", classno, dt, is_final=False)
    add_attendance_record("4", classno, event, dt)
    # 네번째 탭: 18:05 → 최종 입력 → "퇴실입니다"
    dt = datetime.datetime.combine(today, datetime.time(18, 5))
    event = auto_attendance("4", classno, dt)
    add_attendance_record("4", classno, event, dt)
    
    # # ----- 학생 e: 출석, (오전중 퇴실) → 결석 처리 (2-tap 시나리오) -----
    # # 첫 탭: 08:55 → "출석입니다"
    # dt = datetime.datetime.combine(today, datetime.time(8, 55))
    # event = auto_attendance("e", classno, dt)
    # add_attendance_record("e", classno, event, dt)
    # # 두번째 탭: 11:00 (오전) → "결석입니다"
    # dt = datetime.datetime.combine(today, datetime.time(11, 0))
    # event = auto_attendance("e", classno, dt)
    # add_attendance_record("e", classno, event, dt)
    
    # # ----- 학생 f: 첫 입력이 수업시간 이후 (예: 18:30) → "수업시간이 아닙니다"
    # dt = datetime.datetime.combine(today, datetime.time(18, 30))
    # event = auto_attendance("f", classno, dt)
    # add_attendance_record("f", classno, event, dt)
    
    # ----- 현재까지 입력된 전체 출결 기록 조회 -----
    print("\n=== 배치 업데이트 전 전체 출결 기록 ===")
    all_recs = get_all_attendance_records(today)
    for rec in all_recs:
        print(rec)
    
    # ----- 개별 학생별 외출/복귀 업데이트 (예: 학생 d) -----
    print("\n>>> 개별 학생별 외출/복귀 업데이트 (대상: 학생 d)")
    update_return_events_for_student("4", classno, today)
    
    # ----- 전체 배치 업데이트 실행 -----
    print("\n>>> 전체 배치 업데이트 실행")
    batch_update_attendance_records()
    
    # ----- 수업 종료 후(예: 자정)에 최종 출결 확정 배치 실행 -----
    print("\n>>> 최종 출결 확정 배치 실행 (예: 자정 실행)")
    finalize_attendance_records()
    
    # ----- 최종 출결 기록 조회 -----
    print("\n=== 최종 출결 기록 ===")
    all_recs = get_all_attendance_records(today)
    for rec in all_recs:
        print(rec)
