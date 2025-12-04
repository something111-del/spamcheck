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

        let data;
        const contentType = res.headers.get("content-type");
        if (contentType && contentType.indexOf("application/json") !== -1) {
            data = await res.json();
        } else {
            const text = await res.text();
            throw new Error(`Server returned non-JSON response: ${res.status} ${res.statusText}\n${text.substring(0, 100)}...`);
        }

        let result = document.getElementById("result");

        if (!res.ok) {
            throw new Error(data.error || `Server error: ${res.status}`);
        }

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
