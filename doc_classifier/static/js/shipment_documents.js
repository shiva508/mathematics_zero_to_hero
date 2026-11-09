async function loadShipmentDocuments() {
    const tbody = document.getElementById("documents-table");
    const message = document.getElementById("documents-message");

    tbody.innerHTML = `
        <tr>
            <td colspan="5">Loading documents...</td>
        </tr>
    `;

    try {
        const response = await fetch(
            `/api/shipments/${encodeURIComponent(shipmentAwb)}/documents`
        );

        if (!response.ok) {
            throw new Error("Failed to load shipment documents.");
        }

        const result = await response.json();
        const documents = result.documents || [];

        tbody.innerHTML = "";

        if (documents.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5">
                        No documents uploaded for this shipment.
                    </td>
                </tr>
            `;
            return;
        }


        documents.forEach((invoice) => {
            const row = document.createElement("tr");

            const idCell = document.createElement("td");
            idCell.textContent = invoice.id;

            const filenameCell = document.createElement("td");
            filenameCell.textContent = invoice.original_filename;

            const sizeCell = document.createElement("td");
            sizeCell.textContent =
                `${(invoice.file_size / 1024).toFixed(2)} KB`;

            const uploadedCell = document.createElement("td");
            uploadedCell.textContent = invoice.uploaded_at || "";

            const actionsCell = document.createElement("td");

            const downloadLink = document.createElement("a");
            downloadLink.href = `/invoices/${invoice.id}/download`;
            downloadLink.textContent = "Download";
            downloadLink.className = "awb-link";

            actionsCell.appendChild(downloadLink);

            row.append(
                idCell,
                filenameCell,
                sizeCell,
                uploadedCell,
                actionsCell
            );

            tbody.appendChild(row);
        });


    } catch (error) {
        console.error(error);

        tbody.innerHTML = `
            <tr>
                <td colspan="5">Unable to load documents.</td>
            </tr>
        `;

        message.textContent = error.message;
    }
}

document.addEventListener(
    "DOMContentLoaded",
    loadShipmentDocuments
);