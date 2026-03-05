/**
 * Text report panel — displays words data from API.
 */

function Section({ title, children }) {
  return (
    <div className="report-section">
      <h4>{title}</h4>
      {children}
    </div>
  );
}

function Tag({ label, value }) {
  return (
    <div className="report-tag">
      <span className="tag-label">{label}</span>
      <span className="tag-value">{value}</span>
    </div>
  );
}

function ActivationTable({ activations }) {
  if (!activations) return null;
  const { personality = [], design = [] } = activations;

  return (
    <div className="activation-table-wrapper">
      <table className="activation-table">
        <thead>
          <tr>
            <th colSpan={3} className="at-header-design">设计 (潜意识)</th>
            <th className="at-header-planet">星体</th>
            <th colSpan={3} className="at-header-personality">个性 (意识)</th>
          </tr>
          <tr>
            <th>闸门名</th>
            <th>爻</th>
            <th>闸门</th>
            <th></th>
            <th>闸门</th>
            <th>爻</th>
            <th>闸门名</th>
          </tr>
        </thead>
        <tbody>
          {personality.map((p, i) => {
            const d = design[i] || {};
            return (
              <tr key={i}>
                <td className="at-name at-design-cell">{d.gate_name_zh || "-"}</td>
                <td className="at-line at-design-cell">{d.line ?? "-"}</td>
                <td className="at-gate at-design-cell">{d.gate ?? "-"}</td>
                <td className="at-planet">{p.planet_zh}</td>
                <td className="at-gate at-personality-cell">{p.gate ?? "-"}</td>
                <td className="at-line at-personality-cell">{p.line ?? "-"}</td>
                <td className="at-name at-personality-cell">{p.gate_name_zh || "-"}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default function ReportPanel({ wordsData, inputData }) {
  if (!wordsData) return null;

  const { type_info, authority_info, profile_info, definition_info, cross_info, center_infos, channel_infos, gate_infos, activations } = wordsData;

  return (
    <div className="report-panel">
      <h3>{inputData?.name || "匿名"} 的人类图报告</h3>
      <p className="report-subtitle">
        {inputData?.birth_date} {inputData?.birth_time}
      </p>

      {/* Overview */}
      <Section title="基本信息">
        <div className="tag-grid">
          <Tag label="类型" value={`${type_info.name_zh} (${type_info.key})`} />
          <Tag label="策略" value={type_info.strategy || "-"} />
          <Tag label="权威" value={`${authority_info.name_zh} (${authority_info.key})`} />
          <Tag label="人生角色" value={`${profile_info.key} ${profile_info.name_zh}`} />
          <Tag label="定义" value={definition_info.name_zh} />
          <Tag label="轮回交叉" value={cross_info.name_zh} />
        </div>
      </Section>

      {/* Activation Table */}
      <Section title="星体激活表">
        <ActivationTable activations={activations} />
      </Section>

      {/* Type description */}
      <Section title="类型描述">
        <p>{type_info.description}</p>
      </Section>

      {/* Authority */}
      <Section title="权威">
        <p>{authority_info.description}</p>
      </Section>

      {/* Profile */}
      <Section title="人生角色">
        <p>{profile_info.description}</p>
        <div className="tag-grid">
          <Tag label={`第${profile_info.line1?.number}爻`} value={profile_info.line1?.name_zh} />
          <Tag label={`第${profile_info.line2?.number}爻`} value={profile_info.line2?.name_zh} />
        </div>
      </Section>

      {/* Centers */}
      <Section title="能量中心">
        <div className="center-list">
          {center_infos.map((c) => (
            <div key={c.id} className={`center-item ${c.defined ? "defined" : "undefined"}`}>
              <strong>{c.name_zh}</strong>
              <span className={`center-badge ${c.defined ? "badge-on" : "badge-off"}`}>
                {c.defined ? "已定义" : "未定义"}
              </span>
              <p className="center-theme">{c.theme}</p>
              {!c.defined && <p className="center-noself">非自我主题: {c.not_self_theme}</p>}
            </div>
          ))}
        </div>
      </Section>

      {/* Channels */}
      <Section title={`已激活通道 (${channel_infos.length})`}>
        {channel_infos.length === 0 ? (
          <p>无已激活通道</p>
        ) : (
          <div className="channel-list">
            {channel_infos.map((ch, i) => (
              <div key={i} className="channel-item">
                <strong>{ch.gates.join("-")} {ch.name_zh}</strong>
                <span className="channel-en">{ch.name_en}</span>
                <p>{ch.theme}</p>
              </div>
            ))}
          </div>
        )}
      </Section>

      {/* Gates */}
      <Section title={`已激活闸门 (${gate_infos.length})`}>
        <div className="gate-list">
          {gate_infos.map((g) => (
            <div key={g.gate} className="gate-item">
              <span className="gate-num">Gate {g.gate}</span>
              <strong>{g.name_zh}</strong>
              <span className="gate-en">{g.name_en}</span>
              <p className="gate-keynote">{g.keynote}</p>
              <div className="gate-activations">
                {g.activated_by.map((a, i) => (
                  <span key={i} className={`activation-badge ${a.side}`}>
                    {a.side === "personality" ? "个性" : "设计"} · {a.planet} · 第{a.line}爻
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </Section>
    </div>
  );
}
