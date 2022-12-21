from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


ERROR_LIMIT_REQUESTS = "Превышен лимит (5) неудачных попыток ввода пароля. Повторите попытку через 10 минут"
ERROR_DATA = ""
ERROR_TIMEOUT = "timeout error"


class ParserEtis:
    def __init__(self):
        option = Options()
        option.add_argument("--headless")
        self.driver: WebDriver = webdriver.Chrome(options=option)

    def service(self, email: str, password: str):
        if (not email) or (not password):
            return {"status": "error", "description": ERROR_DATA + 33}

        res_login = self.__login(email, password)
        if res_login["status"] == "error":
            return res_login

        cookie = res_login["description"]
        self.driver.add_cookie({'domain': 'student.psu.ru', 'name': 'session_id', 'value': cookie['value'], 'sameSite': 'Strict'})

        res_weeks = self.__get_weeks()
        if res_weeks["status"] == "error":
            return res_weeks

        weeks = res_weeks["description"]
        schedule_weeks = {}
        for i in range(1, len(weeks) + 1):
            res_schedule = self.__get_week_schedule(str(i))

            if res_schedule["status"] == "error":
                return res_schedule
            schedule_weeks[i] = res_schedule["description"]

        self.driver.get('https://student.psu.ru/pls/stu_cus_et/stu.logout')
        self.driver.delete_cookie('session_id')
        return schedule_weeks

    def __login(self, email: str, password: str):
        self.driver.get('https://student.psu.ru/pls/stu_cus_et/stu.login')

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "form"))
            )
        except TimeoutException:
            return {"status": "error", "description": ERROR_TIMEOUT}

        self.driver.find_element(By.ID, 'login').send_keys(email + Keys.RETURN)
        self.driver.find_element(By.ID, 'password').send_keys(password + Keys.RETURN)
        self.driver.find_element(By.ID, 'sbmt').click()

        try:
            error = WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error_message"))
            )
            if error.text == ERROR_LIMIT_REQUESTS:
                return {"status": "error", "description": ERROR_LIMIT_REQUESTS}
            else:
                return {"status": "error", "description": ERROR_DATA + "80"}
        except TimeoutException:
            pass

        cookie = self.driver.get_cookie('session_id')
        return {"status": "ok", "description": cookie}

    def __get_weeks(self):
        self.driver.get('https://student.psu.ru/pls/stu_cus_et/stu.timetable')
        try:
            WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, "timetable"))
            )
        except TimeoutException:
            return {"status": "error", "description": ERROR_TIMEOUT}

        weeks = self.driver.find_elements(By.CLASS_NAME, "week")
        return {"status": "ok", "description": weeks}

    def __get_week_schedule(self, num_week: str):
        self.driver.get(f'https://student.psu.ru/pls/stu_cus_et/stu.timetable?p_cons=y&p_week={num_week}')

        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "timetable"))
            )
        except TimeoutException:
            return {"status": "error", "description": ERROR_TIMEOUT}

        days = self.driver.find_elements(By.CLASS_NAME, "day")
        schedule_week = {}
        for day in days:
            date: str = day.find_element(By.TAG_NAME, "h3").text
            info: List[WebElement] = day.find_elements(By.TAG_NAME, "tr")

            schedule_day = {}
            for pair in info:
                num_date_pair = pair.find_element(By.CLASS_NAME, "pair_num").text.split("\n")
                num_pair, time_pair = num_date_pair[0], num_date_pair[1]

                info_pair = pair.find_element(By.CLASS_NAME, "pair_info").text.split("\n")

                if len(info_pair) == 4:
                    del info_pair[info_pair.index("оценить занятие")]
                    teacher, title, auditorium = info_pair[0], info_pair[1], info_pair[2]
                else:
                    teacher, title, auditorium = "-", "-", "-"

                schedule_day[num_pair] = {
                    "time": time_pair,
                    "title": title,
                    "teacher": teacher,
                    "auditorium": auditorium
                }

            schedule_week[date] = schedule_day
        return {"status": "ok", "description": schedule_week}