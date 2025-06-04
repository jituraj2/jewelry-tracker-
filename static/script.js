document.addEventListener('DOMContentLoaded', loadRecords);

document.getElementById('jewelryForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const id = document.getElementById('recordId').value || Date.now().toString();
    const existing = getRecords().filter(rec => rec.id !== id);

    const jewelryImage = await getImageBase64('jewelryImage');
    const billImage = await getImageBase64('billImage');

    const record = {
        id,
        jewelryName: document.getElementById('jewelryName').value,
        gram: document.getElementById('gram').value,
        amount: document.getElementById('amount').value,
        purchaseDate: document.getElementById('purchaseDate').value,
        shopName: document.getElementById('shopName').value,
        jewelryImage: jewelryImage || getImageFromStorage(id, 'jewelryImage'),
        billImage: billImage || getImageFromStorage(id, 'billImage')
    };

    existing.push(record);
    localStorage.setItem('jewelryRecords', JSON.stringify(existing));
    alert("Record saved!");
    this.reset();
    loadRecords();
});

function getImageBase64(inputId) {
    const file = document.getElementById(inputId).files[0];
    if (!file) return null;
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

function getRecords() {
    return JSON.parse(localStorage.getItem('jewelryRecords')) || [];
}

function getImageFromStorage(id, type) {
    const record = getRecords().find(r => r.id === id);
    return record ? record[type] : null;
}

function loadRecords() {
    const container = document.getElementById('recordList');
    container.innerHTML = '';
    const records = getRecords();

    if (records.length === 0) {
        container.innerHTML = '<p>No records found.</p>';
        return;
    }

    records.forEach(record => {
        const div = document.createElement('div');
        div.className = 'record';
        div.innerHTML = `
            <strong>${record.jewelryName}</strong><br>
            🪙 ${record.gram}g | 💰 ₹${record.amount} | 🗓️ ${record.purchaseDate} <br>
            🏬 ${record.shopName}<br>
            <img src="${record.jewelryImage}" width="100" alt="Jewelry Image">
            <img src="${record.billImage}" width="100" alt="Bill Image"><br>
            <butto
