const API_BASE = "http://localhost:8000";

export async function fetchChart({ name, birthDate, birthTime, longitude, latitude, utcOffset }) {
  const res = await fetch(`${API_BASE}/api/chart`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name,
      birth_date: birthDate,
      birth_time: birthTime,
      longitude,
      latitude,
      utc_offset: utcOffset,
    }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function searchPlaces(query) {
  const res = await fetch(`${API_BASE}/api/places?q=${encodeURIComponent(query)}`);
  if (!res.ok) return [];
  const data = await res.json();
  return data.results || [];
}
