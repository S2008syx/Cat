import { useState, useRef } from "react";
import { searchPlaces } from "../api";

export default function BirthForm({ onSubmit, loading }) {
  const [name, setName] = useState("");
  const [birthDate, setBirthDate] = useState("1990-01-15");
  const [birthTime, setBirthTime] = useState("06:30");

  // Place search state
  const [placeQuery, setPlaceQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedPlace, setSelectedPlace] = useState(null);
  const searchTimeout = useRef(null);

  // Debounced search triggered on input change
  const handlePlaceQueryChange = (value) => {
    setPlaceQuery(value);
    setSelectedPlace(null);
    clearTimeout(searchTimeout.current);
    if (!value.trim()) {
      setSuggestions([]);
      return;
    }
    searchTimeout.current = setTimeout(async () => {
      const results = await searchPlaces(value);
      setSuggestions(results);
      setShowSuggestions(true);
    }, 300);
  };

  const handleSelectPlace = (place) => {
    const [lng, lat] = place.location.split(",").map(Number);
    setSelectedPlace({
      name: place.name,
      district: place.district,
      lng,
      lat,
      utcOffset: Math.round(lng / 15),
    });
    setPlaceQuery(place.district ? `${place.district} ${place.name}` : place.name);
    setShowSuggestions(false);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedPlace) return;
    onSubmit({
      name: name || "匿名",
      birthDate,
      birthTime,
      longitude: selectedPlace.lng,
      latitude: selectedPlace.lat,
      utcOffset: selectedPlace.utcOffset,
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

      <div className="form-field place-field">
        <label>出生地点</label>
        <input
          type="text"
          value={placeQuery}
          onChange={(e) => handlePlaceQueryChange(e.target.value)}
          onFocus={() => suggestions.length > 0 && setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
          placeholder="输入城市名称搜索，如：上海、北京、New York"
          autoComplete="off"
        />
        {showSuggestions && suggestions.length > 0 && (
          <ul className="place-suggestions">
            {suggestions.map((s, i) => (
              <li key={i} onMouseDown={() => handleSelectPlace(s)}>
                <strong>{s.name}</strong>
                {s.district && <span className="suggestion-district">{s.district}</span>}
              </li>
            ))}
          </ul>
        )}
        {selectedPlace && (
          <span className="place-hint">
            {selectedPlace.name} — 经度 {selectedPlace.lng.toFixed(4)}° / 纬度 {selectedPlace.lat.toFixed(4)}° (UTC{selectedPlace.utcOffset >= 0 ? "+" : ""}{selectedPlace.utcOffset})
          </span>
        )}
        {!selectedPlace && placeQuery && (
          <span className="place-hint">请从搜索结果中选择一个地点</span>
        )}
      </div>

      <button type="submit" disabled={loading || !selectedPlace}>
        {loading ? "计算中..." : "生成图表"}
      </button>
    </form>
  );
}
