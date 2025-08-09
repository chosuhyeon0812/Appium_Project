# 1. Skyscanner 앱 실행 확인

from datetime import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from time import sleep

# Desired capabilities 설정
desired_caps = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "R3CN30QEK1W", 
    "appPackage": "net.skyscanner.android.main",  
    "noReset": True
}

#UiAutomator2Options 객체로 변환
options = UiAutomator2Options().load_capabilities(desired_caps)

# Appium 서버에 연결
driver = webdriver.Remote("http://localhost:4723", options=options)

# 앱이 로드될 때까지 대기
sleep(3)
driver.quit()
