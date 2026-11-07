# 18｜外部 Coding Agent 的 Browser + ZIP + Local Git + Sync-only 交付協定

## 適用對象與強制優先順序

**本協定專門給目前負責 SiliconForge 實作的外部 Coding Agent。** 其能力不等同於未來 SiliconForge Super Agent Runtime 所啟動的 Domain Owner，也不等同於在本 Repo 有 GitHub Connector 的整合者。

當其他文件寫著 `git clone`、`git pull`、`git push`、建立 GitHub PR 或 GitHub Commit 時，對**這個外部 Coding Agent** 一律以本協定覆蓋。現有工程目標和 A0–A6 + E01–E20 的 80 項驗收要求不變。

## 1. 真實能力矩陣

| 功能 | 此 Coding Agent | 備註 |
|---|---|---|
| Chrome／Computer Use 開啟 GitHub 檔案、Issues、規格 | 支援 | 可以按需逐檔讀取，不能假定已自動載入 |
| GitHub Code → Download ZIP | 支援 | 取得獨立 Repo 的原始碼快照；ZIP 不含 `.git` |
| 在自己的 Local 開發、使用 Git、建立 Branch/Commit、執行測試 | 支援 | 僅作用於 Agent 的 Local，不等於 GitHub Repository 已更新 |
| 透過 Git 對 GitHub 執行 clone、fetch、pull、push | **不支援** | 不得寫入這些操作作為前置依賴 |
| 透過 Chrome／Computer Use 編輯 GitHub 的 `SiliconForge_Working_SYNC.md` | 支援 | **唯一獲准／可用的遠端檔案修改入口**；Web 編輯會在 GitHub 記錄 Sync 檔的版本變化 |
| 遠端大量更改 `src/`、`tests/`、`docs/`、PR、批次檔案上傳 | **無能力保證** | 不可視為此 Agent 已具備；程式碼上傳交由另有權限的整合執行端 |

## 2. 第一次接手，不要要求 GitHub Clone

1. 以 Browser 進入 `https://github.com/caseykcc0124/SiliconForge/blob/main/SiliconForge_Working_SYNC.md`；這是**第一優先、直接可執行的工作指引與雙向通道**。沒有本地專案也能讀。
2. 依實際可用的 Browser 能力開啟 `CODING_AGENT_START_HERE.md`、`AGENTS.md`、`docs/09_ACCEPTANCE_TEST_MATRIX.md`、`docs/14–16`、`contracts/parallel_exploration_acceptance.json`。若看不到，記錄未讀，不得聲稱完整理解所有細節；Sync 的必要任務摘要仍可先進行下一個授權步驟。
3. 需要大批程式碼時在 GitHub 網頁 `Code → Download ZIP`。將 ZIP 下載到**自己可存取的 Local**、解壓。這是完整原始碼快照，**沒有 Git 歷史，不能宣稱 ZIP 已包含所有既有 commit history**。
4. 在 Local 執行本地開發與測試。可自行 `git init`、建立 Local Branch、Local Commit；不設置或呼叫不支援的 GitHub remote。記錄 ZIP 所對應的 GitHub `main` HEAD SHA（若 Browser 可查）和本地工作目錄快照／雜湊。
5. 繼續以 Browser 修改唯一 Sync 檔，更新任務、已執行證據與下一步。**每一次 Web Sync 編輯只代表狀態同步，絕不代表 Local 程式碼已經上傳到 GitHub**。

## 3. 最低限度 Sync 回報協定

持續更新同一份 `SiliconForge_Working_SYNC.md`，使用以下欄位或等價的機器可讀段落，保留原有狀態與時間戳：
```yaml
external_coding_agent:
  transport: BROWSER_ZIP_LOCAL_GIT
  github_write_scope: SiliconForge_Working_SYNC.md_ONLY
  input_zip_baseline_sha: "<main commit SHA / UNKNOWN>"
  local_workspace_state: NOT_STARTED # ACTIVE, TESTING, LOCAL_VERIFIED, BLOCKED
  local_git_commit: null            # Local Git only; never call this GitHub Commit
  code_artifact_state: NOT_CREATED  # PREPARED_LOCAL, TRANSFERRED, INTEGRATED_REMOTE
  code_artifact_name: null
  code_artifact_sha256: null
  code_artifact_access: null         # Accessible transport channel or UNAVAILABLE
  remote_source_integrated_commit: null  # Only another authorized GitHub integrator fills after verification
  tests_executed: []
  blockers: []
  next_action: "<one executable action>"
```

更新時必須區分 `Local Code Implemented`、`Local Tests Verified`、`Artifact Delivered`、`Source Integrated on GitHub`、`Remote CI Verified`。其中任何一個前階段都不能自動推導後階段。

失敗與未實測維持原樣。若 Browser 上的 Sync 已被他人改動，先重新讀取再合併更新，避免蓋掉其他狀態。只有具有權限的 GitHub 整合執行端會向 Repo 的其他檔案提交程式，並將遠端正式 Commit SHA 更新回 Sync。

## 4. Local Code 交付與 Bridge

ZIP 作為 **GitHub → Local 的輸入通道**。要讓 **Local → GitHub 的實作產物** 成為遠端程式碼，需要額外可存取的傳遞管道：

1. Coding Agent 在 Local 將實作差異、測試程式、配置及證據整理為 ZIP／Patch Bundle，計算 SHA-256；產生 `manifest` 記錄基準 SHA、改動檔案清單、執行命令、測試結果、Real/Mock 區分。
2. 只透過實際存在且已授權的管道把 ZIP／Patch Bundle 交給**有 GitHub 檔案寫入能力的 Integrator**。例如人類將本地交付包附在對話中，再由有 GitHub Connector 的執行者檢查與提交。**不得假設 Agent 能自動傳給本聊天或 GitHub。**
3. Integrator 從 Canonical Repo 取得當前版本，檢查基準差異、排除秘密、重跑可用測試、提交程式並讀回驗證 GitHub Commit。
4. Integrator 將真正遠端的 Commit SHA、CI Run 與差異摘要回寫 Sync；Coding Agent 再用 Browser 讀回確認，必要時重新下載 ZIP 更新自己的 Local Snapshot。
5. **若缺少可用的 Local Artifact 傳遞管道，程式碼實際交付就是阻礙**。允許 Coding Agent 繼續處理它 Local 內可完成的獨立工作，但不得聲稱程式碼已同步或完成 GitHub 驗收。

## 5. 角色分離

- **外部 Coding Agent**：使用 ZIP 閱讀當前 Repo，Local Git 開發、測試，Web 編輯唯一 Sync；不負責對 GitHub Push／PR。
- **GitHub Integrator**：取得實際可存取的程式交付包後，使用自身授權的 GitHub Connector/Repo 操作發布版本，檢查 CI，回寫 Sync；不能只看 Sync 裡的文字就憑空產生程式碼。
- **SiliconForge Runtime／Domain Owner（未來產品功能）**：在正式平台內按權限使用分支、Worktree、事件與 EDA Runner；其能力與外部 Coding Agent 的 Browser 限制完全獨立。
- **人類**：僅在外部交付管道不存在、真正授權或未定設計權重時介入，不作一般 Agent Peer Message 的傳聲筒。

## 6. 驗收規範

- 本次協定的驗收是「Coding Agent 能**不執行任何 GitHub Git 指令**，依 Sync + Browser + ZIP 在 Local 開發與回報」。
- GitHub 上的 `AGENTS.md` 是未來進入專案工作樹時的規則，**不能當成遠端 Browser Coding Agent 已自動讀取的前提**。
- 80 項工程驗收依原規格不變。只有相關程式與報告真正交付、版本一致並有可追溯證據時才能 PASS。
- 此 Repo 保持獨立，不得再引入任何其他 SiliconForge Repository 作為運作依賴。
