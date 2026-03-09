/**
 * Result page — displays bodygraph (left) and text info (right).
 */
import Bodygraph from "./Bodygraph";
import ReportPanel from "./ReportPanel";

export default function ResultPage({ result, onBack }) {
  const { graph, words, input, chart_svg } = result;

  const typeInfo = words?.type_info || {};
  const authorityInfo = words?.authority_info || {};
  const profileInfo = words?.profile_info || {};
  const definitionInfo = words?.definition_info || {};
  const crossInfo = words?.cross_info || {};

  const handleDownload = () => {
    if (!chart_svg) return;
    const blob = new Blob([chart_svg], { type: "image/svg+xml" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${input?.name || "chart"}_人类图.svg`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="result-page">
      {/* Header bar */}
      <div className="result-header">
        <button className="back-btn" onClick={onBack} aria-label="返回输入页">
          ← 返回
        </button>
        <div className="result-header-info">
          <h2>{input?.name || "匿名"} 的人类图</h2>
          <p>{input?.birth_date} {input?.birth_time}</p>
        </div>
      </div>

      {/* Main content */}
      <div className="result-content">
        {/* Left: Bodygraph */}
        <div className="result-left">
          {chart_svg ? (
            <div className="chart-container">
              <div dangerouslySetInnerHTML={{ __html: chart_svg }} />
              <div className="chart-actions">
                <button className="download-btn" onClick={handleDownload}>
                  下载 SVG
                </button>
              </div>
            </div>
          ) : graph ? (
            <Bodygraph graphData={graph} />
          ) : (
            <div className="chart-container" style={{ textAlign: "center", padding: "80px 0", color: "#6b8bb5" }}>
              图表生成中...
            </div>
          )}
        </div>

        {/* Right: Text info */}
        <div className="result-right">
          <div className="info-panel">
            <div className="info-panel-title">基本信息</div>

            {/* Type */}
            <div className="info-card">
              <div className="info-card-label">类型 Type</div>
              <div className="info-card-value">{typeInfo.name_zh || "-"}</div>
              <div className="info-card-sub">{typeInfo.key || ""}</div>
            </div>

            {/* Strategy + Authority */}
            <div className="info-grid">
              <div className="info-card">
                <div className="info-card-label">策略 Strategy</div>
                <div className="info-card-value">{typeInfo.strategy_zh || typeInfo.strategy || "-"}</div>
              </div>
              <div className="info-card">
                <div className="info-card-label">内在权威 Authority</div>
                <div className="info-card-value">{authorityInfo.name_zh || "-"}</div>
                <div className="info-card-sub">{authorityInfo.key || ""}</div>
              </div>
            </div>

            {/* Profile + Definition */}
            <div className="info-grid">
              <div className="info-card">
                <div className="info-card-label">人生角色 Profile</div>
                <div className="info-card-value">{profileInfo.key || "-"}</div>
                <div className="info-card-sub">{profileInfo.name_zh || ""}</div>
              </div>
              <div className="info-card">
                <div className="info-card-label">定义 Definition</div>
                <div className="info-card-value">{definitionInfo.name_zh || "-"}</div>
              </div>
            </div>

            {/* Not-self theme */}
            <div className="info-card not-self">
              <div className="info-card-label">非自我主题 Not-Self Theme</div>
              <div className="info-card-value">{typeInfo.not_self || "-"}</div>
            </div>

            {/* Incarnation Cross */}
            <div className="info-card cross">
              <div className="info-card-label">化身十字 Incarnation Cross</div>
              <div className="info-card-value">{crossInfo.name_zh || "-"}</div>
              <div className="info-card-sub">{crossInfo.name_en || ""}</div>
            </div>
          </div>

          {/* Detailed report */}
          <ReportPanel wordsData={words} inputData={input} />
        </div>
      </div>
    </div>
  );
}
