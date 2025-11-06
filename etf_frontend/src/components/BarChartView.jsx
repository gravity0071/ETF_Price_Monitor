import React from "react";
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
} from "recharts";
import "./BarChartView.css"

const BarChartView = ({data}) => {
    return (
        <div className="bar-chart-container">
            <h3 className="bar-chart-title">Top 5 Holdings</h3>
            <ResponsiveContainer>
                <BarChart data={data} margin={{ top: 10, right: 20, left: 10, bottom: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="symbol" />
                    <YAxis />
                    <Tooltip
                        formatter={(value) => value.toFixed(2)}
                        contentStyle={{
                            backgroundColor: "rgba(0,0,0,0.75)",
                            color: "#fff",
                        }}
                    />
                    <Bar
                        dataKey="holding_value"
                        fill="#007aff"
                        radius={[6, 6, 0, 0]}
                    />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default BarChartView;