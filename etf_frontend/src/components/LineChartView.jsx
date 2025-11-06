import React, {useEffect, useRef} from "react";
import * as echarts from "echarts";
import "./LineChartView.css";

const LineChartView = ({chartData}) => {
    const chartRef = useRef(null);

    useEffect(() => {
        if (!chartData || !chartData.etf_price?.length) return;

        const chartDom = chartRef.current;
        const myChart = echarts.init(chartDom);

        const firstPrice = chartData.etf_price[0];
        const lastPrice = chartData.etf_price[chartData.etf_price.length - 1];
        const isUp = lastPrice > firstPrice;
        const lineColor = isUp ? "#16c784" : "#ea3943"; // green ↑ or red ↓

        const option = {
            title: {
                text: "ETF Price Trend",
                left: "center",
                top: 10,
                textStyle: {
                    fontSize: 16,
                    fontWeight: 600,
                    color: "#333",
                },
            },
            tooltip: {
                trigger: "axis",
                formatter: (params) => {
                    const p = params[0];
                    return `${p.axisValue}<br/>Price: ${p.value.toFixed(3)}`;
                },
                backgroundColor: "rgba(50, 50, 50, 0.9)",
                textStyle: {color: "#fff", fontSize: 12},
                axisPointer: {type: "cross"},
            },
            grid: {
                top: 50,
                left: 50,
                right: 40,
                bottom: 40,
            },
            xAxis: {
                type: "category",
                boundaryGap: false,
                data: chartData.date,
                axisLabel: {
                    fontSize: 10,
                    rotate: 30,
                    color: "#555",
                },
                axisLine: {lineStyle: {color: "#ccc"}},
            },
            yAxis: {
                type: "value",
                scale: true,
                axisLabel: {
                    formatter: (value) => `$${value}`,
                    color: "#555",
                },
                splitLine: {
                    lineStyle: {color: "#eee"},
                },
            },
            dataZoom: [
                {
                    type: "inside",
                    zoomOnMouseWheel: true,
                    moveOnMouseMove: true,
                    moveOnMouseWheel: false,
                    throttle: 40,
                },
            ],
            series: [
                {
                    name: "ETF Price",
                    type: "line",
                    smooth: false,
                    data: chartData.etf_price,
                    lineStyle: {
                        width: 2,
                        color: lineColor,
                    },
                    symbol: "circle",
                    symbolSize: 3,
                    itemStyle: {
                        color: lineColor,
                    },
                    emphasis: {
                        focus: "series",
                        scale: 1.7,
                    },
                },
            ],
            animation: true,
            animationDuration: 700,
            animationEasing: "quadraticOut",
        };

        myChart.setOption(option);

        const handleResize = () => {
            requestAnimationFrame(() => {
                if (myChart && !myChart.isDisposed()) myChart.resize();
            });
        };
        window.addEventListener("resize", handleResize);

        return () => {
            window.removeEventListener("resize", handleResize);
            myChart.dispose();
        };
    }, [chartData]);

    return <div ref={chartRef} className="line-chart-container"/>;
};

export default LineChartView;