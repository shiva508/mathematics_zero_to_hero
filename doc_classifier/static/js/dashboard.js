
const API_BASE = "";

async function apiRequest(url, options = {}) {
    const response = await fetch(`${API_BASE}${url}`, options);

    if (!response.ok) {
        const message = await response.text();
        throw new Error(message || `Request failed: ${response.status}`);
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
}

function showMessage(elementId, message, isError = false) {
    const element = document.getElementById(elementId);

    element.textContent = message;
    element.style.color = isError ? "#b91c1c" : "#166534";
}

async function loadDashboard() {
    try {
        const [shipments, invoices] = await Promise.all([
            apiRequest("/shipments"),
            apiRequest("/invoices")
        ]);

        renderShipments(shipments);
        renderInvoices(invoices);

        document.getElementById("shipment-count").textContent =
            shipments.length;

        document.getElementById("invoice-count").textContent =
            invoices.length;

    } catch (error) {
        console.error(error);
        alert(`Unable to load dashboard: ${error.message}`);
    }
}

function renderShipments(shipments) {
    const table = document.getElementById("shipment-table");
    const shipmentSelect = document.getElementById("shipment-id");

    table.replaceChildren();

    shipmentSelect.replaceChildren();

    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Select a shipment";
    shipmentSelect.appendChild(defaultOption);

    if (!shipments.length) {
        const row = table.insertRow();
        const cell = row.insertCell();

        cell.colSpan = 5;
        cell.textContent = "No shipments found.";

        return;
    }

    for (const shipment of shipments) {
        const row = table.insertRow();

        [
            shipment.id,
            shipment.awb,
            shipment.origin,
            shipment.destination,
            shipment.status
        ].forEach(value => {
            const cell = row.insertCell();
            cell.textContent = value ?? "";
        });

        const option = document.createElement("option");
        option.value = shipment.id;
        option.textContent = `${shipment.awb} — ${shipment.origin} to ${shipment.destination}`;

        shipmentSelect.appendChild(option);
    }
}

function renderInvoices(invoices) {
    const table = document.getElementById("invoice-table");

    table.replaceChildren();

    if (!invoices.length) {
        const row = table.insertRow();
        const cell = row.insertCell();

        cell.colSpan = 4;
        cell.textContent = "No invoices uploaded.";

        return;
    }

    for (const invoice of invoices) {
        const row = table.insertRow();

        [
            invoice.id,
            invoice.shipment_id ?? "",
            invoice.original_filename,
            invoice.uploaded_at ?? ""
        ].forEach(value => {
            const cell = row.insertCell();
            cell.textContent = value ?? "";
        });
    }
}

document.getElementById("shipment-form").addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        const form = event.currentTarget;
        const formData = new FormData(form);

        const payload = {
            awb: formData.get("awb"),
            origin: formData.get("origin"),
            destination: formData.get("destination"),
            status: formData.get("status")
        };

        try {
            await apiRequest("/shipments", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            showMessage("shipment-message", "Shipment created successfully.");

            form.reset();
            await loadDashboard();

        } catch (error) {
            showMessage(
                "shipment-message",
                `Unable to create shipment: ${error.message}`,
                true
            );
        }
    }
);

document.getElementById("invoice-form").addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        const form = event.currentTarget;
        const formData = new FormData(form);

        if (!formData.get("shipment_id")) {
            showMessage("invoice-message", "Please select a shipment.", true);
            return;
        }

        try {
            await apiRequest("/invoices/upload", {
                method: "POST",
                body: formData
            });

            showMessage("invoice-message", "Invoice uploaded successfully.");

            form.reset();
            await loadDashboard();

        } catch (error) {
            showMessage(
                "invoice-message",
                `Unable to upload invoice: ${error.message}`,
                true
            );
        }
    }
);

document.getElementById("invoice-file").addEventListener(
    "change",
    event => {
        const file = event.target.files[0];

        if (file && !file.name.toLowerCase().endsWith(".pdf")) {
            showMessage(
                "invoice-message",
                "Please select a PDF file.",
                true
            );

            event.target.value = "";
        }
    }
);

document.addEventListener("DOMContentLoaded", loadDashboard);