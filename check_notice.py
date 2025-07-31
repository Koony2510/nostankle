from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import time

# ==== 테스트용 날짜 설정 (실제 실행시에는 오늘 날짜 사용 가능) ====
target_date = "2025.07.27"  # 테스트용 날짜
# target_date = datetime.today().strftime('%Y.%m.%d')  # 실제 오늘 날짜

# ==== 크롬 드라이버 옵션 설정 (headless 모드) ====
options = Options()
options.add_argument("--headless")  # 화면없이 실행
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# ==== 드라이버 실행 ====
driver = webdriver.Chrome(options=options)

try:
    url = "https://www.betman.co.kr/main/mainPage/customercenter/notice.do?notiCd=4&searchVal=%EC%B6%95%EA%B5%AC&iPage=1"
    driver.get(url)

    time.sleep(3)  # 페이지 로딩 대기

    # 공지사항 테이블 위치
    table = driver.find_element(By.ID, "lv_noti")
    rows = table.find_elements(By.TAG_NAME, "tr")

    found = False

    for idx, row in enumerate(rows):
        tds = row.find_elements(By.TAG_NAME, "td")
        if len(tds) < 4:
            print(f"[{idx}] 테이블 행 데이터 부족: {len(tds)}개")
            continue

        category = tds[1].text.strip()
        title = tds[2].text.strip()
        date = tds[3].text.strip()

        # 디버깅 출력
        print(f"[{idx}] 구분: '{category}', 제목: '{title}', 날짜: '{date}'")

        # 조건 검사
        if category == "토토" and "축구" in title and "이월" in title and date == target_date:
            print(f"\n✅ 조건에 맞는 공지 발견: '{title}' ({date})\n")
            found = True
            break

    if not found:
        print(f"\n🔍 {target_date}에 해당하는 '축구'와 '이월' 키워드가 포함된 공지를 찾지 못했습니다.\n")

finally:
    driver.quit()
