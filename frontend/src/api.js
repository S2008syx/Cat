import CITIES from "./cities.json";

const API_BASE = import.meta.env.VITE_API_URL || "";

function offlineSearchPlaces(query) {
  const q = query.trim().toLowerCase();
  if (!q) return [];
  const results = [];
  for (const c of CITIES) {
    if (c.name.includes(q) || c.province.includes(q)) {
      results.push({
        name: c.name,
        address: "",
        district: c.province,
        location: `${c.lng},${c.lat}`,
        utc_offset: c.utc_offset,
      });
      if (results.length >= 10) break;
    }
  }
  return results;
}

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
  try {
    const res = await fetch(`${API_BASE}/api/places?q=${encodeURIComponent(query)}`);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    const results = data.results || [];
    if (results.length > 0) return { results, source: "api" };
    // API returned empty, try offline as well
    const offline = offlineSearchPlaces(query);
    return { results: offline, source: offline.length > 0 ? "offline" : "empty" };
  } catch {
    // API unavailable, use offline search
    const results = offlineSearchPlaces(query);
    return { results, source: results.length > 0 ? "offline" : "empty" };
  }
}
