async function fetchTasks() {
    const res = await fetch('/api/tasks');
    const data = await res.json();
    const container = document.getElementById('tasks');
    container.innerHTML = '';

    data.forEach(task => {
        const div = document.createElement('div');
        div.className = `task ${task.completed ? 'completed' : ''}`;

        div.innerHTML = `
            <div>
                <strong>${task.title}</strong> - ${task.description}
                <span class="${task.priority === 'High' ? 'priority-high' : 'priority-medium'}">
                    [${task.priority}]
                </span>
            </div>
            <div>
                <button onclick="toggleComplete(${task.id}, ${!task.completed})">${task.completed ? 'Undo' : '✓'}</button>
                <button onclick="deleteTask(${task.id})">🗑</button>
            </div>
        `;
        container.appendChild(div);
    });
}

async function addTask() {
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;

    if (!title.trim()) {
        alert("Please enter a task title!");
        return;
    }

    await fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description })
    });

    document.getElementById('title').value = '';
    document.getElementById('description').value = '';
    fetchTasks();
}

async function toggleComplete(id, completed) {
    await fetch(`/api/tasks/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed })
    });
    fetchTasks();
}

async function deleteTask(id) {
    await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
    fetchTasks();
}

fetchTasks();
