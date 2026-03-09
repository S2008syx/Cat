import { useState } from "react";
import { searchPlaces } from "../api";

export default function BirthForm({ onSubmit, loading }) {
  const [name, setName] = useState("");
  const [birthDate, setBirthDate] = useState("1990-01-15");
  const [birthTime, setBirthTime] = useState("06:30");

  const [placeQuery, setPlaceQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedPlace, setSelectedPlace] = useState(null);
  const [searchStatus, setSearchStatus] = useState("idle"); // "idle" | "found" | "not_found"
  const [searchMsg, setSearchMsg] = useState("");

  const handleSearch = () => {
    const q = placeQuery.trim();
    if (!q) return;
    setSelectedPlace(null);
    setSearchStatus("idle");
    setSearchMsg("");
    const results = searchPlaces(q);
    setSuggestions(results);
    if (results.length > 0) {
      setShowSuggestions(true);
      setSearchStatus("found");
      setSearchMsg(`找到 ${results.length} 个结果，请点击选择`);
    } else {
      setShowSuggestions(false);
      setSearchStatus("not_found");
      setSearchMsg(`未找到"${q}"，请输入正确的中国城市名（如：北京、上海、广州）`);
    }
  };

  const handleSelectPlace = (place) => {
    const [lng, lat] = place.location.split(",").map(Number);
    setSelectedPlace({
      name: place.name,
      district: place.district,
      lng,
      lat,
      utcOffset: place.utc_offset != null ? place.utc_offset : Math.round(lng / 15),
    });
    setPlaceQuery(place.district ? `${place.district} ${place.name}` : place.name);
    setShowSuggestions(false);
    setSearchMsg("");
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

  const searchBtnClass =
    searchStatus === "found" ? "search-btn found" :
    searchStatus === "not_found" ? "search-btn not-found" :
    "search-btn";

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
        <div className="place-input-row">
          <input
            type="text"
            value={placeQuery}
            onChange={(e) => {
              setPlaceQuery(e.target.value);
              setSelectedPlace(null);
              setSearchStatus("idle");
              setSearchMsg("");
              setShowSuggestions(false);
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                handleSearch();
              }
            }}
            placeholder="输入城市名，如：上海、北京"
            autoComplete="off"
          />
          <button
            type="button"
            className={searchBtnClass}
            onClick={handleSearch}
            disabled={!placeQuery.trim()}
          >
            搜索
          </button>
        </div>
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
        {searchMsg && !selectedPlace && (
          <div className={`place-msg ${searchStatus === "found" ? "place-msg-ok" : "place-msg-err"}`}>
            {searchMsg}
          </div>
        )}
        {selectedPlace && (
          <span className="place-hint">
            {selectedPlace.name} — {Math.abs(selectedPlace.lng).toFixed(2)}°{selectedPlace.lng >= 0 ? "E" : "W"} / {Math.abs(selectedPlace.lat).toFixed(2)}°{selectedPlace.lat >= 0 ? "N" : "S"} (UTC{selectedPlace.utcOffset >= 0 ? "+" : ""}{selectedPlace.utcOffset})
          </span>
        )}
      </div>

      <button type="submit" className="submit-btn" disabled={loading || !selectedPlace}>
        {loading ? "计算中..." : "生成人类图"}
      </button>
    </form>
  );
}
