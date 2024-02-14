import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get('http://localhost:8000')
    yield driver
    driver.quit()

def test_add_task(driver):
    task_input = driver.find_element(By.ID, "taskInput")
    add_button = driver.find_element(By.ID, "addTaskButton")

    task_input.send_keys("Task")
    add_button.click()

    tasks_list = driver.find_element(By.ID, "tasksList")
    assert "Task" in tasks_list.text

def test_complete_task(driver):
    button = driver.find_element(By.XPATH, '//*[@id="tasksList"]/li[1]/button[2]')
    button.click()

    counter = driver.find_element(By.ID, "completedTasksCount").text

    assert int(counter) == 1

def test_add_more_tasks(driver):
    task_input = driver.find_element(By.ID, "taskInput")
    add_button = driver.find_element(By.ID, "addTaskButton")

    for i in range(1, 4):
        task_input.send_keys(f"Task {i}")
        add_button.click()
        task_input.clear()

    tasks = driver.find_elements(By.CSS_SELECTOR, "#tasksList li")
    number_of_tasks = len(tasks)

    assert number_of_tasks == 3, f"Expected 3 tasks, but found {number_of_tasks}"

# usuń 2 pierwsze taski
def test_delete_two_firsts_tasks(driver):
    for _ in range(2):
        delete_buttons = driver.find_elements(By.CLASS_NAME, "delete-task-btn")
        delete_buttons[0].click()
        time.sleep(1)

    tasks = driver.find_elements(By.CSS_SELECTOR, "#tasksList li")
    tasks_list = driver.find_element(By.ID, "tasksList")
    counter = driver.find_element(By.ID, "completedTasksCount").text

    assert len(tasks) == 1
    assert "Task 3" in tasks_list.text
    assert int(counter) == 1

# zmień nazwę id3 task
def test_change_task_name(driver):
    edit_button = driver.find_element(By.XPATH, '//*[@id="tasksList"]/li[1]/button[1]')
    edit_button.click()
    task_input = driver.find_element(By.ID, "taskInput")
    task_input.send_keys("Rename")
    confirm_button = driver.find_element(By.ID, "confirmEdit")
    confirm_button.click()

    tasks_list = driver.find_element(By.ID, "tasksList")
    assert "Rename" in tasks_list.text


# dodaj kolejne zadanie i odświez strone
def test_add_task_and_refresh(driver):
    task_input = driver.find_element(By.ID, "taskInput")
    add_button = driver.find_element(By.ID, "addTaskButton")

    task_input.send_keys("Task")
    add_button.click()
    driver.refresh()

    tasks = driver.find_elements(By.CSS_SELECTOR, "#tasksList li")
    assert len(tasks) == 2

# oznacz 2 zadania jako zrobione
def test_complete_tasks_and_refresh(driver):
    for _ in range(2):
        delete_buttons = driver.find_elements(By.CLASS_NAME, "complete-task-btn")
        delete_buttons[0].click()
        time.sleep(1)
    driver.refresh()

    counter = driver.find_element(By.ID, "completedTasksCount").text

    assert int(counter) == 3