import React, { useState, useMemo } from "react";
import "./TableView.css";

function TableView({ data, title = "Holdings Table" }) {
    const [sortConfig, setSortConfig] = useState({ key: null, direction: null });

    const handleSort = (key) => {
        let direction = "asc";
        if (sortConfig.key === key && sortConfig.direction === "asc") {
            direction = "desc";
        }
        setSortConfig({ key, direction });
    };

    const sortedData = useMemo(() => {
        if (!sortConfig.key) return data;
        return [...data].sort((a, b) => {
            if (["weight", "latest_price"].includes(sortConfig.key)) {
                return sortConfig.direction === "asc"
                    ? a[sortConfig.key] - b[sortConfig.key]
                    : b[sortConfig.key] - a[sortConfig.key];
            }
            return 0;
        });
    }, [data, sortConfig]);

    const getArrow = (key) => {
        if (sortConfig.key !== key) return "↕";
        return sortConfig.direction === "asc" ? "▲" : "▼";
    };

    if (!Array.isArray(data) || data.length === 0) {
        return <p className="table-empty">No table data available</p>;
    }

    return (
        <div className="table-container">
            <h3 className="table-title">{title}</h3>
            <table className="styled-table">
                <thead>
                <tr>
                    <th>Symbol</th>
                    <th
                        onClick={() => handleSort("weight")}
                        className={`sortable ${sortConfig.key === "weight" ? "active" : ""}`}
                    >
                        Weight <span className="arrow">{getArrow("weight")}</span>
                    </th>
                    <th
                        onClick={() => handleSort("latest_price")}
                        className={`sortable ${sortConfig.key === "latest_price" ? "active" : ""}`}
                    >
                        Latest Price <span className="arrow">{getArrow("latest_price")}</span>
                    </th>
                </tr>
                </thead>
                <tbody>
                {sortedData.map((row, idx) => (
                    <tr key={idx}>
                        <td>{row.symbol}</td>
                        <td>{(row.weight * 100).toFixed(2)}%</td>
                        <td>${row.latest_price.toFixed(2)}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}

export default TableView;