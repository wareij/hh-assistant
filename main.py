from selenium import webdriver
import time
import os.path
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pickle
from config import login, password


url = "https://samara.hh.ru/"

options = webdriver.FirefoxOptions()
options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0")
options.set_preference("dom.webnotifications.enabled", False)
# Режим работы в фоне
#options.headless = True
driver = webdriver.Firefox(executable_path="hh-assistant\\geckodriver.exe", options=options)

# Функция нажатия на кнопку поднятия резюме в поиске
def cv_lifter():
    time.sleep(3)
    update_button = driver.find_element(By.XPATH, "/html/body/div[6]/div/div[1]/div[4]/div/div/div/div[1]/div[3]/div[2]/div/div[6]/div/div/div/div[1]/span/button")
    update_button.click()  
          
while True:
    try:
        # Данный код срабатывает при первом запуске/откутствии cookie в папке проекта
        if os.path.isfile("hh-assistant\\cookies") == False:    
            driver.get(url=(url + "account/login?backurl=%2F"))    
            time.sleep(3)
            # Нажимаем на кнопку "Войти с паролем"
            p_buttom = driver.find_element(By.XPATH, "/html/body/div[6]/div/div[1]/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div/form/div[4]/span")
            p_buttom.click()
            time.sleep(2)
            # Вводим логин
            username_input = driver.find_element(By.XPATH, "/html/body/div[6]/div/div[1]/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/form/div[1]/input")
            username_input.send_keys(login)
            # Вводим пароль
            password_input = driver.find_element(By.CLASS_NAME, "bloko-input_password")
            password_input.send_keys(password)
            time.sleep(2)
            password_input.send_keys(Keys.ENTER)
            time.sleep(3)        
            # Сохраняем cookie в папку проекта
            pickle.dump(driver.get_cookies(), open("hh-assistant\\cookies", "wb"))
            # Открываем страницу "Мои резюме"
            driver.get(url=(url + "applicant/resumes?hhtmFrom=main&hhtmFromLabel=header"))

            cv_lifter()
        # Данный код срабатывает при наличии cookie в папке проекта
        else:    
            driver.get(url=(url + "applicant/resumes?hhtmFrom=main&hhtmFromLabel=header"))    
            time.sleep(3)
            # Передаем cookie сайту
            for cookie in pickle.load(open("hh-assistant\\cookies", "rb")):
                driver.add_cookie(cookie)            
            driver.refresh() 

            cv_lifter()

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()
    
    time.sleep(14400)