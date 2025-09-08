# Home 화면을 자동화하기 위한 Page Object 클래스
# 테스트 코드에서 화면 조작(클릭/대기/텍스트 읽기)을 이 클래스로 캡슐화한다

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    def __init__(self, driver, timeout=10):
        """
        생성자 (인스턴스 초기화)
        :param driver: 이미 생성된 Appium WebDriver 인스턴스
        :param timeout: 명시적 대기 기본 타임아웃(초)
        """
        self.d = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_privacy(self):
        """
        개인정보/쿠키 배너 컨테이너가 DOM에 나타날 때까지 대기
        - 화면이 완전히 로드되기 전에 조작하면 실패하기 쉬워서 동기화 용도로 사용
        """
        self.wait.until(                        # 'until'은 조건이 참이 될 때까지 대기
            EC.presence_of_element_located(     # 요소가 DOM에 존재하면 통과(펴시 여부오 무관)
                (AppiumBy.ID, "net.skyscanner.android.main:id/privacy_policy_container")
                # locator는 (By, 값) 형태의 '튜플'이어야 한다
            )
        )

    def accept_cookies_if_visible(self):
        """
        쿠키/프라이버시 배너가 '있으면' 수락 버튼을 누른다
        - 없으면 아무것도 하지 않고 False 반환(예외 안 던짐)
        :return: 클릭했다면 True, 아니면 False
        """

        els = self.d.find_elements(         # 여러 개(또는 0개) 찾기: 없으면 []
            AppiumBy.ID,
            "net.skyscanner.android.main:id/privacy_policy_accept_button"
        )
        if els:                             # 요소가 하나라도 있으면
            els[0].click()                  # 첫 번째 버튼 클릭
            return True
        return False                        # 없으면 아무 작업 없이 False

    def bottom_tab(self, label_text: str):
        """
        하단 탭바에서 특정 라벨 텍스트를 가진 탭을 클릭한다.
        - 다국어 환경에선 @text가 바뀔 수 있으니 가능하면 resource-id/desc 기반 대안을 권장
        """
        
        xpath = (
            '//android.widget.TextView'
            '[@resource-id="net.skyscanner.android.main:id/'
            navigation_bar_item_small_label_view" and @text="%s"]' % label_text
        )
        # 하단 탭: 라벨 텍스트로 찾기 (다국어면 다른 locator 권장)
        el = self.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath))
        )
        el.click()

    def labels(self):
        """
        홈 화면의 Flights/Hotels/Carhire 라벨 텍스트를 읽어 튜플로 반환한다
        - 반환: (flight, hotel, car)
        """
        # 홈의 3개 라벨 텍스트 반환
        flight = self.d.find_element(
            AppiumBy.ID,
            "net.skyscanner.android.main:id/home_flights_text"
        ).text.strip()

        hotel = self.d.find_element(
            AppiumBy.ID,
            "net.skyscanner.android.main:id/home_hotels_text"
        ).text.strip()

        car = self.d.find_element(
            AppiumBy.ID,
            "net.skyscanner.android.main:id/home_carhire_text"
        ).text.strip()

        return flight, hotel, car
