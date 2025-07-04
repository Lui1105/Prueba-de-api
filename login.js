// login.js
document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    console.log("Formulario enviado por http");
    const result = await response.json();
    const messageDiv = document.getElementById('message');
    if (response.ok) {
        messageDiv.style.color = 'green';
        messageDiv.textContent = result.message;
    } else {
        messageDiv.style.color = '#d8000c';
        messageDiv.textContent = result.error;
    }
});