const API_URL = ""; // Use relative path for production

async function predict() {
    let text = document.getElementById("smsInput").value.trim();
    if (!text) return alert("Enter a message!");

    try {
        let res = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        let data = await res.json();
        let result = document.getElementById("result");

        if (data.error) {
            result.style.color = "orange";
            result.innerHTML = "⚠ Error: " + data.error;
            return;
        }

        if (data.prediction === "spam") {
            result.style.color = "#d60606";
            result.innerHTML = "🔥 SPAM";
        } else {
            result.style.color = "#0a7f00";
            result.innerHTML = "✔ HAM (Not Spam)";
        }
    } catch (err) {
        alert("Failed to connect to server: " + err);
    }
}
