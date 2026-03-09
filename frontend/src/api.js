const API_BASE = import.meta.env.VITE_API_URL || "";

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
  if (!res.ok) {
    let detail = `API error: ${res.status}`;
    try {
      const body = await res.json();
      if (body.detail) detail = body.detail;
    } catch {}
    throw new Error(detail);
  }
  return res.json();
}

export async function searchPlaces(query) {
  const res = await fetch(`${API_BASE}/api/places?q=${encodeURIComponent(query)}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  const data = await res.json();
  return data.results || [];
}
