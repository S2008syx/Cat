import { useState } from "react";
import BirthForm from "./components/BirthForm";
import ResultPage from "./components/ResultPage";
import { fetchChart } from "./api";
import "./App.css";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (formData) => {
    setLoading(true);
    const data = await fetchChart(formData);
    setResult(data);
    setLoading(false);
  };

  const handleBack = () => {
    setResult(null);
  };

  // Page 2: Result
  if (result) {
    return (
      <div className="app">
        <ResultPage result={result} onBack={handleBack} />
      </div>
    );
  }

  // Page 1: Input
  return (
    <div className="app">
      <div className="input-page">
        <div className="input-page-header">
          <h1>人类图生成器 2</h1>
          <p>Human Design Chart Generator</p>
        </div>

        <BirthForm onSubmit={handleSubmit} loading={loading} />
      </div>

      {loading && (
        <div className="loading-overlay" role="status" aria-live="polite">
          <div className="loading-spinner" />
          <div className="loading-text">正在计算你的人类图...</div>
        </div>
      )}
    </div>
  );
}
