# 2. skyscanner 로그인 실행 확인

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
import re

desired_caps = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "R3CN30QEK1W",
    "appPackage": "net.skyscanner.android.main",
    "appActivity": "net.skyscanner.shell.ui.activity.SplashActivity",
    "noReset": True
}

options = UiAutomator2Options().load_capabilities(desired_caps)
driver = webdriver.Remote("http://localhost:4723", options=options)
driver.implicitly_wait(5)

try:
    # 1. '프로필' 탭 클릭
    profile_element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("프로필")'))
    )
    profile_element.click()

    # 2. 로그인 버튼 클릭
    login_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ID, "net.skyscanner.android.main:id/profileLoginButton"))
    )
    login_btn.click()

    # 3. 'Google' 로그인 버튼 클릭
    google_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Google")'))
    )
    google_btn.click()


    # 4. 첫 번째 스위치 동의 (위치 정보로 클릭하는 방식) // new UiSelector().className("android.view.View").instance(2)
    # agree_switch1 = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(2)'))
    # )
    # agree_switch1.click()

    # 첫 번째 스위치 (개인정보 처리방침 동의)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("개인정보 처리방침")'))
    ).click()
    print("✅ 첫 번째 스위치 클릭 완료")

     # 두 번째 스위치 좌표로 클릭
    # switch2 = WebDriverWait(driver, 10).until(
    # EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,
    #     'new UiSelector().className("android.view.View").instance(4)'))
    # )
    # bounds_text = switch2.get_attribute("bounds")
    # match = re.findall(r'\d+', bounds_text)
    # x1, y1, x2, y2 = map(int, match)
    # x = (x1 + x2) // 2
    # y = (y1 + y2) // 2
    # print(f"터치 좌표: ({x}, {y})")

    # TouchAction(driver).tap(x=x, y=y).perform()
    # print("✅ 두 번째 스위치 터치 성공")

    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,
    #         'new UiSelector().textContains("서비스 약관")'))
    # ).click()
    # print("✅ 두 번째 스위치 클릭 완료")
    # element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
    # 'new UiSelector().textContains("본인은 만 16세 이상이며 서비스 약관에 동의합니다")')
    # element.find_element(AppiumBy.XPATH, "..").click()
 
    # 5. 두 번째 스위치 동의 (위치 정보로 클릭하는 방식) // new UiSelector().className("android.view.View").instance(4) - 여기서 계속 오류 발생
    agree_switch2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(4)'))
    )
    agree_switch2.click()

    # 6. 파란색 '동의' 버튼 클릭
    agree_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("동의")'))
    )
    agree_button.click()


except Exception as e:
    print("오류 발생:", e)

finally:
    driver.quit()
