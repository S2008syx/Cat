# Human Design Calculator Module

纯 Python 计算引擎，使用 Swiss Ephemeris 天文库计算人类图（Human Design）参数。

## 这是什么

这是一个**纯计算模块**（Part 3），接收 UTC 出生时间 + 出生地经纬度，输出完整的人类图参数。

- **不包含**前端 UI
- **不包含**用户输入处理（由 Part 2 负责）
- **不包含**结果解读（由 Part 4 负责）

```
[Part 2] 输入处理 → [Part 3] 计算器（本模块）→ [Part 4] 解读器
```

---

## 输入输出规范

### 输入（CalculatorInput）

| 字段 | 类型 | 说明 |
|------|------|------|
| `birth_utc` | `datetime` | UTC 出生时间，由上游 Part 2 已转换好 |
| `latitude` | `float` | 出生地纬度（如 31.2304 为上海）。当前不参与计算，保留供未来使用 |
| `longitude` | `float` | 出生地经度（如 121.4737 为上海）。当前不参与计算，保留供未来使用 |

### 输出（CalculatorOutput）

| 字段 | 类型 | 可选值/含义 |
|------|------|------------|
| `type` | `str` | `"Generator"` / `"Manifesting Generator"` / `"Manifestor"` / `"Projector"` / `"Reflector"` |
| `strategy` | `str` | `"To Respond"` / `"To Inform"` / `"To Wait for Invitation"` / `"To Wait a Lunar Cycle"` |
| `authority` | `str` | `"Emotional"` / `"Sacral"` / `"Splenic"` / `"Ego Manifested"` / `"Ego Projected"` / `"Self-Projected"` / `"Lunar"` / `"Mental"` |
| `profile` | `str` | 格式 `"X/Y"`，如 `"1/3"`、`"4/6"` |
| `definition_type` | `str` | `"None"` / `"Single"` / `"Split"` / `"Triple Split"` / `"Quadruple Split"` |
| `split_type` | `str \| None` | 仅当 `definition_type == "Split"` 时为 `"Small"` 或 `"Large"`，否则为 `None` |
| `incarnation_cross_type` | `str` | `"Right Angle"` / `"Juxtaposition"` / `"Left Angle"` |
| `incarnation_cross_gates` | `list[int]` | `[人格太阳门, 人格地球门, 设计太阳门, 设计地球门]` |
| `defined_centers` | `list[str]` | 被定义的能量中心列表 |
| `undefined_centers` | `list[str]` | 未定义的能量中心列表 |
| `active_channels` | `list[dict]` | 被激活的通道列表，每项含 `gate_a`、`gate_b`、`center_a`、`center_b` |
| `personality_activations` | `list[dict]` | 人格（意识）激活数据（13 颗星体），每项含 `planet`、`gate`、`line`、`longitude` |
| `design_activations` | `list[dict]` | 设计（无意识）激活数据（13 颗星体），同上结构 |
| `design_utc` | `datetime` | 计算出的设计时刻（88° 太阳回退） |
| `all_active_gates` | `list[int]` | 所有被激活的门的去重列表 |

9 个能量中心名称：`head`、`ajna`、`throat`、`g`、`heart`、`sacral`、`solar_plexus`、`spleen`、`root`

---

## 安装和使用

### 安装依赖

```bash
pip install pyswisseph
```

### 使用示例

```python
from hd_calculator import calculate
from datetime import datetime, timezone

result = calculate(
    birth_utc=datetime(1990, 1, 15, 6, 30, tzinfo=timezone.utc),
    latitude=31.2304,
    longitude=121.4737,
)

print(result.type)        # "Generator"
print(result.profile)     # "5/1"
print(result.authority)   # "Sacral"
print(result.defined_centers)  # ["g", "sacral", "spleen", "root"]
```

---

## 计算逻辑说明

### 整体流程

输入一个人的 UTC 出生时间，经过五步计算，输出完整的人类图参数。

### 第 1 步：计算星体位置

使用 Swiss Ephemeris 天文库（NASA JPL 精度），计算出生时刻 13 颗星体在黄道上的位置（角度值）。

13 颗星体包括：太阳、地球、月亮、北交点、南交点、水星、金星、火星、木星、土星、天王星、海王星、冥王星。

其中地球 = 太阳 + 180°，南交点 = 北交点 + 180°，这两颗不需要额外查天文表。

同时，计算出生前太阳回退 88° 的精确时刻（称为"设计时刻"），使用 Newton-Raphson 迭代法求解。再在设计时刻算一遍 13 颗星体的位置。

这样得到 26 个角度值（人格 13 个 + 设计 13 个）。

### 第 2 步：角度 → 门和爻

人类图把黄道 360° 均分成 64 个"门"，每个门占 5.625°，每个门再分成 6 条"爻"，每爻占 0.9375°。

门的排列不是按数字顺序，而是按人类图轮盘上的特定顺序（GATE_ORDER），从 302°（水瓶座 2°）处的门 41 开始。

每颗星体的角度值通过公式映射到对应的门和爻：
1. 计算角度相对于 302° 的偏移量
2. 偏移量 ÷ 5.625 = 门的序号
3. 在 GATE_ORDER 表中查找对应的门号
4. 余数部分 ÷ 0.9375 + 1 = 爻号

这一步得到 26 组 (门, 爻) 数据。

### 第 3 步：门 → 通道和能量中心

人体图上有 36 条"通道"，每条连接两个"能量中心"，每条通道的两端各有一个"门"。

如果一条通道两端的门**都**被激活（不管是人格还是设计的激活），这条通道就被"定义"。

通道被定义后，其两端的能量中心也跟着被"定义"。

### 第 4 步：中心连通性 → 定义类型

用图论的 BFS（广度优先搜索）算法，查看所有被定义的中心之间的连通性——有几个独立的"连通分量"：

- 0 个被定义的中心 = 无定义（None）
- 所有中心在 1 个连通分量中 = 单一定义（Single Definition）
- 2 个连通分量 = 二分定义（Split Definition）
  - 进一步判断 Small Split 或 Large Split（是否存在单条通道可以桥接两个分量）
- 3 个连通分量 = 三分定义（Triple Split）
- 4 个连通分量 = 四分定义（Quadruple Split）

### 第 5 步：推导类型、策略、权威等

根据哪些中心被定义、以及它们的连接方式，用一组固定的规则判断出：

**能量类型**（5 种之一）：
1. 无定义中心 → 反映者（Reflector）
2. 骶骨中心被定义 + 动力中心到喉咙有路径 → 显示生产者（Manifesting Generator）
3. 骶骨中心被定义 → 生产者（Generator）
4. 非骶骨动力中心（根、情绪、意志力）到喉咙有路径 → 显示者（Manifestor）
5. 其他情况 → 投射者（Projector）

"有路径"指的是：沿着已定义的通道，可以从动力中心一步步走到喉咙中心（允许经过中间的定义中心）。

**人生策略**（由类型直接决定）：
- Generator / MG → 等待回应（To Respond）
- Manifestor → 告知（To Inform）
- Projector → 等待邀请（To Wait for Invitation）
- Reflector → 等待月循环（To Wait a Lunar Cycle）

**内在权威**（按优先级链判断）：
1. 情绪中心被定义 → 情绪权威
2. 骶骨中心被定义 → 骶骨权威
3. 脾中心被定义 → 脾权威
4. 意志力中心被定义且直连喉咙 → 显示型自我权威
5. 意志力中心被定义 → 投射型自我权威
6. G 中心被定义且直连喉咙 → 自我投射权威
7. 反映者 → 月亮权威
8. 其他 → 精神权威

**人生角色**：人格太阳的爻 / 设计太阳的爻（如 "4/6"）

**化身十字**：由人格太阳门、人格地球门、设计太阳门、设计地球门组成。十字类型由人生角色的第一个数字决定（1-3 为 Right Angle，4 为 Juxtaposition，5-6 为 Left Angle）。

---

## 项目结构

```
hd_calculator/
├── __init__.py              # 暴露 calculate() 主函数（唯一公开接口）
├── ephemeris.py             # 第 1 层：Swiss Ephemeris 封装，星体位置计算
├── gate_mapping.py          # 第 2 层：黄经度数 → 门/爻映射
├── chart_properties.py      # 第 3+4+5 层：通道、中心、类型、权威等推导
├── models.py                # 输入/输出数据结构（dataclass）
├── data/
│   ├── gates.py             # 门序表（GATE_ORDER，64 个门的轮盘排列）
│   ├── channels.py          # 通道表（36 条通道定义）
│   └── centers.py           # 中心定义（9 个中心及其包含的门）
└── tests/
    └── test_calculator.py   # 测试用例（32 个测试）
```

---

## 开源参考

本项目的计算逻辑参考了以下开源项目：

### 核心算法

- **88° 太阳回退算法**：参考 PyHD 开发博客中描述的 Newton-Raphson 迭代法思路
  - 来源：https://pascal.polleunus.be/blog/learning-human-design-by-building-a-python-library

### 数据表

- **门序表（GATE_ORDER）**：从 hdkit 和 SharpAstrology 交叉验证
  - hdkit: https://github.com/jdempcy/hdkit
  - SharpAstrology: https://github.com/CReizner/SharpAstrology.HumanDesign
  - humandesign_api: https://github.com/dturkuler/humandesign_api
  - human_design_engine: https://github.com/MicFell/human_design_engine
- **通道表（CHANNELS）**：从 SharpAstrology、hdkit 和 MCP_Human_design 交叉验证
  - SharpAstrology: https://github.com/CReizner/SharpAstrology.HumanDesign
  - hdkit: https://github.com/jdempcy/hdkit
  - MCP_Human_design: https://github.com/dvvolkovv/MCP_Human_design
- **中心定义（CENTERS）**：从 SharpAstrology 和 hdkit 验证
  - SharpAstrology: https://github.com/CReizner/SharpAstrology.HumanDesign
  - hdkit: https://github.com/jdempcy/hdkit

### 推导逻辑

- **类型判定**：参考 SharpAstrology 的 Type 属性计算（C# → Python 翻译）
  - https://github.com/CReizner/SharpAstrology.HumanDesign
- **权威判定**：参考 SharpAstrology 的 Authority 优先级链
  - https://github.com/CReizner/SharpAstrology.HumanDesign
- **定义类型**：参考 PyHD 博客中描述的 BFS 连通分量算法
  - https://pascal.polleunus.be/blog/learning-human-design-by-building-a-python-library
- **路径搜索**（动力中心到喉咙）：参考 MCP_Human_design 的实现
  - https://github.com/dvvolkovv/MCP_Human_design

### 天文计算

- **Swiss Ephemeris**：通过 pyswisseph Python 绑定调用
  - pyswisseph: https://github.com/astrorigin/pyswisseph
  - 使用 Moshier 内置星历（无需外部数据文件）

### 其他参考

- **humandesign_api**：整体架构、门/爻计算参考
  - https://github.com/dturkuler/humandesign_api
- **human_design_engine**：计算逻辑、数据表参考
  - https://github.com/MicFell/human_design_engine
- **gordianknotC/humandesign_frontend_js**：中文语境数据结构参考
  - https://github.com/gordianknotC/humandesign_frontend_js

---

## 技术约束

- Python 3.10+
- 唯一外部依赖：`pyswisseph`
- 星历模式：Moshier（内置，无需额外数据文件，无网络请求）
- 不依赖任何 Web 框架
- 不依赖任何外部 API
- 所有函数均有 type hints 和 docstring
