import { useState } from "react";
import BirthForm from "./components/BirthForm";
import Bodygraph from "./components/Bodygraph";
import ReportPanel from "./components/ReportPanel";
import { fetchChart } from "./api";
import mockData from "./mock_data.json";
import "./App.css";

const DEMO_MODE = !import.meta.env.VITE_API_URL;

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchChart(formData);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectExample = (id) => {
    const example = mockData.find((d) => d.id === id);
    if (example) setResult(example);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>人类图计算器</h1>
        <p>Human Design Chart Calculator</p>
      </header>

      <main className="app-main">
        {DEMO_MODE ? (
          <div className="demo-section">
            <div className="demo-notice">
              静态 Demo 模式 — 选择一个示例查看人类图
            </div>
            <div className="demo-selector">
              {mockData.map((d) => (
                <button
                  key={d.id}
                  className={`demo-btn ${result?.id === d.id ? "active" : ""}`}
                  onClick={() => handleSelectExample(d.id)}
                >
                  <strong>{d.input.name}</strong>
                  <span>{d.input.birth_date} {d.input.birth_time}</span>
                  <span className="demo-type">{d.words.type_info.name_zh} · {d.words.profile_info.key}</span>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="input-section">
            <BirthForm onSubmit={handleSubmit} loading={loading} />
          </div>
        )}

        {error && <div className="error-banner">错误: {error}</div>}

        {result && (
          <div className="result-section">
            <div className="result-left">
              <Bodygraph graphData={result.graph} />
              {result.chart_svg && (
                <div className="chart-image-section">
                  <h4>人类图图片</h4>
                  <div dangerouslySetInnerHTML={{ __html: result.chart_svg }} />
                  <button
                    className="chart-download-btn"
                    onClick={() => {
                      const blob = new Blob([result.chart_svg], { type: "image/svg+xml" });
                      const url = URL.createObjectURL(blob);
                      const a = document.createElement("a");
                      a.href = url;
                      a.download = `${result.input?.name || "chart"}_人类图.svg`;
                      a.click();
                      URL.revokeObjectURL(url);
                    }}
                  >
                    下载 SVG 图片
                  </button>
                </div>
              )}
            </div>
            <div className="result-right">
              <ReportPanel wordsData={result.words} inputData={result.input} />
            </div>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>{DEMO_MODE ? "静态 Demo 版本" : "Demo 版本"} — Cat Project</p>
      </footer>
    </div>
  );
}
