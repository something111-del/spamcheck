const API_URL = ""; // Use relative path for production

console.log("SpamCheck Frontend v1.2 loaded"); // Version check

async function predict() {
    let text = document.getElementById("smsInput").value.trim();
    if (!text) return alert("Enter a message!");

    try {
        let res = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const responseText = await res.text();
        let data;

        try {
            data = JSON.parse(responseText);
        } catch (e) {
            // If JSON parse fails, show the raw text (likely an HTML error page)
            throw new Error(`Server returned invalid JSON. Status: ${res.status}. Response: ${responseText.substring(0, 150)}...`);
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
        alert("Debug Error: " + err.message);
        console.error("Full error:", err);
    }
}
