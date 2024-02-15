import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    # Initialize a Chrome WebDriver and navigate to the local test application.
    driver = webdriver.Chrome()
    driver.get('http://localhost:8000')
    yield driver  # Yield control to the test function.
    driver.quit()  # Quit the WebDriver after test execution.

def test_add_task(driver):
    # Locate the task input and add button elements.
    task_input = driver.find_element(By.ID, "taskInput")
    add_button = driver.find_element(By.ID, "addTaskButton")
    # Input a new task and click the add button.
    task_input.send_keys("Task")
    add_button.click()
    # Locate the tasks list element.
    tasks_list = driver.find_element(By.ID, "tasksList")

    # Verify the new task is added to the tasks list.
    assert "Task" in tasks_list.text, "Added task should appear in the tasks list."

def test_complete_task(driver):
    # Locate and click the complete task button.
    button = driver.find_element(By.CLASS_NAME, "complete-task-btn")
    button.click()
    # Locate the completed tasks counter element.
    counter = driver.find_element(By.ID, "completedTasksCount").text

    # Verify the completed tasks counter is incremented.
    assert int(counter) == 1, "Completed tasks counter should be 1 after completing a task."

def test_add_more_tasks(driver):
    # Locate the task input and add button elements.
    task_input = driver.find_element(By.ID, "taskInput")
    add_button = driver.find_element(By.ID, "addTaskButton")

    # Add multiple tasks.
    for i in range(1, 4):
        task_input.send_keys(f"Task {i}")
        add_button.click()
        task_input.clear()  # Clear the input for the next task.

    # Locate all task list items.
    tasks = driver.find_elements(By.CSS_SELECTOR, "#tasksList li")
    number_of_tasks = len(tasks)

    # Verify the number of tasks added matches the expected count.
    assert number_of_tasks == 3, f"Expected 3 tasks, but found {number_of_tasks}"

def test_delete_two_firsts_tasks(driver):
    # Delete the first two tasks.
    for _ in range(2):
        delete_buttons = driver.find_elements(By.CLASS_NAME, "delete-task-btn")
        delete_buttons[0].click()
        time.sleep(1)  # Wait for the task deletion to complete.

    # Locate remaining tasks and the completed tasks counter.
    tasks = driver.find_elements(By.CSS_SELECTOR, "#tasksList li")
    tasks_list = driver.find_element(By.ID, "tasksList")
    counter = driver.find_element(By.ID, "completedTasksCount").text

    # Verify only one task remains and it is the correct task.
    assert len(tasks) == 1, "Only one task should remain after deleting two."
    assert "Task 3" in tasks_list.text, "The remaining task should be 'Task 3'."
    assert int(counter) == 1, "Completed tasks counter should remain 1."

def test_change_task_name(driver):
    # Locate and click the edit button for a task.
    edit_button = driver.find_element(By.CLASS_NAME, "edit-task-btn")
    edit_button.click()
    # Locate the task input, enter the new name, and confirm the change.
    task_input = driver.find_element(By.ID, "taskInput")
    task_input.send_keys("Rename")
    confirm_button = driver.find_element(By.ID, "confirmEdit")
    confirm_button.click()
    # Locate the tasks list element.
    tasks_list = driver.find_element(By.ID, "tasksList")

    # Verify the task name is updated in the tasks list.
    assert "Rename" in tasks_list.text, "The task's name should be updated to 'Rename'."

def test_add_task_and_refresh(driver):
    # Add a new task and refresh the page.
    task_input = driver.find_element(By.ID, "taskInput")
    add_button = driver.find_element(By.ID, "addTaskButton")
    task_input.send_keys("Task")
    add_button.click()
    driver.refresh()
    # Locate all task list items.
    tasks = driver.find_elements(By.CSS_SELECTOR, "#tasksList li")

    # Verify the tasks remain after refreshing the page.
    assert len(tasks) == 2, "Two tasks should be present after adding another task and refreshing."

def test_complete_tasks_and_refresh(driver):
    # Complete all tasks and refresh the page.
    for _ in range(2):
        complete_buttons = driver.find_elements(By.CLASS_NAME, "complete-task-btn")
        complete_buttons[0].click()
        time.sleep(1)  # Wait for the task completion to process.
    driver.refresh()
    # Locate the completed tasks counter.
    counter = driver.find_element(By.ID, "completedTasksCount").text

    # Verify the completed tasks count is accurate after refreshing.
    assert int(counter) == 3, "Completed tasks counter should be 3 after completing tasks and refreshing."
