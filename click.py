import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def auto_click(driver, xpath, time):
    button = WebDriverWait(driver, time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    if button.is_displayed() and button.is_enabled():
        button.click()
        return

# def auto_fill(driver, xpath, input_text):
#     try:
#         input_field = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, xpath))
#         )
#         input_field.clear()
#         input_field.send_keys(input_text)
#     except Exception as e:
#         print("Lỗi khi nhập dữ liệu")
