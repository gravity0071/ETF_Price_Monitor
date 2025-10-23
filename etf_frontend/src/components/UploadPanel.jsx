import React, { useState } from "react";
import axios from "axios";

const UploadPanel = ({ onUploaded }) => {
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => setFile(e.target.files[0]);

    const handleUpload = async () => {
        if (!file) return alert("Please select an ETF CSV file first.");
        const formData = new FormData();
        formData.append("file", file);

        const days = 90;

        try {
            const res = await axios.post(`http://127.0.0.1:8000/upload?days=${days}`, formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            onUploaded?.(res.data);
        } catch (err) {
            console.error(err);
            alert("Upload failed. Please check your server connection.");
        }
    };

    return (
        <div style={{ textAlign: "center", width: "100%" }}>
            <h4 style={{ margin: "0 0 8px" }}>Upload ETF CSV</h4>
            <input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                style={{ width: "100%", marginBottom: "8px" }}
            />
            <button
                onClick={handleUpload}
                style={{
                    width: "100%",
                    height: 36,
                    border: "none",
                    borderRadius: 8,
                    background: "#007aff",
                    color: "#fff",
                    fontWeight: 600,
                    cursor: "pointer",
                    transition: "background 0.2s ease",
                }}
                onMouseOver={(e) => (e.target.style.background = "#0066d6")}
                onMouseOut={(e) => (e.target.style.background = "#007aff")}
            >
                Upload
            </button>
        </div>
    );
};

export default UploadPanel;