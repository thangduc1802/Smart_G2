const BASE_URL = "http://127.0.0.1:5001";

console.log("JavaScript geladen!");

// 📌 Registrierung eines neuen Users
function register() {
    console.log("Registrierung gestartet...");

    fetch(`${BASE_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            email: document.getElementById("reg_email").value,
            password: document.getElementById("reg_password").value,
            zip_code: document.getElementById("reg_zip").value
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Antwort erhalten:", data);
        alert(data.message);
        if (data.message === "Registrierung erfolgreich!") {
            window.location.href = "login.html"; // Weiterleitung nach erfolgreicher Registrierung
        }
    })
    .catch(error => {
        console.error("Fehler bei der Registrierung:", error);
        alert("Fehler bei der Registrierung!");
    });
}

// 📌 Login und JWT-Token speichern
function login() {
    console.log("Login gestartet...");

    fetch(`${BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            email: document.getElementById("login_email").value,
            password: document.getElementById("login_password").value
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Antwort erhalten:", data);
        if (data.access_token) {
            localStorage.setItem("jwt", data.access_token);
            alert("Login erfolgreich!");
            window.location.href = "dashboard.html"; // Weiterleitung nach erfolgreichem Login
        } else {
            alert("Login fehlgeschlagen!");
        }
    })
    .catch(error => {
        console.error("Fehler beim Login:", error);
        alert("Fehler beim Login!");
    });
}
