/**
 * [MOCK DATA] 人类图 Demo 假数据
 *
 * 这是硬编码的 mock 数据，不经过后端计算。
 * 不管用户输入什么出生信息，都会返回这份固定的人类图结果。
 *
 * 当后端 API 可用时，请切换回 api.js 中的真实 fetchChart 接口。
 * 对应的真实计算逻辑在: /hd_calculator + /hd_converters (Python)
 */
import { MOCK_CHART_SVG } from "./mockChartSvg"; // [MOCK] 预渲染的 SVG 人体图

// [MOCK] 固定的图表数据 —— 类型: 生产者, 人生角色: 4/6, 权威: 情绪权威
export const MOCK_CHART_RESPONSE = {
  // [MOCK] 预渲染的高质量 SVG 人体图（由 chart_image.py 生成）
  chart_svg: MOCK_CHART_SVG,
  // [MOCK] 模拟用户输入
  input: {
    name: "Demo 用户",
    birth_date: "1990-01-15",
    birth_time: "06:30",
    longitude: 121.47,
    latitude: 31.23,
    utc_offset: 8,
  },
  graph: {
    centers: [
      { id: "head", name_zh: "头脑中心", defined: false,
        position: { x: 0.48, y: 0.09 }, shape: "triangle" },
      { id: "ajna", name_zh: "逻辑中心", defined: false,
        position: { x: 0.48, y: 0.22 }, shape: "triangle" },
      { id: "throat", name_zh: "喉咙中心", defined: true,
        position: { x: 0.48, y: 0.37 }, shape: "square" },
      { id: "g", name_zh: "G中心", defined: true,
        position: { x: 0.48, y: 0.53 }, shape: "diamond" },
      { id: "heart", name_zh: "意志力中心", defined: false,
        position: { x: 0.61, y: 0.61 }, shape: "triangle" },
      { id: "sacral", name_zh: "骶骨中心", defined: true,
        position: { x: 0.48, y: 0.81 }, shape: "square" },
      { id: "solar_plexus", name_zh: "情绪中心", defined: true,
        position: { x: 0.75, y: 0.77 }, shape: "triangle" },
      { id: "spleen", name_zh: "直觉中心", defined: false,
        position: { x: 0.18, y: 0.77 }, shape: "triangle" },
      { id: "root", name_zh: "根中心", defined: false,
        position: { x: 0.47, y: 0.95 }, shape: "square" },
    ],
    channels: [
      { gate_a: 20, gate_b: 34, center_a: "throat", center_b: "sacral", color: "mixed" },
      { gate_a: 59, gate_b: 6, center_a: "sacral", center_b: "solar_plexus", color: "personality" },
      { gate_a: 7, gate_b: 31, center_a: "g", center_b: "throat", color: "design" },
    ],
    gates: [
      { gate: 6, center: "solar_plexus", color: "personality",
        activated_by: [{ side: "personality", planet: "sun", line: 4 }] },
      { gate: 7, center: "g", color: "design",
        activated_by: [{ side: "design", planet: "moon", line: 2 }] },
      { gate: 13, center: "g", color: "personality",
        activated_by: [{ side: "personality", planet: "earth", line: 1 }] },
      { gate: 20, center: "throat", color: "both",
        activated_by: [
          { side: "personality", planet: "mercury", line: 3 },
          { side: "design", planet: "sun", line: 5 },
        ] },
      { gate: 31, center: "throat", color: "design",
        activated_by: [{ side: "design", planet: "venus", line: 1 }] },
      { gate: 34, center: "sacral", color: "design",
        activated_by: [{ side: "design", planet: "mars", line: 6 }] },
      { gate: 59, center: "sacral", color: "personality",
        activated_by: [{ side: "personality", planet: "venus", line: 2 }] },
    ],
    meta: {
      type: "Generator",
      profile: "4/6",
      authority: "Emotional",
    },
  },
  words: {
    type_info: {
      key: "Generator",
      name_zh: "生产者",
      strategy: "等待回应",
      strategy_zh: "等待回应",
      not_self: "挫败感",
      description: "你拥有持续不断的生命力能量，是世界的建造者。",
    },
    authority_info: {
      key: "Emotional",
      name_zh: "情绪权威",
      description: "在做重要决定之前，等待情绪波浪走完一个完整周期。没有当下的真相。",
    },
    profile_info: {
      key: "4/6",
      name_zh: "机会主义者/榜样",
      description: "通过人际网络获取机会，人生分三阶段逐步成为他人榜样。",
      line1: { number: 4, name_zh: "机会主义者" },
      line2: { number: 6, name_zh: "榜样" },
    },
    definition_info: {
      key: "Split",
      name_zh: "二分定义",
      description: "定义的中心分成两个独立的组，需要桥梁来连接两部分能量。",
    },
    cross_info: {
      type: "Right Angle",
      name_en: "Right Angle Cross of Eden",
      name_zh: "右角度伊甸园之十字",
      gates: [12, 11, 6, 36],
    },
    center_infos: [
      { id: "head", name_zh: "头脑中心", defined: false, theme: "灵感与压力", not_self_theme: "试图回答不属于你的问题" },
      { id: "ajna", name_zh: "逻辑中心", defined: false, theme: "概念化与思考", not_self_theme: "假装确定" },
      { id: "throat", name_zh: "喉咙中心", defined: true, theme: "表达与行动", not_self_theme: "试图引起注意" },
      { id: "g", name_zh: "G中心", defined: true, theme: "身份与方向", not_self_theme: "寻找爱与方向" },
      { id: "heart", name_zh: "意志力中心", defined: false, theme: "意志力与价值", not_self_theme: "不断试图证明自己" },
      { id: "sacral", name_zh: "骶骨中心", defined: true, theme: "生命力与工作力", not_self_theme: "不知道什么时候足够了" },
      { id: "solar_plexus", name_zh: "情绪中心", defined: true, theme: "情绪波与感受", not_self_theme: "逃避真相与对抗" },
      { id: "spleen", name_zh: "直觉中心", defined: false, theme: "直觉与健康", not_self_theme: "紧抓不健康的东西" },
      { id: "root", name_zh: "根中心", defined: false, theme: "肾上腺素压力", not_self_theme: "总是急于完成事情" },
    ],
    channel_infos: [
      { gates: [20, 34], name_zh: "魅力的通道", name_en: "Channel of Charisma", centers: ["throat", "sacral"], theme: "忙碌中的觉知" },
      { gates: [59, 6], name_zh: "亲密的通道", name_en: "Channel of Mating", centers: ["sacral", "solar_plexus"], theme: "专注于生育的设计" },
      { gates: [7, 31], name_zh: "领导力的通道", name_en: "Channel of The Alpha", centers: ["g", "throat"], theme: "为善而领导" },
    ],
    gate_infos: [
      { gate: 6, name_zh: "冲突之门", name_en: "Gate of Friction", center: "solar_plexus", keynote: "情绪的平衡与摩擦",
        activated_by: [{ side: "personality", planet: "sun", line: 4 }] },
      { gate: 7, name_zh: "军队之门", name_en: "Gate of The Role of the Self", center: "g", keynote: "在互动中的自我角色",
        activated_by: [{ side: "design", planet: "moon", line: 2 }] },
      { gate: 20, name_zh: "当下之门", name_en: "Gate of The Now", center: "throat", keynote: "当下的觉知与表达",
        activated_by: [{ side: "personality", planet: "mercury", line: 3 }, { side: "design", planet: "sun", line: 5 }] },
      { gate: 31, name_zh: "影响力之门", name_en: "Gate of Influence", center: "throat", keynote: "通过领导产生影响",
        activated_by: [{ side: "design", planet: "venus", line: 1 }] },
      { gate: 34, name_zh: "力量之门", name_en: "Gate of Power", center: "sacral", keynote: "强大的回应力量",
        activated_by: [{ side: "design", planet: "mars", line: 6 }] },
      { gate: 59, name_zh: "分散之门", name_en: "Gate of Sexuality", center: "sacral", keynote: "打破障碍的能量",
        activated_by: [{ side: "personality", planet: "venus", line: 2 }] },
    ],
    // [MOCK] 星体激活表 —— 13行（太阳到北交点），左设计右个性
    activations: {
      personality: [
        { planet: "sun",           planet_zh: "太阳 ☉",   gate: 6,  line: 4, gate_name_zh: "冲突之门" },
        { planet: "earth",         planet_zh: "地球 ⊕",   gate: 13, line: 1, gate_name_zh: "倾听者之门" },
        { planet: "moon",          planet_zh: "月亮 ☽",   gate: 29, line: 3, gate_name_zh: "深渊之门" },
        { planet: "north_node",    planet_zh: "北交点 ☊", gate: 44, line: 5, gate_name_zh: "聚合之门" },
        { planet: "south_node",    planet_zh: "南交点 ☋", gate: 24, line: 2, gate_name_zh: "回归之门" },
        { planet: "mercury",       planet_zh: "水星 ☿",   gate: 20, line: 3, gate_name_zh: "当下之门" },
        { planet: "venus",         planet_zh: "金星 ♀",   gate: 59, line: 2, gate_name_zh: "分散之门" },
        { planet: "mars",          planet_zh: "火星 ♂",   gate: 40, line: 1, gate_name_zh: "递送之门" },
        { planet: "jupiter",       planet_zh: "木星 ♃",   gate: 37, line: 4, gate_name_zh: "友谊之门" },
        { planet: "saturn",        planet_zh: "土星 ♄",   gate: 54, line: 6, gate_name_zh: "少女之门" },
        { planet: "uranus",        planet_zh: "天王星 ♅", gate: 38, line: 2, gate_name_zh: "斗士之门" },
        { planet: "neptune",       planet_zh: "海王星 ♆", gate: 58, line: 1, gate_name_zh: "活力之门" },
        { planet: "pluto",         planet_zh: "冥王星 ♇", gate: 51, line: 5, gate_name_zh: "激发之门" },
      ],
      design: [
        { planet: "sun",           planet_zh: "太阳 ☉",   gate: 20, line: 5, gate_name_zh: "当下之门" },
        { planet: "earth",         planet_zh: "地球 ⊕",   gate: 34, line: 2, gate_name_zh: "力量之门" },
        { planet: "moon",          planet_zh: "月亮 ☽",   gate: 7,  line: 2, gate_name_zh: "军队之门" },
        { planet: "north_node",    planet_zh: "北交点 ☊", gate: 11, line: 4, gate_name_zh: "和平之门" },
        { planet: "south_node",    planet_zh: "南交点 ☋", gate: 12, line: 3, gate_name_zh: "静止之门" },
        { planet: "mercury",       planet_zh: "水星 ☿",   gate: 31, line: 6, gate_name_zh: "影响力之门" },
        { planet: "venus",         planet_zh: "金星 ♀",   gate: 31, line: 1, gate_name_zh: "影响力之门" },
        { planet: "mars",          planet_zh: "火星 ♂",   gate: 34, line: 6, gate_name_zh: "力量之门" },
        { planet: "jupiter",       planet_zh: "木星 ♃",   gate: 2,  line: 3, gate_name_zh: "接收之门" },
        { planet: "saturn",        planet_zh: "土星 ♄",   gate: 56, line: 1, gate_name_zh: "刺激之门" },
        { planet: "uranus",        planet_zh: "天王星 ♅", gate: 48, line: 5, gate_name_zh: "井之门" },
        { planet: "neptune",       planet_zh: "海王星 ♆", gate: 22, line: 4, gate_name_zh: "优雅之门" },
        { planet: "pluto",         planet_zh: "冥王星 ♇", gate: 49, line: 2, gate_name_zh: "革命之门" },
      ],
    },
  },
};
