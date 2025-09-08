# conftest.py : 테스트 환경 설정 및 공통 기능 관리
"""
주요 기능
1. 자동 인식
- 같은 디렉토리에 conftest.py 파일이 있으면 pytest가 자동으로 불러옴
- 별도로 import conftest 같은 코드를 쓸 필요가 없다

2. Fixture 관리
- @pytest.fixture로 정의한 함수를 넣어두면, 해당 디렉토리 및 
하위 디렉토리 테스트 파일에서 다 쓸 수 있다
- 중복 코드를 줄이고 테스트 실행 환경을 일정하게 유지할 수 있다

3. Hook 함수
- pytest의 동작을 가로채거나 커스터마이징할 수 있는 hook을 정의할 수 있다
- ex) 테스트 시작 전/후에 로그 찍기, 테스트 결과 보고 형식 바꾸기

위치 선택 가이드
1. tests 폴더 안에 두는 경우 (추천)
- tests/conftest.py
- 대부분의 자동화 테스트에서는 이 구조를 가장 많이 씀
- 이유 :  테스트 코드 전용 설정만 모아두고, 애플리케이션 코드(utils,config 등)와는 분리하기 좋음

2. 프로젝트 루트에 두는 경우
- project_root/conftest.py
- 프로제젝트 전채에서 공유해야 하는 fixture (예: DB 연결, 전역 로거 등)일 때 사용
- 단점 : 프로젝트가 커지면 범위가 너무 넓어져서 불필요한 테스트까지 영향을 받을 수 있음
"""

# conftest.py
import os
import time                 # os/time : 환경변수 읽기, 타임스탬프 만들 때 사용
from pathlib import Path    # Path : artifacts/ 폴더를 안전하게 생성하기 위해 사용

import pytest               # pytest : fixture/hook을 쓰기 위해 필요
from appium import webdriver
from appium.options.android import UiAutomator2Options 
# Appium 세션(드라이버) 생성과 Android 용 옵션을 다루기 위해 핗요

# ---- 로깅 설정 --------
# 필요에 맞게 level=INFO/DEBUG 조절, 파일로 남기고 싶으면 filename="test.log" 추가
logging.basicConfig(
    filename="test.log",   # 로그 저장할 파일 이름
    filemode="w"           # "w"는 덮어쓰기, "a"는 이어쓰기
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session") # 각 테스트 세션이 실행될 때마다 생성되고 삭제
def appium_url():
    # 로컬 Appium 서버는 보통 http 사용
    url = os.getenv("APPIUM_URL", "http://localhost:4723")
    logger.info(f"Using Appium URL: {url}")
    return url


@pytest.fixture(scope="function") # 테스트 함수마다 새로운 Appium 세션을 띄우고, 테스트가 끝나면 종료
def driver(appium_url, request): # request, 현재 실행 중인 테스트 노드 정보에 접근할 때 쓰임
    opts = UiAutomator2Options()

    # 필수/권장 capability 설정
    # (Appium 2에서는 appium: prefix 권장, set_capability 사용이 호환성 좋음)
    opts.set_capability("platformName", "Android")
    opts.set_capability("appium:automationName", "UiAutomator2")

    udid = os.getenv("UUID", "R3CN30QEK1W")
    app_pkg = os.getenv("APP_PACKAGE", "net.skyscanner.android.main")
    app_act = os.getenv("APP_ACTIVITY", "net.skyscanner.shell.ui.activity.SplashActivity")

    opts.set_capability("appium:udid", udid)
    opts.set_capability("appium:appPackage", app_pkg)
    opts.set_capability("appium:appActivity", app_act)

    logger.info(f"Creating driver (udid={udid}, package={app_pkg}, activity={app_act})")

    drv = webdriver.Remote(appium_url, options=opts)
    drv.implicitly_wait(3)

    yield drv # 드라이버 종료

    # ---- teardown: 실패 시 아티팩트 저장 + 항상 종료 ----
    try:
        # 실패 여부 확인 (pytest 훅에서 rep_call을 심어줌)
        failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
        if failed:
            ts = time.strftime("%Y%m%d_%H%M%S")
            artifacts_dir = Path("artifacts")
            artifacts_dir.mkdir(parents=True, exist_ok=True)

            png = f"artifacts/{request.node.name}_{ts}.png"
            xml = f"artifacts/{request.node.name}_{ts}.xml"

            # 스크린샷 저장
            try:
                drv.save_screenshot(png)
                logger.info(f"[ARTIFACT] Screenshot saved: {png}")
            except Exception as e:
                logger.warning(f"[ARTIFACT] Failed to save screenshot : {png} ({e})", exc_info=True)

            # vpdlwl 소스 저장
            try:
                with open(xml, "w", encoding="utf-8") as f:
                    f.write(drv.page_source)
                    logger.info(f"[ARTIFACT] Page source saved: {xml}")
            except Exception as e:
                logger.warning(f"[ARTIFACT] Failed to save page source: {xml} ({e})", exc_info=True)
    finally:
        # 성공/실패와 무관하게 항상 종료
        try:
            drv.quit()
            logger.info("Driver quit successfully.")
        except Exception as e:
            logger.error(f"Failed to quit driver ({e})", exc_info=True)


# 테스트 단계별 리포트를 item.rep_setup / item.rep_call / item.rep_teardown로 주입
@pytest.hookimpl(hookwrapper=True, tryfirst=True)   
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

     # 원하면 테스트별 결과 로그도 남길 수 있음 (call 단계만 예시)
    if rep.when == "call":
        logger.info(
            f"[REPORT] {item.name} - outcome={rep.outcome} "
            f"(passed={rep.passed}, failed={rep.failed}, skipped={rep.skipped})"
        )

'''
pytest의 Hook

1. Hook
- pytest는 테스트 실행의 각 단계에서 특정 함수를 불러줄 수 있는 포인트를 제공
- 우리가 직접 작성한 함수를 pytest가 자동으로 실행하면서,
-> 거기서 원하는 동작(로깅, 결과 가공, 스크린샷 등)을 추가

2.pytest_runtest_makereport 훅의 역할
- 이 훅은 각 테스트 함수 실행이 씉난 후 pytest가 생성한 "리포트 객체(report)"를 전달
- 테스트의 단계
    1. setup 단계 : 픽스처/환경 준비
    2. call 단계 : 실제 테스트 함수 실행
    3. teardown 단계 : 뒷정리(드라이버 종료 등)
- pytest는 각 단계별 결과를 rep_setup, rep_call, rep_teardown 형태로 담아줌
- 이 훅을 사용하면, 우리가 실행 중인 테스트 객체(item)에 이 결과들을 속성으로 붙일 수 있음

3. 코드 해석
1) @pytest.hookimpl(hookwrapper=True, tryfirst=True)
- @pytest.hookimpl : pytest가 이 함수를 훅 구현체로 인식하게 만듦
- hookwrapper=True : pytest에 의해 원래 실행될 로직을 감사서 실행할 수 있다
    - 즉, 이 함수 안에서 yield를 하고 나면 pytest가 본래 작업을 하고, 다시 돌아옴
- tryfirst=True : 다른 훅 구현체보다 먼저 실행되도록 순서를 앞당겨 줌

2) def pytest_runtest-makereport(item, call):
- 훅 함수 이름은 반드시 pytest_runtest_makereport여야 pytest가 알아봄
- item : 지금 실행 중인 테스트 함수 객체 (메타 데이터 들어있음)
- call : 현재 실행 중인 단계(estup, call, teardown)에 대한 정보

3) outcome = yield
- yield는 "pytest, 너 원래 할 일 다 하고 와"라는 뜻
- pytest가 실제 테스트를 실행하고, 그 결과(outcome)를 우리에게 돌려줌

4) rep = outcome.get_result()
- outcome.get_result() -> 리포트 객체(TestReport)를 반환
- 이 안에는 when, failed, passed, skipped 같은 정보가 들어있다
- ex) rep.failed == true (실패) /  rep.when == "call" (테스트 본문 실행 단게 결과)

5) setattr(item, "rep_" + rep.when, rep)
- setattr : 객체에 동적으로 속성을 추가하는 함수
- item 객체에 "rep_" + rep.when 이름으로 rep을 붙임
    - setup 단계 -> item.rep_setup = rep
    - call 단계 -> item.rep_call = rep
    - teardown 단계 -> item.rep_teardown = rep

4. 참고 문헌 
- https://velog.io/@jaewan/Pytestfixture%EC%99%80-scope
'''