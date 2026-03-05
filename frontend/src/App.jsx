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
