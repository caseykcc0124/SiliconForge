# 19｜SiliconForge Supervisor Work Order：自主連續開發與動態指令通道

> **DIRECTIVE_ID: SF-DIR-20261108-01**
>
> **DIRECTIVE_STATUS: ACTIVE**
>
> **UPDATED_AT_UTC: 2026-11-07T23:25:10.380Z**
>
> **CANONICAL_REPO: caseykcc0124/SiliconForge**
>
> **SUPERVISOR_WRITE_OWNER: 監督者／授權 GitHub Integrator**
>
> **CODING_AGENT_ACK_CHANNEL: 根目錄 SiliconForge_Working_SYNC.md（GitHub Web Edit only）**

## 0. 任務與角色

這是目前**外部 Coding Agent** 的現行工作指引，與未來 SiliconForge Super Agent Runtime／Domain Owners 的執行角色分離。外部 Coding Agent 以 Chrome／Computer Use 讀取 GitHub；必要時以 **Code → Download ZIP** 取得完整 Repository；在自己的 Local 使用 Git、寫程式、執行測試；遠端只有 GitHub 網頁編輯 `SiliconForge_Working_SYNC.md` 的能力，**不能要求它 git clone、pull、push、遠端 Commit／PR 或大量上傳原始碼**。

Coding Agent 從既有 Local 工作區繼續，不要為了讀新指令而重下載整包 ZIP。Supervisor 只透過本文件變更任務方向；Coding Agent 透過 Sync 回報進度、確認指令版本與需求。**任何文件、同步文字或模型自評不構成工程驗收證據。**

## 1. 強制定時檢查指令並自動接續

在 Coding Agent 的**活躍執行階段**：
1. **每 15 分鐘**（可與 Sync Heartbeat 同一週期），使用 Chrome／Computer Use **重新載入** [本工作指引](https://github.com/caseykcc0124/SiliconForge/blob/main/docs/19_SUPERVISOR_WORK_ORDER.md)；此外，每次完成 Gate、出現 BLOCKED、重啟 Session、打算轉入新里程碑前，立即再讀一次。
2. 比較文件頂部 `DIRECTIVE_ID` 與上次在 Sync 記錄的 `last_seen_directive_id`。如有新版本，讀取全文並對照當前 Local Commit、已通過 Gate、阻礙與剩餘任務；**在安全檢查點套用新指令**，不毀掉已完成工作，不重跑沒有受影響的整套開發，不擅自放寬測試。
3. 使用 GitHub Web UI **只修改** `SiliconForge_Working_SYNC.md`，回報 `last_seen_directive_id`、`directive_ack_at_utc`、`directive_application_state`（APPLIED、PENDING_SAFE_CHECKPOINT、REJECTED_POLICY_CONFLICT）與摘要、目前 Gate、Local tests、Last effective progress、下次行動。即使指令無更新，也維持 Heartbeat，但**只有真實工程進展才更新** `last_progress_at_utc`。
4. 若指令無更新：**持續執行目前 Gate 與已授權的下個 Gate，不要停下等待 Supervisor**。
5. 若 Browser 重讀失敗：紀錄 `directive_poll_state=FAILED` 與錯誤、重試有限次；繼續不依賴新指令的已授權 Local 工作，無法確認新授權的操作則不可擅作。
6. 若 Agent Harness **不支援在沒有活躍 Session 時執行排程或保持輪詢**，必須如實寫 `polling_mode=ACTIVE_SESSION_ONLY`。不可聲稱已建立 Always-on 服務、背景 Timer 或持續監督。允許它使用自身已授權的本地 Timer/Loop 於活躍執行期輪詢，但不得增加新框架維持常駐。
7. 如 Supervisor 指令與 `AGENTS.md`、安全 Policy、使用者核可、這份 Transport Contract 衝突，標 `REJECTED_POLICY_CONFLICT` 並指出衝突，執行仍合法的其他工作；不允許靠動態指令繞過 Policy。
8. **只有 Supervisor／授權 Integrator 修改本文件。外部 Coding Agent 不應在 GitHub 編輯本文件**。Supervisor 改本文件時一定遞增 `DIRECTIVE_ID`，保留主要決策摘要與有效里程碑。不直接編輯 Agent 回報欄位，以免競爭覆蓋。

## 2. 本輪立即工作：從 Local A0 收斂，避免測試無限擴張

上次 Sync 記錄：Local Git `c5f3194` 乾淨版本 18/18 A0 ID 與 67/67 Local suite，後續未提交修改 79/79 suite 與 18/18 A0 ID，Peer Lifecycle、Ingress、Immutable Journal 的 Review 尚未正式閉合；Local 產物尚未製作，無遠端 Source Integration。

**A0-CLOSE（本輪第一優先）**：
1. 從上次 Local 工作區恢復，清點 Dirty Diff 與已完成的審查；只處理真實發現的缺陷或未覆蓋的正式 A0 契約。禁止為了追求更多測試數量自行延長 A0。
2. 合併 Review 修正，確認 Peer Reply／Refusal／Expiry、WAITING 狀態、過期 Lease ACK 拒絕、Replay、Ingress AuthZ、Scope 隔離、失效 Evidence 拒絕、Watchdog 與重啟。
3. 固定一個新 **Local Commit**，記錄真正的 Local SHA、Input ZIP Baseline SHA、Runtime/Policy/Test SHA256；在隔離乾淨 Local Worktree 或 Snapshot 重跑 `A0-01..A0-18`、完整 stdlib suite、必要 fault injection。若有 FAIL，最多三次相同失敗簽名的修復迭代，仍無有效進展就停止該子問題、保存可重現證據、轉處理不依賴它的工作。
4. 請獨立 Reviewer 明確檢查通過標準；不允許僅由實作者文字自評 PASS。A0 成立條件是 18/18 Case 符合證據契約且完整測試真實通過，不能以「79/79」替代。
5. 製作 `SiliconForge_A0_<localSHA>_source_evidence.zip` 或完整 Patch Bundle：包含 changed source、tests、config、完整 raw logs、`manifest.json`、SHA256、input_zip_baseline_sha、Local Commit 與重跑命令；在 Sync 標 `PREPARED_LOCAL`。**有產物不代表已傳到 GitHub**。
6. 如果沒有實際可取得的 Local → Integrator 傳輸管道，在 Sync 標 `artifact_transfer_state=UNAVAILABLE`、`remote_source_integrated_commit=null`。**不因這項外部傳輸阻礙停止 Local A0X 等可獨立繼續的開發**；但不能稱 A0 已 Remote Verified。

## 3. 後續里程碑，自主往前，不用等待人工分派

| Gate | 工作範圍 | 本地完成證據與自動移轉 |
|---|---|---|
| **G0：A0 CLOSE** | 關閉 18 個 A0 ID、獨立 Review、固定 Local Commit、交付包 | 所有 A0 正式契約通過、原始 Logs/Hash、Reviewer Sign-off、Local Bundle；完成立即進入 G1 |
| **G1：A0X / E Runtime** | Exploration / Branch Registry、Owner Role 與 Instance 分離、多同 Role Instance、Candidate-scoped Routing、Durable Fan-out/Fan-in、Lease Epoch、Quota、Lineage DAG、Crash Replay | 在本地用可執行單元/失效注入證明 E01–E08 適用的 Runtime Contracts；Fake EDA 只能標 MOCK；完成進 G2 |
| **G2：A1 / MCP & Harness** | native Codex / Claude Code + MCP/Skills、AuthZ、Session 換裝、持久化通知，不自造聊天 CLI | 原 A1-01..A1-08 逐項真實 Harness 證據；不可達的外部 Harness 需具體標示，不可用 Mock 替代；獨立可行工作可平行進 G3 前置準備 |
| **G3：A2 / Real EDA** | Environment Owner pin tools、APB CRC32 golden model、Verilator/cocotb、Formal、Yosys/netlist 等真實工具 | 原 A2-01..A2-07 的實際工具與 profile/spec/source hashes；授權或無法安裝阻礙不阻止其他 Local 模組準備 |
| **G4：A3 + A3X** | RTL/Verification/Formal 多 Owner Instance、Git Branch/Worktree 隔離、真實 defect→repair→verify、Lease/Wakeup/Peer | 原 A3-01..A3-07、E09/E10 與相關隔離/重啟證據。Local Runtime 所管理的 Branch 不需要此 Coding Agent 具有遠端 Push 權限 |
| **G5：A4 + A4X** | 同一 Requirement 三路 Performance/Power/Area 真正重疊探索、一次 Nested Fork、候選個別 Simulation/Formal/Synthesis/PPA、Pareto、Merge Conflict、合併後新 SHA 重新驗證 | A4-01..A4-06；E11–E18 與 E20，必須有真實可比較 EDA 報告和 Merge 版 Evidence。沒有合理 Power 證據顯示 INCOMPARABLE，不自行宣稱通過 |
| **G6：A5 + A5X** | Event Journal Replay、Dashboard DAG、Owner/Branch/Evidence/Cost Trace、PDCA、通知 | A5-01..A5-07 及 E19；DAG 查詢完整可追溯，失敗候選也保留 |
| **G7：A6 + A6X** | 多分支 Chaos、長期 Restart/Crash、No-progress Watchdog、資源公平、安全與 Scope Gate | A6-01..A6-07、E20 回歸及剩餘全部 Required，逐 Case 回報。**全專案遠端完成**還需實際 Source Bundle 交付、Remote Integration、CI 與適用真實 EDA Gate，不能靠 Local Sync 自評 |

**自動推進政策**：每個 Gate 的 Local 實作與驗證完成即可轉入下個不依賴遠端發布的 Gate；未達正式 Gate 不能把它升格 `VERIFIED`。依賴可並行，不做一關卡卡死全專案。正式全體 80 Required Cases 不降低、不自行擴充成無限測試清單，也不擅改架構、Autonomy Policy 或批准權限。

## 4. 有限失敗處理與資源治理

- 相同 Failure Signature 連續三輪未有新證據就停止當前 Ticket，記錄 Root Cause、Attempts、Evidence、已驗證替代路徑，繼續無關的其他任務。
- `WAITING_FOR_TOOL`／`WAITING_FOR_ENV` 只能用在具體工具、版本或權限問題，禁止以「Agent 不知道怎麼做」作為無限 Blocker。
- 預算沿用 Local 既有 Policy；不得自改 Token/EDA quota、框架尺度、Test Gate、使用受限 PDK 或未授權外部連線。
- 負責工程 Owner 應自行解決同 Role 多 Instance 的局部問題；Main 只傳達監督意圖，不在每個 Peer Request 中轉。
- 不要求 Coding Agent 持續維持無產出的迴圈或憑空發明 Background Always-On Runtime。

## 5. 每 15 分鐘 Sync 欄位，重大事件立即回報

**Coding Agent 只透過 Chrome 編輯唯一的 `SiliconForge_Working_SYNC.md`，保留既有 Agent Status 與歷史，不要覆寫其他 Writer。** 推薦新增／更新以下區塊：

```yaml
supervisor_coordination:
  directive_url: "https://github.com/caseykcc0124/SiliconForge/blob/main/docs/19_SUPERVISOR_WORK_ORDER.md"
  last_seen_directive_id: SF-DIR-20261108-01
  directive_poll_at_utc: "<actual UTC>"
  directive_ack_at_utc: "<actual UTC>"
  directive_application_state: APPLIED
  polling_mode: ACTIVE_SESSION_ONLY # or SELF_MANAGED_TIMER only if actually supported
  active_gate: G0
  gate_state: ACTIVE
  local_git_commit: "<actual Local SHA>"
  local_test_evidence: []
  local_artifact_state: NOT_CREATED # PREPARED_LOCAL / TRANSFERRED / INTEGRATED_REMOTE
  artifact_sha256: null
  artifact_access: UNAVAILABLE
  remote_source_integrated_commit: null
  blocked_items: []
  next_executable_action: "..."
  last_heartbeat_at_utc: "<actual UTC>"
  last_effective_progress_at_utc: "<actual UTC, only update on evidence>"
```

**必須回報**：每次 Gate 啟動／完成、Local Commit、真實測試新結果、重大缺陷、阻礙、指令版本改變、Artifact Ready、遠端 Integration、Session 停止。一般在活躍執行期間至少每 15 分鐘檢查一次指令並更新 Heartbeat；不活躍時不能偽造輪詢。若無實質改變，不要把 Heartbeat 或重新跑同一套測試當新工程進展。

## 6. Supervisor 的定時監督與指令修改責任

Supervisor 每兩小時巡檢**本 Repository** 的 Sync、最新 GitHub Commit/CI 與本指引的版本，並和前次狀態比對：
- 當看到 Gate 合法閉合、真實新阻礙、重複失敗、交付渠道變更或需求有新的決策，**由 Supervisor 更新這份 docs/19 文件並遞增 DIRECTIVE_ID**，Coding Agent 下次主動輪詢即可接收，不需要人類轉達。
- 更新只限安全且已授權的目標排序、下一階段、故障恢復及 Reviewer 的查核重點；**禁止自動降低測試 Gate、擅自核准公開發布、增加未授權外部工具或改變原架構意圖**。
- 除明確需要人類批准外，Supervisor 不要求人類重複搬運同一任務；若沒有重大改變，**不要製造新版本或打斷 Coding Agent**。
- Supervisor 不編輯 Agent 擁有的 Sync Status 區塊；Agent 不編輯 Supervisor 擁有的 docs/19 指引。若指令已更新而沒有 ACK，下一輪巡檢提醒或分類為執行能力限制。
- 此監督是 GitHub 可觀測層，不是 Runtime 可以直接喚醒外部 Coding Agent 的保證。若沒有活躍 Harness Session，定時讀取指令需等 Session 恢復。

## 7. 絕對禁止的完工宣稱

不得以 README/AGENTS.md/本指引更新、GitHub Sync Web Commit、Local Git Commit、79 個 Local Unit Tests、三個假平行 Worker、模擬 EDA、漂亮 Dashboard、或 A0 Mock CI Green 當成正式 SiliconForge Release。每個驗收結論必須回到 `docs/09_ACCEPTANCE_TEST_MATRIX.md` 和 `docs/15_PARALLEL_EXPLORATION_ACCEPTANCE.md`，並有對應版本的真實 Raw Evidence。

**此工作指引的預設下一動作**：Coding Agent 恢復工作時立即確認本 Directive，先完成 G0 A0 CLOSE，再自主推進 G1 A0X，之後依 Gate 表繼續，不必等人逐段傳令。
