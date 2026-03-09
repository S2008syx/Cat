import { useState, useEffect, useRef } from "react";
import { searchPlaces } from "../api";

export default function BirthForm({ onSubmit, loading }) {
  const [name, setName] = useState("");
  const [birthDate, setBirthDate] = useState("1990-01-15");
  const [birthTime, setBirthTime] = useState("06:30");

  const [placeQuery, setPlaceQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedPlace, setSelectedPlace] = useState(null);
  const searchTimeout = useRef(null);

  useEffect(() => {
    if (!placeQuery.trim()) {
      setSuggestions([]);
      return;
    }
    clearTimeout(searchTimeout.current);
    searchTimeout.current = setTimeout(async () => {
      const results = await searchPlaces(placeQuery);
      setSuggestions(results);
      setShowSuggestions(true);
    }, 300);
    return () => clearTimeout(searchTimeout.current);
  }, [placeQuery]);

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
    <form className="form-card" onSubmit={handleSubmit}>
      <div className="form-field">
        <label>姓名</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="请输入你的名字"
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
          onChange={(e) => {
            setPlaceQuery(e.target.value);
            setSelectedPlace(null);
          }}
          onFocus={() => suggestions.length > 0 && setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
          placeholder="输入城市名搜索，如：上海、北京"
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
            {selectedPlace.name} — {selectedPlace.lng.toFixed(2)}°E / {selectedPlace.lat.toFixed(2)}°N (UTC+{selectedPlace.utcOffset})
          </span>
        )}
        {!selectedPlace && placeQuery && (
          <span className="place-hint">请从搜索结果中选择一个地点</span>
        )}
      </div>

      <button type="submit" className="submit-btn" disabled={loading || !selectedPlace}>
        {loading ? "计算中..." : "生成人类图"}
      </button>
    </form>
  );
}
