import CITIES from "./cities.json";

/**
 * 调用后端 POST /api/chart 获取真实人类图数据。
 *
 * @param {Object} params - 请求参数
 * @param {string} params.name - 姓名
 * @param {string} params.birth_date - "YYYY-MM-DD"
 * @param {string} params.birth_time - "HH:MM"
 * @param {number} params.longitude - 经度
 * @param {number} params.latitude - 纬度
 * @param {number} params.utc_offset - UTC 偏移（小时）
 * @returns {Promise<Object>} 后端返回的图表数据
 */
export async function fetchChart(params) {
  const body = {
    name: params.name || "",
    birth_date: params.birthDate,
    birth_time: params.birthTime,
    longitude: params.longitude,
    latitude: params.latitude,
    utc_offset: params.utcOffset ?? 8.0,
  };
  const resp = await fetch("/api/chart", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: resp.statusText }));
    throw new Error(err.detail || "请求失败");
  }
  return resp.json();
}

/** 搜索城市（本地离线数据） */
export function searchPlaces(query) {
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
