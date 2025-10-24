import React, {useState} from "react";
import axios from "axios";
import BarChartView from "./components/BarChartView";
import LineChartView from "./components/LineChartView";
import TableView from "./components/TableView";
import UploadPanel from "./components/UploadPanel";
import "./App.css";

function App() {
    const [data, setData] = useState(null);
    const [sessionId, setSessionId] = useState(null);
    const [chart, setChart] = useState(null);

    const handleUploaded = (respData) => {
        setData(respData);
        setSessionId(respData.session_id);
        setChart(respData.chart);
    };

    const fetchRange = async (days) => {
        if (!sessionId || !(chart && chart.date && chart.date.length)) return;
        const endStr = chart.date[chart.date.length - 1];
        const end = new Date(endStr);
        const start = new Date(end);
        start.setDate(end.getDate() - days + 1);

        const startStr = start.toISOString().slice(0, 10);
        const endIsoStr = end.toISOString().slice(0, 10);

        try {
            const res = await axios.get("http://127.0.0.1:8000/chart", {
                params: {session_id: sessionId, start: startStr, end: endIsoStr},
            });
            // console.log(res);
            setChart(res.data);
        } catch (e) {
            console.error(e);
            alert("Failed to fetch chart data");
        }
    };

    return (
        <div className="dashboard">
            <div className="line-chart-panel">
                {chart ? (
                    <>
                        <LineChartView chartData={chart}/>
                        <div className="timebar">
                            <button onClick={() => fetchRange(7)}>1W</button>
                            <button onClick={() => fetchRange(30)}>1M</button>
                            <button onClick={() => fetchRange(90)}>3M</button>
                            <button onClick={() => fetchRange(180)}>6M</button>
                            <button onClick={() => fetchRange(365)}>1Y</button>
                        </div>
                    </>
                ) : (
                    <div className="no-chart-warning">Please upload a CSV first</div>
                )}
            </div>

            <div className="table-panel">
                {data? (<TableView data={data.table}/>):(<div className="no-chart-warning">Please upload a CSV first</div>)}
            </div>

            <div className="bar-chart-panel">
                {data?(<BarChartView data={data.top5}/>):(<div className="no-chart-warning">Please upload a CSV first</div>)}
            </div>

            <div className="upload-panel">
                <UploadPanel onUploaded={handleUploaded}/>
            </div>
        </div>
    )
        ;
}

export default App;