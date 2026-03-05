/**
 * Bodygraph SVG placeholder.
 * Renders 9 centers as shapes + channels as lines using graph data from API.
 * This is a simplified demo — real version will use hdkit SVG template.
 */

const W = 400;
const H = 520;

const CENTER_COLORS = {
  defined: "#f5c542",
  undefined: "#e8e8e8",
};

const CHANNEL_COLORS = {
  personality: "#111",
  design: "#c0392b",
  mixed: "#8e44ad",
};

function centerPos(center) {
  return {
    x: center.position.x * W,
    y: center.position.y * H,
  };
}

function CenterShape({ center }) {
  const { x, y } = centerPos(center);
  const fill = center.defined ? CENTER_COLORS.defined : CENTER_COLORS.undefined;
  const stroke = center.defined ? "#b8860b" : "#aaa";
  const size = 24;

  let shape;
  if (center.shape === "triangle") {
    const points = `${x},${y - size} ${x - size},${y + size * 0.7} ${x + size},${y + size * 0.7}`;
    shape = <polygon points={points} fill={fill} stroke={stroke} strokeWidth={2} />;
  } else if (center.shape === "diamond") {
    const points = `${x},${y - size} ${x + size},${y} ${x},${y + size} ${x - size},${y}`;
    shape = <polygon points={points} fill={fill} stroke={stroke} strokeWidth={2} />;
  } else {
    shape = (
      <rect
        x={x - size * 0.8}
        y={y - size * 0.8}
        width={size * 1.6}
        height={size * 1.6}
        fill={fill}
        stroke={stroke}
        strokeWidth={2}
      />
    );
  }

  return (
    <g>
      {shape}
      <text
        x={x}
        y={y + 3}
        textAnchor="middle"
        fontSize={9}
        fontWeight="bold"
        fill="#333"
      >
        {center.name_zh}
      </text>
    </g>
  );
}

function ChannelLine({ channel, centersMap }) {
  const a = centersMap[channel.center_a];
  const b = centersMap[channel.center_b];
  if (!a || !b) return null;
  const posA = centerPos(a);
  const posB = centerPos(b);
  const color = CHANNEL_COLORS[channel.color] || "#999";

  return (
    <line
      x1={posA.x}
      y1={posA.y}
      x2={posB.x}
      y2={posB.y}
      stroke={color}
      strokeWidth={3}
      strokeLinecap="round"
      opacity={0.7}
    />
  );
}

export default function Bodygraph({ graphData }) {
  if (!graphData) return null;

  const centersMap = {};
  for (const c of graphData.centers) {
    centersMap[c.id] = c;
  }

  return (
    <div className="bodygraph-container">
      <h3>人体图 Bodygraph</h3>
      <svg viewBox={`0 0 ${W} ${H}`} width={W} height={H}>
        {/* Channels (lines behind centers) */}
        {graphData.channels.map((ch, i) => (
          <ChannelLine key={i} channel={ch} centersMap={centersMap} />
        ))}
        {/* Centers */}
        {graphData.centers.map((c) => (
          <CenterShape key={c.id} center={c} />
        ))}
        {/* Legend */}
        <g transform={`translate(10, ${H - 50})`}>
          <rect x={0} y={0} width={12} height={12} fill={CENTER_COLORS.defined} stroke="#b8860b" strokeWidth={1} />
          <text x={16} y={10} fontSize={10} fill="#666">已定义</text>
          <rect x={0} y={18} width={12} height={12} fill={CENTER_COLORS.undefined} stroke="#aaa" strokeWidth={1} />
          <text x={16} y={28} fontSize={10} fill="#666">未定义</text>
          <line x1={80} y1={6} x2={100} y2={6} stroke="#111" strokeWidth={2} />
          <text x={104} y={10} fontSize={10} fill="#666">个性</text>
          <line x1={80} y1={24} x2={100} y2={24} stroke="#c0392b" strokeWidth={2} />
          <text x={104} y={28} fontSize={10} fill="#666">设计</text>
        </g>
      </svg>
      <p className="bodygraph-note">简化 Demo 图 — 正式版将使用 hdkit SVG 模板</p>
    </div>
  );
}
