# SiliconForge v3.1 Coding Agent 開發入口

**唯一實作目標：** 在本 Repository 繼續完成可恢復、事件驅動的自主晶片研發框架。Super Agent Runtime 管理自主性；同一 Domain Role 可以同時擁有多個 Owner Instance；每個 Instance 使用領域特化 P-Stack Skills，自主處理所屬 Candidate 的工程問題。人類透過原生 Codex / Claude Code + Skills/MCP 操作，Web 顯示工程與事件 DAG；不另外開發聊天 CLI。

## 正式執行順序

1. 讀 [AGENTS.md](AGENTS.md)、[主旨](docs/00_MISSION_AND_BOUNDARIES.md)、[事件協定](docs/02_EVENT_RUNTIME_PROTOCOL.md)、[既有驗收](docs/09_ACCEPTANCE_TEST_MATRIX.md)、[正式工作指令](docs/10_CODING_AGENT_EXECUTION_ORDER.md)、[權威進度](SiliconForge_Working_SYNC.md)。
2. **v3.1 必讀**：[多 Owner / 並行探索架構](docs/14_PARALLEL_EXPLORATION_ARCHITECTURE.md)、[E01–E20 驗收](docs/15_PARALLEL_EXPLORATION_ACCEPTANCE.md)、[實作插入點](docs/16_PARALLEL_EXPLORATION_IMPLEMENTATION.md)、[Policy](config/exploration_policy.json)、[JSON Schema](contracts/exploration_event.schema.json)、[E 類機器驗收表](contracts/parallel_exploration_acceptance.json)。
3. 完成既有 A0 至 A6 的所有要求，並在既有順序內加入 A0X、A3X、A4X、A5X、A6X 的 Branch Exploration 工作。**不能另外開新專案，不能以 v3.1 覆蓋既有成果或降低任何 Gate。**
4. 現有 A0–A6 共 **60 個 Required Cases**；新增 **E01–E20 共 20 個**；合計 **80 項 Required Acceptance**，全部要有原始可重現證據，未實測不得標 PASS。

## 必須真正做到的三路驗證

同一個 APB CRC32 Requirement 同時展開 performance、low_power、area 三個獨立 Git Branch/Worktree；至少三個 RTL Owner Instances 可並行執行，各自啟動 Verification、Formal 和 PPA；其中一支再次 Fork。每支候選保留獨立 Commit、Spec Revision、Toolchain/Constraints SHA、Seeds、EDA Report 和 Evidence Fingerprint。對候選進行 Pareto 比較，保留無支配解；建立受控 Merge Proposal，處理衝突，產生全新的 Merge SHA 後**重新完成所有必要 Gate**。

不得把順序執行偽裝成並行，不得把不同 Branch 的 PASS 混用，不得由 Main Agent 代替領域 Owner 決定技術方案，不得無限分叉或為求通過而放寬測試。

## 工作回報與同步

- 先讀並持續更新 [SiliconForge_Working_SYNC.md](SiliconForge_Working_SYNC.md)，不要寫到另一個 Repo 的同名或相似檔案。
- 每次有實際 commit、Fork、Merge、驗證完成、阻塞或需批准事項，記錄探索群組 / 分支 / Instance / Commit / Evidence / 停止原因 / 下一步；活躍期間每 15 分鐘至少更新一次狀態或 Heartbeat。
- 進展、模擬、真實 EDA、未執行分開記錄。Heartbeat、Worker 數量、分支數量不算工程成果。
- 對實作仍採 Git topic branch + PR；批准邊界、資源上限和公開發布政策依現有 AGENTS.md。

**即刻可執行下一步：** 先執行既有 A0 基準測試，做 80 項 Gap Audit，將 A0X Exploration Registry/Owner Instance/Worktree Isolation 的第一個可驗收工作切入既有 A0/M1 模組，保留失敗測試，逐 Gate 繼續推進。
