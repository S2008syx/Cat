import CITIES from "./cities.json";
import { MOCK_CHART_RESPONSE } from "./mockData"; // [MOCK]

/**
 * [MOCK] 返回硬编码的人类图数据，不调用后端 API。
 * TODO: 接入真实后端时，替换为真实的 POST /api/chart 调用。
 */
export async function fetchChart() {
  await new Promise((resolve) => setTimeout(resolve, 300));
  return MOCK_CHART_RESPONSE;
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
