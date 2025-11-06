import React, { useState } from "react";
import axios from "axios";

const UploadPanel = ({ onUploaded, sessionId, setSessionId }) => {
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {setFile(e.target.files[0]);console.log(e)}

    const handleUpload = async () => {
        if (!file) return alert("Please select an ETF CSV file first.");
        const formData = new FormData();
        formData.append("file", file);

        const days = 90;

        try {
            const res = await axios.post(`http://127.0.0.1:8000/upload`, formData,
                {
                    params: {days: days,
                    session_id: sessionId
                    },
                    headers: {"Content-Type": "multipart/form-data"},
                });
            if (onUploaded) {
                onUploaded(res.data);
            }
        } catch (err) {
            console.error(err);

            let msg = "Upload failed. Please check your server connection.";
            if (err.response) {
                if (err.response && err.response.data && err.response.data.detail) {
                    msg = err.response.data.detail;
                } else if (typeof err.response.data === "string") {
                    msg = err.response.data;
                } else {
                    msg = JSON.stringify(err.response.data);
                }
            } else if (err.message) {
                msg = err.message;
            }

            alert(msg);
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