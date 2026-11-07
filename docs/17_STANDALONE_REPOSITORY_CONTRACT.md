# 17. SiliconForge Standalone Repository Contract

## 17.1 唯一權威來源

SiliconForge 的**唯一原始碼、架構規格、驗收契約、Agent 工作指引與開發同步來源**是此 Repository：

```text
https://github.com/caseykcc0124/SiliconForge
```

獨立 Clone 本 Repository 後，無須另外 Clone、解壓、引用或 Fetch 其他 SiliconForge Repository 才能閱讀全部現行規格、執行 A0 參考測試、運作本地參考 Runtime、使用內建 Skills / MCP Scaffold、更新唯一狀態同步檔或繼續開發下一里程碑。

一般 Python build dependency、外部原生 Codex/Claude Code Harness 服務、Open Source EDA 套件及工具鏈的依賴，依本 Repo 自有配置與正常安裝流程建立；**不得以別處另一個 SiliconForge Repo 充當原始碼、Spec、測試或發行來源**。任何暫時無法提供的外部 EDA 工具須記為 Environment Blocker，不能偷偷使用未知版本成果代替。

## 17.2 單一 Repository 的權威檔案

| 目的 | 目前 Repository 中的權威檔案 |
|---|---|
| Coding Agent 首輪入口 | `CODING_AGENT_START_HERE.md` |
| Codex Agent / Claude Code 專案規則 | `AGENTS.md` 和 `CLAUDE.md` |
| 產品初衷、架構與事件協定 | `docs/00_MISSION_AND_BOUNDARIES.md`、`docs/01_ARCHITECTURE_AND_OWNERSHIP.md`、`docs/02_EVENT_RUNTIME_PROTOCOL.md` |
| Runtime、Harness、EDA、P-Stack、Watchdog、Observability | `docs/03_PSTACK_DOMAIN_WORKFLOWS.md` 至 `docs/07_SAFETY_AND_RESOURCE_GATES.md` |
| 實作順序與原生 60 項驗收 | `docs/08_IMPLEMENTATION_PLAN.md`、`docs/09_ACCEPTANCE_TEST_MATRIX.md`、`docs/10_CODING_AGENT_EXECUTION_ORDER.md` |
| v3.1 Branch/多實例 Owner／Merge 設計 | `docs/14_PARALLEL_EXPLORATION_ARCHITECTURE.md` |
| v3.1 新增 20 項驗收 | `docs/15_PARALLEL_EXPLORATION_ACCEPTANCE.md`、`contracts/parallel_exploration_acceptance.json` |
| v3.1 實作插入點 | `docs/16_PARALLEL_EXPLORATION_IMPLEMENTATION.md` |
| 完整 GitHub 同步／工作進度 | `SiliconForge_Working_SYNC.md` |
| Runtime／Harness／MCP 的參考實作 | `src/siliconforge/` |
| 可執行 A0 參考測試 | `tests/` |
| 區分正式 EDA 與 mock 的展示工具 | `simulator/`、`examples/` |
| 本地原生操作 Skill | `skills/` |
| 所有環境與工具策略 | `config/`、`contracts/` |

`docs/reference/` 只作**本 Repository 內部**的歷史背景，所有現行版本以根目錄入口及 docs/00–17、contracts 和 config 為準。不得要求 Coding Agent 去外部 Repo 下載某個隱含必備檔才能執行本地規格。

## 17.3 使用 Chrome／Download ZIP 取得乾淨 Local 專案

從 GitHub 網頁進入 `caseykcc0124/SiliconForge`，選擇 **Code → Download ZIP**，下載至 Coding Agent 的 Local 並解壓。ZIP 不含 Git 歷史；在解壓資料夾執行：

```bash
python -m pip install --no-build-isolation -e .
python -m unittest discover -s tests -v
python -m siliconforge.demo
```

Agent 可在 Local 自行 `git init`／建立 Local Branch／Local Commit，但沒有遠端 GitHub Clone／Pull／Push 權限。它只能以 Browser 編輯 `SiliconForge_Working_SYNC.md`。實際原始碼要另以 ZIP／Patch 交付授權 Integrator，未收到完整產物前不得宣稱已更新 GitHub。見 `docs/18_BROWSER_ZIP_CODING_AGENT_HANDOFF.md`。

上述命令驗證的是**本 Repo 所含的 A0 參考 Runtime**；真實 Codex/Claude、EDA、完整並行探索的驗收仍依 A0–A6 與 E01–E20 逐項獨立執行，不能把 Reference CI Green 改寫成 Engineering Complete。

## 17.4 硬性獨立性驗收

1. 所有現行工作指引必須直接指向本 Repo 的相對路徑；不得使用其他 SiliconForge Repository 的下載位置作為必經步驟。
2. 禁止 Git submodule / Git LFS 指標 / 機器本機絕對路徑充當唯一的內部工作檔。
3. `AGENTS.md`、`CLAUDE.md`、`CODING_AGENT_START_HERE.md`、`SiliconForge_Working_SYNC.md`、`config/`、`contracts/`、`skills/`、`src/`、`tests/`、`docs/` 均存在於此 Repo 的同一 Commit Tree。
4. 既有 A0–A6 共 60 Required Cases 加新增 E01–E20 共 20 項，合計 80，均使用本 Repo 的檔案 ID 與路徑。
5. 用 `python -m unittest discover -s tests -v` 執行 Repository Independence Tests，驗證主要入口存在、無禁止的跨 Repo 引用，以及本地 Acceptance Tracker 一致性。
6. 對於未實作的功能保持清楚的 `NOT_RUN` / `NOT_VERIFIED`，不得把搬移文件、創建 Branch 或提供 Dockerfile 當成工程驗收。
7. GitHub Actions / Coding Agent 不得透過額外 Git Checkout 另一份 SiliconForge 原始碼來讓 CI 過關；若缺少本 Repo 內的原始碼或規格就必須 FAIL。
8. 權威同步檔的 `repo` 欄位永久指向本 Repo；所有進度由此 Repo 的 Sync 網頁更新、明確區分的 Local Commit，以及實際傳遞並整合後的 Remote Commit/PR 和不可變執行證據支持。Local Commit 不能假冒 Remote Commit。

## 17.5 規格變更治理

未來 v3.2 或更高版本，必須透過此 Repo 的 PR 更新 `AGENTS.md`、`docs/10_CODING_AGENT_EXECUTION_ORDER.md`、`contracts/`、`SiliconForge_Working_SYNC.md` 並附客觀測試。不可自行建立第二份權威指令或把受限變更推送到其他 Repo。Main Agent 仍不具有工程仲裁權，Git Worktree 的設計探索是本 Repo **內部受控分支**，與跨 Repository 依賴無關。
