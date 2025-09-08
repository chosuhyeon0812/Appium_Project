# 5. 하단 영역 선택 > Drops

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
    # 1. 'Drops' 탭 클릭
    profile_element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Drops")'))
    )
    profile_element.click()
    print("✅ 'Drops' 탭 클릭 완료")


except Exception as e:
    print("오류 발생:", e)

finally:
    driver.quit()
