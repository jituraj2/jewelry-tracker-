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
    showAlert("✅ Record saved successfully!");

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
    const tbody = document.querySelector("#recordTable tbody");
    tbody.innerHTML = '';

    const records = getRecords();
    if (records.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7">No records found.</td></tr>';
        return;
    }

    records.forEach(record => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${record.jewelryName}</td>
            <td>${record.gram}g</td>
            <td>₹${record.amount}</td>
            <td>${record.purchaseDate}</td>
            <td>${record.shopName}</td>
            <td>
                <img src="${record.jewelryImage}" width="50" />
                <img src="${record.billImage}" width="50" />
            </td>
            <td>
                <button onclick="editRecord('${record.id}')">✏️ Edit</button>
                <button onclick="deleteRecord('${record.id}')">🗑️ Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function editRecord(id) {
    const record = getRecords().find(r => r.id === id);
    if (!record) return;

    document.getElementById('recordId').value = record.id;
    document.getElementById('jewelryName').value = record.jewelryName;
    document.getElementById('gram').value = record.gram;
    document.getElementById('amount').value = record.amount;
    document.getElementById('purchaseDate').value = record.purchaseDate;
    document.getElementById('shopName').value = record.shopName;

    showAlert("✏️ Now editing. Make changes and press Save.");
}

function deleteRecord(id) {
    if (!confirm("Are you sure you want to delete this record?")) return;
    const updated = getRecords().filter(r => r.id !== id);
    localStorage.setItem('jewelryRecords', JSON.stringify(updated));
    loadRecords();
    showAlert("🗑️ Record deleted.");
}

function showAlert(msg) {
    const alertBox = document.getElementById('alert');
    alertBox.textContent = msg;
    alertBox.style.display = 'block';
    setTimeout(() => {
        alertBox.style.display = 'none';
    }, 3000);
}
