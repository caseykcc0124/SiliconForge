# SiliconForge v3.1 Coding Agent 開發入口

**此文件適用於 GitHub Browser + Download ZIP + Local Git 的 Coding Agent。** 該 Agent 沒有 GitHub Clone／Pull／Push 能力；它只會透過 Chrome／Computer Use 瀏覽 GitHub，並且只能透過 GitHub 網頁編輯 `SiliconForge_Working_SYNC.md`。如果尚未下載 ZIP，先直接打開 Sync 檔就可接收工作。詳細協定：[18｜Browser + ZIP 交付](docs/18_BROWSER_ZIP_CODING_AGENT_HANDOFF.md)。

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

- 先讀並持續更新 [SiliconForge_Working_SYNC.md](SiliconForge_Working_SYNC.md)，這是本專案唯一權威狀態檔，不要建立第二個同步入口。
- 每次有實際 commit、Fork、Merge、驗證完成、阻塞或需批准事項，記錄探索群組 / 分支 / Instance / Commit / Evidence / 停止原因 / 下一步；活躍期間每 15 分鐘至少更新一次狀態或 Heartbeat。
- 進展、模擬、真實 EDA、未執行分開記錄。Heartbeat、Worker 數量、分支數量不算工程成果。
- Agent 的實作採 **Local Git Branch / Local Commit**；它不能直接推 GitHub Branch、Commit／PR。需要交付程式時在 Local 製作 ZIP／Patch Bundle 和 SHA256，只有實際可用的傳遞管道交到授權 Integrator 後，才能由 Integrator 寫入 GitHub 並驗證。缺少傳遞管道時須明記交付受阻，不能宣稱遠端已更新。

**即刻可執行下一步：** 先執行既有 A0 基準測試，做 80 項 Gap Audit，將 A0X Exploration Registry/Owner Instance/Worktree Isolation 的第一個可驗收工作切入既有 A0/M1 模組，保留失敗測試，逐 Gate 繼續推進。


## Repo 完全獨立（強制）

本 Repository 已包含自有程式碼、Spec、Skills、Mock 模擬器、測試與 GitHub Sync。不需要也不允許另外從其他 SiliconForge Repository 拉取檔案來完成任務。先閱讀 [17｜Standalone Repository Contract](docs/17_STANDALONE_REPOSITORY_CONTRACT.md)，並執行 `python -m unittest discover -s tests -v` 檢查獨立性。所有**GitHub 網頁回報**僅寫入本 Repo 的 `SiliconForge_Working_SYNC.md`；程式與測試先保存在 Local，待取得真正的 Artifact 交付通道後交由授權 Integrator 提交此 Repo。不得要求這位 Agent 執行 GitHub Clone 或 Push。

## 動態監督指令與自主進度推進

**目前最優先的工作命令**請直接從 [SiliconForge_Working_SYNC.md](SiliconForge_Working_SYNC.md) 讀取，再開啟 [19｜Supervisor Work Order](docs/19_SUPERVISOR_WORK_ORDER.md)。活躍執行期間每 15 分鐘用 Chrome 重新讀取 docs/19，比對 `DIRECTIVE_ID`，如有更新則在安全檢查點套用並以 Sync 網頁編輯回覆 `last_seen_directive_id`、ACK、目前 Gate、Local SHA、測試證據、阻礙及下一步。**無更新則繼續目前工作與已授權的後續里程碑，不必等待人類重複指示。**

監督端每兩小時檢查 Sync，必要時只更新 docs/19 的工作方向；不接管 Agent 的 Sync 狀態欄位。此安排不代表關閉 Agent Session 後依然具備 Always-on Polling，若無常駐能力須如實註記。Coding Agent 仍只能用 Local Git 與 GitHub Browser 編輯單一 Sync 檔。
