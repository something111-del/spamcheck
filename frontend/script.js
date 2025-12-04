const API_URL = ""; // Use relative path for production

async function predict() {
    let text = document.getElementById("smsInput").value.trim();
    if (!text) return alert("Enter a message!");

    let res = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    let data = await res.json();

    let result = document.getElementById("result");

    if (data.prediction === "spam") {
        result.style.color = "#d60606";
        result.innerHTML = "🔥 SPAM";
    } else {
        result.style.color = "#0a7f00";
        result.innerHTML = "✔ HAM (Not Spam)";
    }
}
