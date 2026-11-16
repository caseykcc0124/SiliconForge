# UI模擬器

SiliconForge v3.0 自主晶片工程系統運作互動模擬器。

## 開啟方式

1. 下載同資料夾的 [index.html](./index.html)。
2. 用 Chrome 或 Edge 開啟 HTML。
3. 自由注入 Spec、Simulation、Formal、PPA、環境異常等事件，觀察 Super Agent Runtime 的事件路由、Domain Owner 的 P-Stack 活動、EDA 回流、Evidence Gate、Human Approval、Watchdog、Notifications 及 PDCA。
4. 可逐事件執行或自動播放，並查看事件紀錄。

## 模擬邊界

本頁是獨立的離線互動展示。Agent、Codex／Claude Code、EDA 工具與證據均屬模擬，不代表真實 SiliconForge 後端、MCP Server、RTL、Formal 或 OpenROAD 已完成整合。

## 設計原則

- Super Agent Runtime 管理事件可靠投遞、路由、自主執行與恢復。
- P-Stack 特化方法沉入各 Domain Owner。
- Codex／Claude Code 是使用者原生 Harness 入口，Main Agent 不仲裁工程決策。
- Environment Owner 負責工具環境，Integration Gate 需同版工程證據。
- 超過預算、越界擴張或缺乏有效進展時，系統應有理由地停止。

本目錄只放 UI 展示資料，不會更改其他工程工作狀態。
