import pytest
from pages.home_page import HomePage

def test_app_launch(driver):
    home = HomePage(driver)
    # 예외 없이 privacy 컨테이너가 잡히면 성공으로 간주
    home.wait_privacy()
    # 더 명확히 하려면 존재 여부를 assert로 표현(옵션)
    # assert home.exists_privacy_container() is True

def test_main_labels(driver):
    home = HomePage(driver)
    home.accept_cookies_if_visible()
    flight, hotel, car = home.labels()

    assert flight == "항공권"
    assert hotel == "호텔"
    assert car == "렌터카"

    # 더 유연하게 하고 싶다면 예
    # assert "항공" in flight
    # assert hotel in ("호텔", "숙소")
    # assert car.replace(" ", "") in ("렌터카", "렌터카예약")
    