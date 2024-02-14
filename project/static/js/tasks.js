document.addEventListener('DOMContentLoaded', () => {
    fetchTasks();
    fetchCompleted();
});

async function fetchCompleted() {
    const response = await fetch('http://localhost:8000/tasks/completed/count')
    const completedCounter = await response.json()
    document.getElementById('completedTasksCount').textContent = completedCounter.completed_tasks_count;
};

async function fetchTasks() {
    const response = await fetch('http://localhost:8000/tasks/');
    const tasks = await response.json();
    const tasksList = document.getElementById('tasksList');
    tasksList.innerHTML = ''; // Wyczyść listę przed ponownym załadowaniem
    tasks.forEach(task => {
        if(!task.completed) {
            let li = document.createElement('li');

            // Nazwa zadania z możliwością edycji
            let taskSpan = document.createElement('span');
            taskSpan.textContent = task.name;
            taskSpan.className = 'task-name';
            li.appendChild(taskSpan);

            // Przycisk do edycji nazwy zadania
            let editButton = document.createElement('button');
            editButton.textContent = '✏️';
            editButton.className = 'edit-task-btn';
            editButton.onclick = () => editTaskName(task.id, taskSpan);
            li.appendChild(editButton);

            // Przycisk do zatwierdzania zadania
            let completeButton = document.createElement('button');
            completeButton.textContent = '✔️';
            completeButton.className = 'complete-task-btn';
            completeButton.onclick = () => completeTask(task.id);
            li.appendChild(completeButton);

            // Przycisk do usuwania zadania
            let deleteButton = document.createElement('button');
            deleteButton.textContent = '❌';
            deleteButton.className = 'delete-task-btn';
            deleteButton.onclick = () => deleteTask(task.id);
            li.appendChild(deleteButton);

            tasksList.appendChild(li);
        }
    });
}

async function addTask() {
    const taskInput = document.getElementById('taskInput');
    const task = taskInput.value;
    if (task) {
        await fetch('http://localhost:8000/tasks/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({name: task})
        });
        taskInput.value = '';
        fetchTasks(); // Odśwież listę zadań
    }
}

function editTaskName(taskId, taskSpan) {
    let taskInput = document.getElementById('taskInput');
    let addTaskButton = document.getElementById('addTaskButton');
    let confirmEditButton = document.getElementById('confirmEdit');

    // Ustaw placeholder na "Edit task name:" podczas edycji
    taskInput.placeholder = "Edit task name:";
    taskInput.value = taskSpan.textContent;
    addTaskButton.style.display = 'none';
    confirmEditButton.style.display = 'inline';

    confirmEditButton.onclick = async () => {
        if (taskInput.value !== taskSpan.textContent) {
            await updateTaskName(taskId, taskInput.value);
            taskSpan.textContent = taskInput.value;
        }

        // Przywróć UI do stanu początkowego
        taskInput.value = '';
        taskInput.placeholder = "Add a new task"; // Zmień placeholder z powrotem na "Add a new task"
        addTaskButton.style.display = 'inline';
        confirmEditButton.style.display = 'none';
    };
}

async function updateTaskName(taskId, newName) {
    await fetch(`http://localhost:8000/tasks/${taskId}/update`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({name: newName})
    });
    fetchTasks(); // Można pominąć, jeśli aktualizacja na froncie jest wystarczająca
}

async function completeTask(taskId) {
    await fetch(`http://localhost:8000/tasks/${taskId}/complete`, {
        method: 'PUT'
    });
    fetchTasks();
    fetchCompleted();// Odśwież listę zadań
}

async function deleteTask(taskId) {
    await fetch(`http://localhost:8000/tasks/${taskId}`, {
        method: 'DELETE'
    });
    fetchTasks(); // Odśwież listę zadań
}