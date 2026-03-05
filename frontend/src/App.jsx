import { useState } from "react";
import BirthForm from "./components/BirthForm";
import Bodygraph from "./components/Bodygraph";
import ReportPanel from "./components/ReportPanel";
import { fetchChart } from "./api";
import "./App.css";

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

  return (
    <div className="app">
      <header className="app-header">
        <h1>人类图计算器</h1>
        <p>Human Design Chart Calculator</p>
      </header>

      <main className="app-main">
        <div className="input-section">
          <BirthForm onSubmit={handleSubmit} loading={loading} />
        </div>

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
        <p>Demo 版本 — 使用模拟数据 · Cat Project</p>
      </footer>
    </div>
  );
}
