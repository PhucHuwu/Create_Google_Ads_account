import requests


WEBSITE_KEY = '6LfWyjkmAAAAAJfv7tBe1VBeQ6MQzVuYD2nKl5jE'


def submit_form(driver):
    data = {
        "key": "cafe0fde8073bf6f61797a4cc10167f1",
        "type": "recaptchav2",
        "googlesitekey": WEBSITE_KEY,
        "pageurl": driver.current_url,
    }
    try:
        token = requests.post(url="https://autocaptcha.pro/apiv3/process", json=data).json().get("captcha")
    except Exception as e:
        print("Lỗi khi giải Captcha", e)

    if token:
        driver.execute_script("""
        let Url_Str = window.location.href;\n
        Callback_Reqd = 0;\n
        let list0 = ___grecaptcha_cfg.clients\n
        Callback_Str = ''\n
        for (let item1 of Object.keys(list0))\n
        \t  {\n
        \t  let list1 = ___grecaptcha_cfg.clients[item1]\n
        \t  for (let item2 of Object.keys(list1))\n
        \t\t    {\n
        \t\t    let list2 = ___grecaptcha_cfg.clients[item1][item2];\n
        \t\t    for (let item3 of Object.keys(list2))\n
        \t\t\t      {\n
        \t\t\t      let list3 = ___grecaptcha_cfg.clients[item1][item2][item3];\n
        \t\t\t      if (!(typeof list3 === 'object' && list3 !== null)) { continue; }\n
        \t\t\t      if (!('sitekey' in list3)) { continue; }\n
        \t\t\t      if (!('sitekey' in list3 && 'callback' in list3)) { continue; }\n
        \t\t\t      Callback_Str = list3;\n
        \t\t\t      Callback_StrVal = '___grecaptcha_cfg.clients[' + item1 + '].' + item2 + '.' + item3;\n
        \t\t\t      break;\n
        \t\t\t      }\n
        \t\t    if (!(Callback_Str === '')) {break;}\n
        \t\t        }\n
        \t  if (!(Callback_Str === '')) {break;}\n
        \t  }\n
        """)
        data_callback = driver.execute_script("return Callback_StrVal")
        driver.execute_script(data_callback + ".callback('" + token + "')")
    elif token == False:
        print("Lỗi giải Captcha")
