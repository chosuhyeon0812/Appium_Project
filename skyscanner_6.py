# 6. 서울 - 어디든지 동작 확인

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction

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
    # 1. '검색' 탭 클릭
    search_element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("검색")'))
    )
    search_element.click()
    print("✅ '검색' 탭 클릭 완료")

    # 2. '어디든지 검색' 선택
    anywhere_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("net.skyscanner.android.main:id/card_background").instance(0)'))
    )
    anywhere_element.click()
    print("✅ '어디든지 검색' 선택 완료")

    # 3. '서울 - 어디든지' 선택
    seoul_anywhere_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("net.skyscanner.android.main:id/informativeContent")'))
    )
    seoul_anywhere_element.click()
    print("✅ '서울 - 어디든지' 선택 완료")

    # 4. '어디든지' 선택
    anywhere_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("net.skyscanner.android.main:id/originCardView").instance(1)'))
    )
    anywhere_element.click()
    print("✅ '어디든지' 선택 완료")

    # 5. '도착지 국가,도시 또는 공항' 선택
    destination_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("searchModalTextField")'))
    )
    destination_element.click()
    print("✅ '도착지 국가,도시 또는 공항' 선택 완료")

    # 6. '방콕' 입력
    destination_element.send_keys("방콕").click()
    print("✅ '방콕' 입력 완료")

    # 7. 목록에서 '방콕 (모두)' 선택
    
    # '방콕' 검색 후 결과 리스트 전부 가져오기
    # '방콕 (모두)' 항목을 찾기 위해 모든 TextView 요소를 가져옴
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((AppiumBy.CLASS_NAME, "android.widget.TextView"))
    )

    # 원하는 항목 찾기
    for el in elements:
        text = el.text
        if "방콕 (모두)" in text:
            el.click()
            print("✅ '방콕 (모두)' 클릭 완료")
            break
        destination_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(4)'))
        )

    # 8. '날짜 지정 안 함' 선택
    date_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("net.skyscanner.android.main:id/departureDate")'))
    )
    date_element.click()
    print("✅ '날짜 지정 안 함' 선택 완료")

    # 9.'8월' 선택
    august_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("MonthCell8월")'))
    )
    august_element.click()
    print("✅ '8월' 선택 완료")

    # 10. '계속' 버튼 선택
    continue_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").instance(3)'))
    )
    continue_button.click()
    print("✅ '계속' 버튼 클릭 완료")

    # 11. '검색' 버튼 선택
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.LinearLayout").instance(8)'))
    )
    search_button.click()
    print("✅ '검색' 버튼 선택 완료")

except Exception as e:
    print("오류 발생:", e)
    
finally:
    driver.quit()