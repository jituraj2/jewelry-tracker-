document.getElementById("jewelryForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const readFileAsBase64 = (file) => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });

    const data = {
        jewelryImage: await readFileAsBase64(document.getElementById("jewelryImage").files[0]),
        name: document.getElementById("jewelryName").value,
        gram: document.getElementById("gram").value,
        amount: document.getElementById("amount").value,
        date: document.getElementById("purchaseDate").value,
        shop: document.getElementById("shopName").value,
        billImage: await readFileAsBase64(document.getElementById("billImage").files[0])
    };

    const key = "my_secret_key_1234567890123456"; // 32 chars for AES-256
    const iv = crypto.getRandomValues(new Uint8Array(12));

    const encoded = new TextEncoder().encode(JSON.stringify(data));
    const cryptoKey = await crypto.subtle.importKey(
        "raw",
        new TextEncoder().encode(key),
        { name: "AES-GCM" },
        false,
        ["encrypt"]
    );

    const encrypted = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, cryptoKey, encoded);

    const record = {
        iv: Array.from(iv),
        encrypted: Array.from(new Uint8Array(encrypted))
    };

    localStorage.setItem("record_" + Date.now(), JSON.stringify(record));
    alert("Saved securely on your device.");
});

