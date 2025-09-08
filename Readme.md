[노션 url](https://perpetual-boar-23b.notion.site/22c5e225ddce80cba9ded66999edd1b3?v=22c5e225ddce8001a2eb000cd81b11fa)

| TC      | 시나리오                            | 주요 Page / 메서드                                                                                                                                                                     |
| ------- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **TC1** | 앱 실행/프라이버시 로드                   | `HomePage.wait_privacy()`, `HomePage.accept_cookies_if_visible()`                                                                                                                 |
| **TC2** | 로그인(Google) 성공                  | `HomePage.accept_cookies_if_visible()` → `LoginPage.select_google_provider()` → `LoginPage.accept_terms_if_present()` → `LoginPage.pick_account()` → `LoginPage.wait_logged_in()` |
| **TC3** | 홈 라벨(항공권/호텔/렌터카) 확인             | `HomePage.skip_marketing_if_visible()`, `HomePage.labels()`                                                                                                                       |
| **TC4** | Drops 탭 진입 및 “Drops 시작하기” 확인    | `NavBar.goto_tab_by_text("Drops")`, `DropsPage.is_get_started_visible()`                                                                                                          |
| **TC5** | Drops 닫기 → 위시리스트 탭 → “위시리스트” 확인 | `DropsPage.close_if_present()`, `NavBar.goto_tab_by_text("위시리스트")`, `WishlistPage.is_header_visible()`                                                                            |
| **TC6** | 검색 플로우(ICN→BKK) 후 결과 8개         | `SearchFlightsPage.open_search_tab() / tap_flights_card() / close_onboarding_if_present() / pick_departure_icn() / pick_arrival_bkk() / click_search() / count_result_cards()`    |
