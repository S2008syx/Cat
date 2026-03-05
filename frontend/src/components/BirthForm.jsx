import { useState } from "react";

const EXAMPLE_PLACES = [
  { label: "上海", lng: 121.4737, lat: 31.2304, utcOffset: 8 },
  { label: "北京", lng: 116.4074, lat: 39.9042, utcOffset: 8 },
  { label: "纽约", lng: -74.006, lat: 40.7128, utcOffset: -5 },
  { label: "伦敦", lng: -0.1276, lat: 51.5074, utcOffset: 0 },
  { label: "东京", lng: 139.6917, lat: 35.6895, utcOffset: 9 },
];

export default function BirthForm({ onSubmit, loading }) {
  const [name, setName] = useState("");
  const [birthDate, setBirthDate] = useState("1990-01-15");
  const [birthTime, setBirthTime] = useState("06:30");
  const [placeIdx, setPlaceIdx] = useState(0);

  const place = EXAMPLE_PLACES[placeIdx];

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      name: name || "匿名",
      birthDate,
      birthTime,
      longitude: place.lng,
      latitude: place.lat,
      utcOffset: place.utcOffset,
    });
  };

  return (
    <form className="birth-form" onSubmit={handleSubmit}>
      <h2>出生信息</h2>

      <div className="form-field">
        <label>姓名</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="输入姓名（可选）"
        />
      </div>

      <div className="form-field">
        <label>出生日期</label>
        <input
          type="date"
          value={birthDate}
          onChange={(e) => setBirthDate(e.target.value)}
          required
        />
      </div>

      <div className="form-field">
        <label>出生时间</label>
        <input
          type="time"
          value={birthTime}
          onChange={(e) => setBirthTime(e.target.value)}
          required
        />
      </div>

      <div className="form-field">
        <label>出生地点</label>
        <select value={placeIdx} onChange={(e) => setPlaceIdx(Number(e.target.value))}>
          {EXAMPLE_PLACES.map((p, i) => (
            <option key={p.label} value={i}>
              {p.label} (UTC{p.utcOffset >= 0 ? "+" : ""}{p.utcOffset})
            </option>
          ))}
        </select>
        <span className="place-hint">
          经度 {place.lng}° / 纬度 {place.lat}°
        </span>
        <p className="form-note">
          Demo 模式：从预设城市选择。正式版将接入高德地图搜索。
        </p>
      </div>

      <button type="submit" disabled={loading}>
        {loading ? "计算中..." : "生成图表"}
      </button>
    </form>
  );
}
