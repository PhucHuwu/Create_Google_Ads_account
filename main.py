import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import threading
import os
import pandas as pd
import pyautogui
import config
import click
import submit
from proxy_manager import ChromeProxy


driver_lock = threading.Lock()

if not os.path.exists('Account_id.csv'):
    data = {
        'ID': [],
        'Name': [],
        'Country': [],
        'Timezone': [],
        'Currency': [],
        'Proxy': []
    }
    df = pd.DataFrame(data)
    df.to_csv('Account_id.csv', index=False)
    print("File excel vừa được tạo, vui lòng thêm ID vào file excel")
    print("*Lưu ý: 1 ID sẽ là 1 luồng, nhập tối đa 10 ID và các ID phải khác nhau")
    time.sleep(10)
    exit()

df = pd.read_csv('Account_id.csv')
list_account_id = df["ID"].dropna().values.tolist()
list_name = df["Name"].dropna().values.tolist()
list_country = df["Country"].dropna().values.tolist()
list_timezone = df["Timezone"].dropna().values.tolist()
list_money = df["Currency"].dropna().values.tolist()
list_proxy = df["Proxy"].dropna().values.tolist()

confirmation_received = threading.Event()


def create_account(num_accounts, idx, account_id, name, country, timezone, money, proxy):
    options = uc.ChromeOptions()
    profile_directory = f"Profile_{idx + 1}"
    lst = proxy.split(":")

    if not os.path.exists(profile_directory):
        os.makedirs(profile_directory)

    driver = None

    proxy = ChromeProxy(
        idx=idx,
        host=lst[0],
        port=lst[1],
        username=lst[2],
        password=lst[3]
    )

    extension_path = proxy.create_extension()

    with driver_lock:
        options.user_data_dir = profile_directory
        try:
            driver = uc.Chrome(options=options)
        except Exception:
            print(f"Lỗi 1 ở luồng {idx + 1}")
            time.sleep(180)
            exit()

        screen_size = pyautogui.size()
        screen_width = screen_size.width
        screen_height = screen_size.height
        num_windows = len(list_account_id)

        num_cols = num_windows
        num_rows = 1
        window_width = screen_width // num_cols
        window_height = screen_height // num_rows // 2
        driver.set_window_size(window_width, window_height)

        row = idx // num_cols
        col = idx % num_cols
        x_position = col * window_width // 2
        y_position = window_height
        driver.set_window_position(x_position, y_position)

    driver.get("https://ads.google.com/aw/account/new")
    confirmation_received.wait()

    for NUM in range(num_accounts):
        driver.get("https://ads.google.com/aw/account/new")
        time.sleep(config.wait)

        try:
            click.auto_click(driver, "//span[text()='" + account_id + "']", 30)
        except Exception:
            print(f"Lỗi 2 ở luồng {idx + 1}")
            continue

        time.sleep(5)
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "input-area")))
            input_areas = driver.find_elements(By.CLASS_NAME, "input-area")
            if len(input_areas) > 1:
                input_areas[1].send_keys(f'{name}_{NUM + 1}_{datetime.now().strftime("%H:%M")}')
            else:
                time.sleep(config.wait)
                input_areas[1].send_keys(f'{name}_{NUM + 1}_{datetime.now().strftime("%H:%M")}')
        except Exception:
            print(f"Lỗi 3 ở luồng {idx + 1}")
            continue

        # country -----------------------------------------------------------------------------------------------------
        try:
            driver.find_element(By.XPATH, '/html/body/div[1]/root/div/div[1]/div[2]/div/div[3]/div/div/awsm-child-content/content-main/div/div/mcc-root/base-root/div/div[2]/div[1]/view-loader/new-account-view/mcc-create-account-stepper/div/ess-stepper/material-stepper/div[2]/div/step-loader/account-creation-step/div/div[1]/material-expansionpanel[3]/div/div[2]/div/div[1]/div/div/span[2]/country-select/material-dropdown-select/dropdown-button/div').click()
        except Exception:
            print(f"Lỗi 4 ở luồng {idx + 1}")
            continue

        time.sleep(config.wait)
        country_xpath = f"//material-select-dropdown-item[span[text()='{country}']]"
        try:
            click.auto_click(driver, country_xpath, 3)
        except Exception:
            print(f"Lỗi 5 ở luồng {idx + 1}")
            continue

        # timezone ----------------------------------------------------------------------------------------------------
        time.sleep(3)

        try:
            driver.find_element(By.XPATH, '/html/body/div[1]/root/div/div[1]/div[2]/div/div[3]/div/div/awsm-child-content/content-main/div/div/mcc-root/base-root/div/div[2]/div[1]/view-loader/new-account-view/mcc-create-account-stepper/div/ess-stepper/material-stepper/div[2]/div/step-loader/account-creation-step/div/div[1]/material-expansionpanel[4]/div/div[2]/div/div[1]/div/div/span[2]/time-zone-select/material-dropdown-select/dropdown-button/div/material-icon/i').click()
        except Exception:
            print(f"Lỗi 6 ở luồng {idx + 1}")
            continue

        timezone_xpath = f"//material-select-dropdown-item[span[text()='{timezone}']]"
        try:
            click.auto_click(driver, timezone_xpath, 3)
        except Exception:
            print(f"Lỗi 7 ở luồng {idx + 1}")
            continue
        # money -------------------------------------------------------------------------------------------------------
        time.sleep(config.wait)

        try:
            driver.find_element(By.XPATH, '/html/body/div[1]/root/div/div[1]/div[2]/div/div[3]/div/div/awsm-child-content/content-main/div/div/mcc-root/base-root/div/div[2]/div[1]/view-loader/new-account-view/mcc-create-account-stepper/div/ess-stepper/material-stepper/div[2]/div/step-loader/account-creation-step/div/div[1]/material-expansionpanel[5]/div/div[2]/div/div[1]/div/div/span[2]/currency-select/material-dropdown-select/dropdown-button').click()
        except Exception:
            print(f"Lỗi 8 ở luồng {idx + 1}")
            continue
        
        time.sleep(config.wait)
        money_xpath = f"//material-select-dropdown-item[span[text()='{money}']]"
        try:
            click.auto_click(driver, money_xpath, 3)
        except Exception:
            print(f"Lỗi 9 ở luồng {idx + 1}")
            continue
        # -------------------------------------------------------------------------------------------------------------

        driver.switch_to.default_content()

        print(f"Đang giải Captcha của luồng {idx + 1}")
        submit.submit_form(driver)

        try:
            click.auto_click(driver, config.save_button_xpath, 30)
        except Exception:
            print(f"Lỗi 10 ở luồng {idx + 1}")
            continue

        if NUM == 0:
            confirm = input(f"Hãy xác nhận danh tính của luồng {idx + 1}, nếu đã xác nhận danh tính rồi thì nhấn 'ok': ")
            if confirm.lower():
                time.sleep(15)
                print(f"Đã tạo xong {NUM + 1} tài khoản của luồng {idx + 1}")
        else:
            time.sleep(15)
            print(f"Đã tạo xong {NUM + 1} tài khoản của luồng {idx + 1}")


threads = []

num_accounts_per_thread = int(input("Nhập số lượng tài khoản cần tạo: "))

if num_accounts_per_thread:
    for idx, (id, name, country, timezone, money, proxy) in enumerate(zip(list_account_id, list_name, list_country, list_timezone, list_money, list_proxy)):
        thread = threading.Thread(target=create_account, args=(num_accounts_per_thread, idx, id, name, country, timezone, money, proxy))
        thread.start()
        time.sleep(2)
        threads.append(thread)

    start_program = input("Nhập 'ok' để bắt đầu quá trình tự động hóa: ")
    if start_program.lower() == "ok":
        confirmation_received.set()
else:
    print("Số lượng tài khoản không hợp lệ")

for thread in threads:
    thread.join()
