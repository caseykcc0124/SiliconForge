# 19｜SiliconForge Supervisor Work Order：自主連續開發與動態指令通道

> **DIRECTIVE_ID: SF-DIR-20261108-12**
>
> **DIRECTIVE_STATUS: ACTIVE**
>
> **UPDATED_AT_UTC: 2026-11-08T12:57:08Z**
>
> **CANONICAL_REPO: caseykcc0124/SiliconForge**
>
> **SUPERVISOR_WRITE_OWNER: 監督者／授權 GitHub Integrator**
>
> **CODING_AGENT_ACK_CHANNEL: 根目錄 SiliconForge_Working_SYNC.md（GitHub Web Edit only）**
> **CURRENT MISSION PRIORITY: 全功能實作成果已回報；現在優先依 §2.13 打通真實 Select→Merge→ReGate，測試僅限必要阻斷點，正式80項保持待驗收。**


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

## 2. 本輪最新工作指示：先交付可使用的開發版本（DEV），避免測試框架循環

**2026-11-08 使用者決策，優先於本文件較早的 A0-CLOSE 順序描述：SiliconForge 目前製作的是可使用、可展示、可交付的開發版本，不以一開始達到量產等級為目標。** 以真正能跑通的功能、取得實際產物、可重現的操作流程衡量進度。Coding Agent 不得將持續增加測試、回歸案例、Reviewer 次數、治理框架或 Mock PASS 數量當成主要交付目標。這項優先順序調整**不降低**既有 A0–A6 60 項與 E01–E20 20 項 Required Acceptance、既有安全 Policy、授權要求或正式 Release 門檻。

**已知基準（僅 Sync 聲稱，尚未取得 Local 原始檔重驗）：** G0 本地已閉合；G1 的 Scope、Candidate、Watchdog、Typed Commands、ArchiveBranch 及 Failure Receipt 等子單元由 Agent 回報本地凍結，最新 Local Git `9bb2677`，137/137 Local Suite、18/18 A0 IDs PASS；Local Bundle 已製作但傳遞仍為 UNAVAILABLE，remote_source_integrated_commit=null；正式 Native Harness、Real EDA 與 E01–E20 無完成證據。不要為了照本節舊文字重新做 G0，也不要把本地數字視為遠端驗收。

### 2.1 立即執行順序：可用成果優先

1. **停止以 G1 細項無限延伸為預設工作模式。** 先固定目前已收斂且無已知重大缺陷的 Local 基準。僅修正會使最小端到端流程無法執行、造成資料／權限越界、不可恢復錯誤、或妨礙必要證據的實際缺陷；其他 G1 增強（例如完整實際 Usage Accounting、進階 Registered-job Retry、額外框架抽象化）除非證明為最小可用流程的硬性依賴，先記錄 Backlog，不以其全部完成作為開始整合的前提。若發現真正的安全漏洞或必要政策 Gate，不能略過。
2. **優先建立一條可重現的 Vertical Slice：** 使用既有 Runtime 接受一項 APB CRC32／RTL 修復工作，經由**真實 Codex 或 Claude Harness**（使用現有授權方式，非 Fake/Mock）、產生 Local RTL 修改與 Commit、執行**實際可合法使用的 EDA 工具**（例如已安裝或合法可用的 Verilator，依現有環境與權限選擇），保存 FAIL → 修復 → 重跑 PASS 的原始輸出及版本關聯。先做單一 Task、單一 Owner 最小閉環，再擴至多 Owner、分支與 PPA。不要為了第一個 Demo 先建置全新 Agent 框架、完整 Dashboard 或額外大型測試平台。
3. **若真實 Harness 或 EDA 尚不可用：** 優先依 §2.4 在既有權限內啟用合法開源 EDA；若仍不可用，立即以具體命令、環境、所缺工具/權限與重現結果記錄阻礙，不擅自提升權限、違反政策或用 Mock 冒充。可先交付能在 Local 啟動的 Runtime 加明確標示 `DEV_MOCK_DEMO` 的示範流程，但不得標 `DEV_USABLE_E2E`、A1/A2 PASS 或 Real EDA Verified。同步執行其他已授權、與工具阻礙無關的實作。
4. **每一次開發交付必須有可以使用的實體成果：** 可啟動的 Code、清楚的入口命令及 README/操作步驟、固定 Local SHA、必要設定/依賴、實際 Sample Input/Output、已執行的最小重現與原始 Logs、已知限制，以及 Source + Evidence ZIP/Patch Bundle 與 SHA256。優先讓 Reviewer 從乾淨 Local Snapshot 使用文件中的命令重現功能。若只有 Spec、Mock 報告、測試清單或 Sync 心跳，標示 `NO_USABLE_DELIVERABLE_YET`。
5. **Local → GitHub 交付明確分離：** Coding Agent 只能本地製作 Bundle 並用 GitHub Web Edit 更新根目錄 Sync。傳遞管道若仍 `UNAVAILABLE`，正確標記 `DEV_LOCAL_ONLY_PENDING_TRANSFER`，不可宣稱 `DEV_DELIVERED_REMOTE`；由有權 Integrator 真正拿到檔案、核對 SHA256 並提交遠端 Source Commit 後，才可進行遠端 CI/驗證。不能讓 Coding Agent 嘗試遠端 Git、PR 或批次上傳。
6. **最小開發版驗收（與正式 80 項分離）：** 僅在第三方可用相同 Local 原始碼、設定和可用工具重現前述真實 Harness + RTL 修改 + 真實 EDA 結果時標 `DEV_USABLE_E2E_LOCAL`；若已由 Integrator 真正整合並重現，標 `DEV_DELIVERED_REMOTE` 並記錄 Commit/CI。這是開發版使用性檢查，**不取代、減少或自動通過任何正式 Acceptance ID**。發布或宣稱量產就緒仍需既有全部適用正式 Gate；未授權不得公開發布。

### 2.2 測試與 Review 收斂規則

- **測試是證明功能的工具，不能自行成為任務目標。** 每個新測試必須直接綁定一個實際修復的缺陷、一項已實作的外部可觀測行為、一個既定 Required Case，或阻止交付的明確風險；否則先不新增。禁止為了提高 PASS 數而設計新框架、重構測試架構或增加無界矩陣。
- 一般工作先跑受影響模組的必要回歸，於**固定交付 Revision／Gate 轉換／真實整合前後**執行完整既有回歸與必要驗收。若出現新 FAIL，按同一 Failure Signature 最多三次修復迭代原則處理；不要對完全未受影響的模組反覆全量重測。
- Reviewer 以「可使用功能、真正阻斷交付的缺陷、安全問題、可重現性」作優先順序；不因細枝末節或新提出的測試喜好無限延長開發版交付。Reviewer 發現實質高風險缺陷則必須阻擋相關功能的 PASS，不得遮掩或降低 Gate。
- 每次 Sync 與 Supervisor Dashboard 的**首要 KPI**：可實際啟動的功能、端到端工作是否真正執行、真實工具與證據、可取得的 ZIP/Patch、遠端 Source Integration、阻礙與下一步。Local Test Count、Agent 活動數、Mock PASS、Heartbeat 僅為輔助指標。

### 2.3 明確的開發版標籤

交付標題、README、Bundle manifest、Sync 摘要與報告中，必須清楚標註：
- `DEVELOPMENT VERSION / 開發版本，非量產版`；
- `DEV_MOCK_DEMO`、`DEV_LOCAL_ONLY_PENDING_TRANSFER`、`DEV_USABLE_E2E_LOCAL`、`DEV_DELIVERED_REMOTE` 中**有證據支持**的實際能力／交付狀態，勿把「已製作 Local ZIP」當成已交付；
- 哪些地方仍依賴 Mock／Stub，哪些 Native Harness、真實 EDA 與 80 項正式驗收尚未執行；列出已知限制與後續工作；
- 若 `DEV_USABLE_E2E_LOCAL` 不成立，直接說明尚未能完整使用，禁止用測試總數代替。

### 2.4 使用者新決策：EDA 先採免費開源工具，保留商業替換能力（2026-11-08）

**使用者已決定：開發版本優先使用免費、開源、合法可用的 EDA，立刻排除「尚未採購商業工具」作為第一個可運作 Demo 的等待理由。未來可以換接商業 EDA，但現在不得為了抽象相容性開發大型 Framework。**

1. **優先工具與安裝路徑。** Coding Agent 應優先選用 YosysHQ **OSS CAD Suite** 官方 Windows x64 封裝（https://github.com/YosysHQ/oss-cad-suite-build/releases），因目前 Local 是 Windows、WSL 未安裝。先用其中 **Icarus Verilog 或 Verilator** 對 APB CRC32 RTL 做真實編譯、Testbench、Bug Reproduction、修復與 Regression；以 **Yosys** 做最小可執行的 Synthesis Smoke；Formal 若本次需求確實需要、且工具已可用，再用 **SymbiYosys/SBY + 可用的開源 Solver**。cocotb 可用但不是第一版必要前提。不要求為了選工具建置新測試平台、搭建 WSL、購買 License 或等待商業 EDA。
2. **使用授權邊界。** 本決策授權採用上述免費開源工具，在 Coding Agent **現有本機、現有合法權限及原有工具／連線政策允許的範圍內**，從官方來源下載並以使用者目錄的 portable 解壓方式供本開發任務使用；先核對供應來源、發行檔 SHA256、適用 License、實際版本／環境。**不授權**管理員權限、系統全域安裝、變更防火牆或公司 Policy、接觸受限 PDK、增加 Token/EDA 額度、使用未核准商業 License 或把開源原始碼／專案內容對外公開。如果 Local 政策禁止下載／執行、需提高權限或無法驗證可信來源，具體回報當前阻礙與實際嘗試，不得假稱已裝好。
3. **先跑一條真實可重現的最小流程。** 不等待 G1 進階 Accounting/Retry：使用已存在的 Native Codex/Claude Harness 在 Local 產生或修改 APB CRC32 RTL，保存修改前真實 EDA FAIL、Local Git 修復 Commit、修改後真實 EDA PASS，並保存 Verilator/iverilog/Yosys 的實際 CLI 命令、exit code、標準輸出與錯誤輸出、工具版本、RTL/Golden/Testbench SHA、環境與 Bundle SHA256。測試只需覆蓋足以說明這條流程和既有硬性 Gate 的必要案例；完成後即產生 **DEVELOPMENT VERSION / 非量產版** 的可啟動交付包。若只能做到部分流程，逐段標 `NOT_RUN`／`BLOCKED`，不得填寫不存在的 EDA PASS。
4. **保留輕量、可替換的 EDA Tool Adapter。** Runtime/Domain Owner 只透過一份穩定的 EDA Request/Result Contract 呼叫工具；由配置 Profile 指定 Provider、執行檔路徑、命令模板、版本、Timeout、Input／Output 路徑和可選的 Corner/Constraint。Result 至少記錄 run/job ID、project/branch/candidate/source SHA、Spec/Golden SHA、Provider+Tool Version、完整執行命令、Exit Code、PASS/FAIL/BLOCKED/NOT_RUN、原始 Log/Result Paths 與 SHA256、Environment Digest。第一版只做**一個** OSS Provider 與必要的極薄 Adapter，不先實作沒實際工具可驗證的商業 Provider；在設計和範例配置中預留未來的 **VCS/Questa/Xcelium** Simulation、**Design Compiler/Genus** Synthesis、**JasperGold/VC Formal** Formal Provider。
5. **證據不可跨工具偽造。** 開源 EDA 的真實執行結果可作為開發版的真實工具證據；它不會自動等價於特定商業 Toolchain 的 Timing、Power、Area、Formal 能力或流片資格。未來換用商業 EDA 時，必須使用該工具重新跑適用案例，記錄 License、Library、Corner、Constraint 和工具版本，不能沿用不同 Provider 的 PPA PASS 或 Merge ReGate 結論。
6. **Sync/交付記錄。** Coding Agent 下次輪詢 ACK 本 Directive，於 Sync 回報 `eda_provider=OSS_CAD_SUITE`（僅實際可用時）、本地安裝或解壓是否完成、各工具 `--version` 實際輸出、真正執行過的命令與原始 Logs、可跑通的 Vertical Slice 階段、未完成的步驟、Blocker 和下一步。Local ZIP/Patch 仍須按現有 Transport Contract 處理；可交付的功能性成果優先於增加測試計數。

### 2.5 開源 EDA 取得失敗的有限恢復方案（2026-11-08）

**觸發證據：** Coding Agent 已依 Directive 03 經 Chrome 從 YosysHQ 官方 GitHub Release 下載 Windows x64 OSS CAD Suite（約 577 MB），兩輪下載均停在約 1.25 MB，Pause/Resume 與新下載仍未成功；未取得完整可驗 SHA256 的 Archive，也未執行任何實際 EDA。最新本地 `8f084ed` 已有 APB CRC32 defective RTL/Golden/Testbench、薄型 EDA Profile/Request/Result Adapter 與可執行但實際工具缺席的開發版本，Bundle 仍僅本地可存取。

1. **立即停止對同一個 577 MB GitHub Asset 的無界重試。** 先查明 Chrome 的實際 Download 狀態、Disk Space、是否遭瀏覽器／權限／網路限制。在現有瀏覽器讀取與下載權限內，可有界嘗試官方供應者提供的另一個已驗證完整版本、官方鏡像或更小的獨立 **Icarus/Verilator** Windows Binary；必須核對官方專案／維護者來源、平台、License、SHA256、工具版本並實際執行。不要把「Source Tarball 下載成功」當作已具有可執行 EDA，亦不得使用未經允許的第三方安裝程式、非官方鏡像、系統管理員權限、改變防火牆、WSL 部署或未批准的下載方法。
2. **恢復先做最小可用閉環。** 若取得可信任的 Icarus 或 Verilator，可**先完成真實 RTL FAIL → Codex/Claude 修復 → 真實 RTL Simulation PASS**，再取得 Yosys 執行 Synthesis；如缺少 Synthesis，將該階段標 `NOT_RUN`，整體 `DEV_USABLE_E2E_LOCAL` 仍不得宣稱完成。無需先建好完整 Toolchain、Formal、PPA、多 Branch 或新測試框架才開始已可執行的部分。
3. **工具仍不可取得時，停止該下載 Ticket 並準確上報。** Sync 必須回報 `EDA_TOOL_ACQUISITION_BLOCKED`、失敗嘗試次數、完整錯誤/下載證據、已評估的合法替代途徑、下一項真正可執行的工程動作，與**明確待人工協助的取得方案**，例如由有權環境以原始官方 SHA256 供應離線 Archive 或開通既有允許的 Artifact Transfer。此類人工協助屬待核可事項，Coding Agent 不得自行宣稱已有傳輸能力。其餘不依賴 EDA 的原有薄型整合與交付文件維持可重現，禁止再以增加 Local Tests、Retry 或抽象化框架消耗空轉。
4. **標示開發版與正式證據的區別。** `PARTIAL_DEV_TOOL_BLOCKED`／`DEV_LOCAL_ONLY_PENDING_TRANSFER` 可作客觀交付狀態，但不能記成真實 EDA PASS、A1/A2 或 E Case PASS，也不能把 Sync Web Commit 當原始碼整合。G0–G7、80 項驗收與所有既有安全及傳輸限制維持。

### 2.6 GitHub Release 分片離線 EDA 已上架，恢復可用功能優先（2026-11-08）

**可核實的新外部交付條件：** 使用者已由其有權環境上傳並正式發布 [SiliconForge OSS CAD Suite Windows x64 開發工具 Release](https://github.com/caseykcc0124/SiliconForge/releases/tag/eda-oss-cad-suite-20261107)，GitHub Release tag `eda-oss-cad-suite-20261107`；GitHub 元資料顯示 **59 個 Assets 均為 uploaded**，名稱為 `oss-cad-suite-windows-x64-20261107.z01` 至 `.z58` 全部連續、加最後的 `oss-cad-suite-windows-x64-20261107.zip`。其中 z01 大小 10485760 bytes、GitHub Asset SHA256 `80ff68fb2b174cd93d740bc946782b4ce2355b064937750805c1d6ad0790c9d9`；末卷 zip 大小 3174935 bytes、GitHub Asset SHA256 `617fad027f5db1346ec5e91c2b4dc0056fc367dfafc9e54a2ec76351a951bf0c`。**這僅證實 GitHub 上有可下載的分片清單，尚未證明受限 Coding Agent 成功下載、重組、執行或原始 Archive SHA 正確。**

**立即工作指令，取代 §2.5 對 577 MB 原始大檔重試的下一動作：**

1. **在活躍 Session 以 Chrome／Computer Use 瀏覽上面的正式 Release URL，優先做小規模可達性測試。** 先下載末卷 `oss-cad-suite-windows-x64-20261107.zip`（約 3.0 MiB），再下載 `oss-cad-suite-windows-x64-20261107.z01`（10 MiB），兩份都核對檔案實際存在、大小及上列 SHA256（Windows PowerShell `Get-FileHash -Algorithm SHA256`）。若其中任一份受到政策限制、傳輸超時或未完整下載，採有限次恢復後記錄 Browser/Download 原始錯誤，**不要立刻發起其餘 57 份下載**。不得以修改下載域名、外部網路腳本、Proxy 或規避政策方式突破。
2. **小樣本成功才完成全部分片下載。** 使用同一 Release 的 Assets，從 `.z01` 依序至 `.z58` 與末卷 `.zip` 下載到**同一個本地目錄**，逐一檢查無缺卷、無重名、實際位元組數與 SHA256；必要時以 GitHub Release 頁面或瀏覽器查閱該 Release 的 Asset Metadata/個別 SHA。下載權限僅限已授權的 Browser/Computer Use，不能要求 Remote Git/PR、程式化未核准下載或擴大權限。
3. **使用既有合法可用、支援 Multi-volume Split ZIP 的本地解壓工具**（例如環境已裝的 7-Zip）從末卷 `oss-cad-suite-windows-x64-20261107.zip` 啟動重組／解壓，保留所有 `.z01`～`.z58` 同目錄；可用 `7z x "<path>\\oss-cad-suite-windows-x64-20261107.zip" -o"<target>"` 作為現有 7-Zip 的示例，實際工具可用性先確認。**不要把它當單純分割 raw `.tgz` 用 Copy/Concat 隨意拼接，也不要只對 `.z01` 解壓。** 若缺少支援分卷 ZIP 的解壓器，明確回報缺少的工具，不能擅自管理員安裝。若重組會產生原始 `oss-cad-suite-windows-x64-20261107.tgz`，對產物核對 YosysHQ 官方原始 SHA256 `3d7f21c829cce34fd79eb61f72aedb462877bb08d6ca307e5a562cf04e6e5bf0`，不符則停止執行並回報。
4. **完成完整可信工具驗證後才實際執行 EDA：** 檢查原始工具包 License、解壓、`iverilog`／`verilator`／`yosys` 可執行版本和實際 PATH/Profile，使用已完成的 Local `8f084ed` APB CRC32 fixture/薄型 Adapter，先實際跑出 baseline FAIL，再透過已授權 Native Codex/Claude 修復 RTL，執行 Simulation PASS、能跑的 Yosys Synthesis，記錄實際版本、命令、exit codes、Raw Logs、Local Git SHA 和證據檔 SHA256。必要的測試與安全 Gate 保留；**不得再擴張測試框架或重新建大型抽象層**。與商業 EDA 相容只保留既有輕量 Provider/Profile 設計。
5. **成果回報與權限邊界：** 於根目錄 Sync 以 GitHub Web Edit 回報最後看到的 Directive ID/ACK、分片是否下載完整、分卷數、雜湊結果、`eda_provider`/版本、實際 RTL↔EDA 結果、最新版 Local SHA/交付包及必要 blocker。保留 `DEVELOPMENT VERSION / 非量產版` 標籤。這個 GitHub Release 是**工具配送路徑**，不能擅自改寫 `artifact_transfer_state` 為專案 Source Bundle 已可傳遞；`remote_source_integrated_commit` 沒有實際 Integrator Commit 仍為 null。不得以 GitHub Sync/Release/Mock CI 當正式 80 Required Case PASS。若 Coding Agent Session 不活躍，只有下次啟動並輪詢指引後才能接續，Supervisor 不得假稱遠端 Agent 已被強制喚醒。

### 2.7 開發版下一階段：固定 Demo 已跑通，收斂為可重複使用的功能（2026-11-08）

**有根據的新進展：** Coding Agent 在根目錄 Sync 回報，已 ACK Directive 05，59 卷 OSS CAD Suite 於本機解壓並可執行 Icarus/VVP/Yosys；本地 H0 `8f084ed` 的 CRC32 缺陷重現為預期 FAIL，Native Codex 實際修改 RTL 產生 H1 `21ec027012bab629561a53c02b64b49d26499b91`，修復後模擬 PASS、Yosys 結構檢查 PASS，第三方於 Local Git Archive 回報獨立重現；開發包 `SiliconForge-DEV-REAL-21ec027.zip` SHA256 `81fbb9b2c13db4e5a19f6cdb091d2e3b68fac4da961c05198864e1d95082bb7b`，**仍僅 LOCAL_WORKSPACE_ONLY，Supervisor 未取得原始碼/Logs 重驗，遠端 Source 未整合**。最小單次 Demo 已有實體成果，請勿重新追求額外單元測試數量，亦不得把固定 Demo 當多 Owner／全流程正式驗收。

**下個可執行工作（使用現有權限與架構，不新增大型框架）：**
1. **由固定示範改為可設定的開發工作流程。** 使用目前既有 Runtime、Native Codex/Claude Harness、精簡 OSS EDA Adapter 與已合法可用的工具，提供可重複的最小任務入口。把 Requirement／Spec、RTL 檔路徑、Testbench／Golden、工作目錄、EDA Profile 與必要輸出位置做為明確輸入，避免只對硬編碼 `SOFTWARE_CLEAR_CARRYOVER` 範例成功。至少在本地用**另一個實際可觀測的 RTL 故障／修復情境**展示：接受任務 → 產生修復 → Simulation 檢查 → 保存源碼版本、原始 Logs、結果。以功能可重用性為目標，非新加測試框架或擴建通用調度平台。若既有 API 已足夠，只需寫最薄的實際入口／操作指南，不進行重構。
2. **逐步連接真正 Domain Owner 使用流程。** 先完成單一真實任務的「Request／Owner → Native Harness → RTL Edit → EDA → Evidence → Runtime Completion」可重現鏈路；若仍使用 `MODE_MOCK` Branch Head 或 unauthenticated MCP development stub，於報告標示確切 Mock 範圍，不能說已完成多 Owner、正式 Authenticated Gateway 或 A1–A3。之後才進入同 Role 多 Instance、Branch DAG、PPA、Merge/ReGate 的原有 G4–G7 目標。
3. **只做必要功能驗證。** 保存一個乾淨 Local Snapshot、版本／工具簽章、成功與失敗的原始輸出及 Reviewer 重現方法；保留原來已有的 80 Required Cases 與安全 Gate，對此次未動到的模組不無端擴充回歸。完成真正能重複執行的功能才記 `last_effective_progress`，測試數、模型活動和 Heartbeat 不是交付。
4. **立刻區分工具配送與專案成果交付。** GitHub Release 的 59 個 EDA Assets 僅能證明工具送達，不能當作 Coding Agent 的開發 Source Bundle 已送達。請在 Sync 記錄已完成的本地開發版 ZIP、大小、SHA256、完整目錄、重現命令及所需 Integrator 操作，並具體回報目前 `artifact_transfer_state=UNAVAILABLE` 的受限點；**不得自行嘗試 Remote Git、PR、Binary Upload、外傳或增權**。沒有可供 Integrator 存取的檔案及 GitHub 真正 Source Commit，`DEV_DELIVERED_REMOTE` 與正式 CI/80 Cases 都不能晉級。
5. **保留供應鏈事實邊界。** 目前 Agent 自述 59 卷本地可執行，但依 Sync 原始官方 `.tgz` SHA256 並未重驗，只有分卷最末 ZIP 的 Profile pin。應在交付中照實標示 `OFFICIAL_ORIGINAL_ARCHIVE_NOT_VERIFIED`，無原始字節證據不得宣稱官方 Archive 完整 Hash 已核對；如不需新授權且能從現有文件/工具核對，可補實際驗證，不得宣稱自己執行過未實作的檢查。不得降低安全要求或正式驗收證據門檻。
6. **停止條件與報告。** 若第二個實際工作流程被外部權限、工具、Source 交付或必要安全條件卡住，有限次重現並回報可複製的錯誤與確切人工核可需求。可持續處理其他有直接開發版使用價值的工作；不反覆新增抽象層或測試以填補阻礙。每次本地交付均標 `DEVELOPMENT VERSION / 非量產版`、`DEV_USABLE_E2E_LOCAL`（僅有確實可重現的範圍）及 `DEV_LOCAL_ONLY_PENDING_TRANSFER`（若仍受限）。

### 2.8 Local-only 開發交付與 80 案驗收對帳（使用者澄清，2026-11-08）

**最高優先澄清：這一輪 Coding Agent 只須在自己的 Local 交付能使用的開發版本。使用者從未要求它將 Source Bundle 上傳 GitHub。過往各節中 Source Transfer/Integrator/Remote Integration 被列為開發進度阻礙或本輪待辦的語句全部撤銷；本節優先適用。**

1. **Coding Agent 有限權限**：只使用 Chrome 讀取正式 GitHub、下載授權的工具 ZIP；GitHub Web Edit 僅限根目錄 SiliconForge_Working_SYNC.md。可在自己的 Local Git、寫程式、執行 EDA 和測試、產生 Source/Evidence ZIP 與 SHA256。禁止要求遠端 Git/PR、上傳 Source、建立 Release 或找 Integrator。Local 可用功能及可重現交付包就是本輪開發版成果。
2. **遠端不是本輪阻礙**：artifact_transfer_state=UNAVAILABLE、remote_source_integrated_commit=null、Local-only 仍須如實保留，但只是已知環境限制，不得列作 blocked_items、human_approval_required、next_executable_action，亦不能要求人類搬移 Source。GitHub EDA Release 只是工具配送，不代表 Source 已整合。未授權不能宣稱遠端 CI/Release 完成。
3. **修正 0/80 的誤導**：Sync 已回報 A0-01..A0-18 在 Local 18/18 PASS，且固定 SHA/逐 ID Logs/Reviewer Hash 存在；Agent 亦回報 Native Codex 修復 APB CRC32 RTL、Icarus FAIL→PASS、Yosys 結構檢查 PASS、獨立 Local 重現。Supervisor 尚未直接取得 Local Raw Evidence 重驗。E01..E20 仍全部 NOT_RUN，A1..A6 尚無完整逐 ID 正式驗收證據。Dashboard 必須分列：(a) Agent 回報有證據的 Local PASS，(b) 已由 Supervisor 可直接檢視且符合 Case 原定斷言的 Verified PASS，(c) NOT_RUN/BLOCKED/未取得證據；不得把 Local PASS 淹沒成『一件都沒通過』，也不可冒稱已正式驗收。
4. **立即逐 ID 對帳現成 A0 證據**：沿用凍結的 Local 原始碼、A0-01..A0-18 逐 Case Raw Log、Local SHA、命令、Evidence SHA256、環境/Profile 與獨立 Reviewer 結果，在 Sync 新增 acceptance_local_summary 和每項 Evidence Mapping。證據符合 docs/09 原文才標 LOCAL_EVIDENCE_VERIFIED，欠缺證據標 NEEDS_EVIDENCE；不修改正式 60+20 Required Cases、不自行更改 Gate、不為了提高 PASS 數重跑無關測試或擴張測試框架。
5. **開發版繼續向前**：保持 DEVELOPMENT VERSION / 非量產版，優先將已跑通的 Runtime→Native Harness→RTL→Real EDA 固定案例做成可以接受另一項真實 RTL 工作輸入的可重複流程，保留最小必要修復與真實 Logs。Local Reviewer 可重現就能標相應 DEV_USABLE_E2E_LOCAL，不需要 GitHub Source Commit。完整正式 80 案仍依既有 Case 原要求驗收，不能以 Local Mock 或 Sync 文字自行宣告 PASS。

### 2.9 A0 驗收收斂：已發現四項斷言缺口，限縮補證，不再空轉（2026-11-08）

**本輪有實證的新發現：** 已 ACK Directive 07 的 Coding Agent 回報 A0-01..A0-18 均有 Local PASS 紀錄，逐 ID Log/來源 SHA/Reviewer Mapping 已整理；對照 docs/09 原斷言，其中 14 項內容覆蓋充分，但 A0-03、A0-09、A0-13、A0-18 四項仍有實際斷言缺口。此外舊版 18 項紀錄均欠缺符合 docs/09 Passing evidence format 的當次 environment_digest，故不得把歷史 Local PASS 自動升格正式驗收。另第二個可設定 CRC Polynomial 任務已於 Local 真實跑通 Codex→RTL→Icarus→Yosys，這項開發成果保留為可使用功能。**

1. **這一輪唯一 A0 驗收工作是關閉四個已知缺口及環境證據。** A0-03：比較遭拒衝突前後原始 Event Payload/Row 不變；A0-09：證明另一 IP 真的獨立完成，包含可核對的 Delivery/Ticket Terminal Status；A0-13：真實呈現使用者離開/關閉 Native Harness 後 Event 與 Owner Work 持續存在（必要時精確標缺少的 Harness 能力，不得以 Worker process exit 充當）；A0-18：新事件啟動後證明舊 Event/History 仍完整保留。只增補上述四項必要斷言或測試，不創建新框架、新矩陣或無關回歸。
2. **environment_digest 不得事後偽造。** 用既有 frozen A0 Local 工作區／可重現快照做一次有界的新取證輪次，執行既有 A0-01..A0-18 必要原 Case Commands，對實際新執行的每項記錄 implementation_commit、started_utc/ended_utc、environment_digest（工具/OS/Python/設定指紋與可追溯 SHA）、actual_result、raw log path/digest、Reviewer 與 limitations。對歷史 Logs 只保留它們原有 provenance，不以現時指紋冒稱舊環境。只要一項真正缺證便標 NEEDS_EVIDENCE 或 BLOCKED，不宣稱已閉合。
3. **Gate 簽核與進度報告採雙層狀態。** 每項 Case 分別列 Local Recorded PASS、Local Evidence Verified（證據是否符合 docs/09）與 Supervisor Directly Verified（若原始 bytes/Log 不可取得則 UNKNOWN）。滿足原定義與完整證據的 A0 案例才可標 LOCAL_EVIDENCE_VERIFIED；完整 A0 18/18 達標與 Reviewer 簽核後才可記 Local A0 Gate CLOSED_WITH_EVIDENCE。保留 G0–G7、80 個 Required Cases 與正式發布控制。A1–A6 不以固定 EDA Demo 自動 PASS；E01–E20 仍以真實條件各自查核。
4. **開發版與範圍保持。** 已完成可設定 Local RTL/EDA 開發版本即為合法交付，不要求 Source GitHub 上傳、Integrator、遠端 PR、傳輸通道或額外人類動作；不要把 artifact_transfer_state=UNAVAILABLE 列 Blocker。對既有二個 Local Real EDA 案例保留原始證據與已知限制，不重跑未受影響的工作。A0 補證完成或確實受限後，繼續下一項真正可用的 Domain Owner/RTL 工程功能。
5. **完成條件**：於 Sync 回報十八個 A0 ID 的實際新驗收狀態總表、四項斷言對應證據、環境指紋、Reviewer 結果、精確 Local SHA 和 Local Bundle SHA256；缺少的項目和下一步要具體，不用再次要求 Supervisor 為此開新 Directive。整個工作是一個限縮 A0 收斂任務，不得自行擴張成無界測試／Review 系統。

### 2.10 Directive 08 驗收發現：只收斂 A0-09 與 A0-13 的實際 Runtime 能力（2026-11-08）

**本次變更的具體依據：** Coding Agent 已 ACK Directive 08，於本地執行一次有當次 environment_digest 的 18 個 A0 原案例，獨立 Reviewer 回報 **16 個 LOCAL_EVIDENCE_VERIFIED，A0-09／A0-13 仍 NEEDS_EVIDENCE**。本地新驗證證據包含來源 b99a624、該輪 18 個 Logs、環境指紋及 Reviewer SHA256；Supervisor 只讀到 GitHub Sync 的記錄，未拿到 Local Source/Raw Logs 直接重驗。A0 Gate 仍 OPEN，正式 80 案不得升格。以下為真正需要實作的兩個缺口，不得以重新解釋測試、補寫自評或放寬 Assertion 收斂。

1. **A0-09：確立可觀測的獨立 IP 完工語義。** 目前第二個 IP 的 Delivery 雖 ACKED，但 Ticket 仍 READY，不能證明該 IP 任務獨立完成。沿用既有 Runtime Event/Delivery/Ticket/Lifecycle 及 AuthZ，做最薄的合法 success completion transition（或採用既有真正終態及事件，如已存在）；在第一 IP 因阻礙保持相應狀態時，使第二 IP 有真實成功終態、正確因果 Decision/History，且反覆 Callback 不得重複推進。以原 A0-09 斷言執行並保存確切來源 SHA、命令、原始 Logs、環境 Digest、結果及 Reviewer。不增加新通用流程框架、不改政策或多 Owner 架構。
2. **A0-13：確認真實 Native Harness 退出後既有 Owner 工作的存續與恢復。** 既有測試只證明 Worker Exit，而本次 Native 修正只驗證啟動/終止 PID 與 Controller-driven Recovery，尚不能證明 Owner Work 自主持續。請用已允許的 Native Harness 和既有持久化 Runtime 機制，重現使用者關閉/離開 Harness 後 Event、Ticket、Owner Work 持久，且下一次既有 Local Runtime/Owner 執行路徑能接續；清楚區分「持久保存」「下次啟動恢復」與「無人值守持續運轉」，**不得虛稱第三項**。若實際要求在 Session 關閉時仍有獨立背景服務，而現有架構/權限尚未授權，不得私設 Windows Service、新 Agent、排程守護進程或新控制平面；精確記錄欠缺能力與需要的人類架構核准，並將此 Case 保持 NEEDS_EVIDENCE／BLOCKED。
3. **保存 Native Harness 真實工具證據。** 前次 A0-13 修正欠 contemporaneous environment_digest，且未 pin native CLI/wrapper 版本。此次只對實際執行回合記錄工具版本、現時 OS/Python/Runtime/CLI/必要 Wrapper Digest、Local Git SHA、開始/結束時間、完整 Command/Exit Code、事件與 Owner 狀態截圖或 Raw Log 及 SHA256，不能倒填歷史環境指紋。保留既有安全、Sandbox、Authenticated Actor/Scope 和原測試限制；不得為了成功而削弱 AuthZ 或批准 Policy。
4. **有界驗收與轉段。** 先針對 A0-09 和 A0-13 兩項執行定點 Case，修復迴圈遵循既有最多三次相同 Failure Signature 迭代，最後只做一次必要的受影響 A0 合約回歸與獨立 Reviewer。其餘已有 16 個 LOCAL_EVIDENCE_VERIFIED 的固定證據維持版本可追溯，不要為了提高測試數反覆驗證未受影響模組。若兩案都符合原 docs/09 契約及 docs/09 Passing Evidence Format 才可報 A0 Local Gate CLOSED_WITH_EVIDENCE；若 A0-13 牽涉未授權架構或其他真正阻礙，就保持 OPEN、清楚標示，並繼續下一個有用的 Local 開發版本功能，不無限卡在 A0。
5. **Sync 時間欄位一致性及權限**：本次 GitHub Sync 追加了 07:18:01 UTC 的有效進度，但 YAML machine-readable 的 heartbeat/last_effective_progress 仍停在 06:55:20 UTC，任務頂層 mission_state timestamp 更舊。下次活躍 Session 編輯 Sync 時，依真實當次時間更新機器可讀的 Heartbeat、Last Effective Progress、updated_at 與 Directive ACK，讓 Dashboard 可依真實門檻監督；不要回填或偽造 15 分鐘輪詢。Local Source/Evidence Bundle 仍只須保存在 Coding Agent 自己的 Local，**不能要求上傳 GitHub、找 Integrator 或建立遠端 Source 傳遞通道**。既有 80 個 Case、安全與正式發布 Gate 都不改。



### 2.11 下一輪明確工作單：G1 Domain Owner 可用功能整合（SF-DIR-20261108-10，2026-11-08T09:59:00Z）

**觸發依據及優先順序：** 最新 Sync 回報 Directive09 已 APPLIED、Local A0 18/18 CLOSED_WITH_EVIDENCE，Local SHA `365e85509f3660e93fc6b5fbc0eeed38b238f560`，本地交付 ZIP SHA256 `7209d9ab938b827cb28d031895aaea7d9b04bad7ff1e303a8f767a0af942c471`；G1 的 Scope、Candidate、Watchdog、Typed Registry、Lifecycle、Failure Receipt 有 Local Mock/Reviewer 單元證據，但 G1_NOT_ACCEPTED，E01–E20 仍 NOT_RUN。Supervisor 未取得本地原始碼和 Raw Logs 獨立重驗。使用者要求立即發布可執行的下一輪工作指引。**本節取代 §2.10 已完成的 A0 補證作為當前立即任務；不改變原 G0–G7、80 項正式驗收、權限或架構。**

1. **立即開始，不等待下一份指令。** 活躍 Session 讀取本文件，ACK `SF-DIR-20261108-10` 至 Sync；從現有 Local SHA 和已凍結的 G1 單元延續，不重做 A0，不重新下載 Repo，不建立新專案或通用 Agent 框架。若 Session 已停止，於下次啟動後執行，不宣稱 Always-on。
2. **本輪唯一優先工程成果：一條真實 Domain Owner Runtime 工作鏈。** 以既有 Requirement/Scope、Candidate、Typed Command/Registry、Lifecycle、Watchdog/Checkpoint 與既有可設定 Native Codex→RTL→Icarus/Yosys Vertical Slice，實作並執行 `Requirement → 指定 Owner Instance → durable work/ticket → Native Harness → RTL edit → Real EDA → Evidence → terminal completion`。明確提供可執行入口、範例 Input/Output、完整命令、成功終態、失敗狀態與因果 trace；沿用既有合法授權及現成 Adapter。禁止用 MODE_MOCK 代替 Native/EDA 的真實結果，禁止以單元測試數取代功能交付。
3. **恢復能力限縮驗證。** 使用既有持久化與 checkpoint，證明至少一項工作在 Harness 關閉、Owner/Controller 重新啟動後仍可查詢並恢復，不遺失工作、不重複完成或越權；如只證明「下次啟動可恢復」，就照實標示，不可宣稱無人值守背景持續運轉。若需未授權 Windows Service/排程/控制平面變更，停止該部分並報告需核准事項，繼續其餘合法工作。
4. **同 Role 多 Instance 的最小真實行為。** 在既有 Registry/Scope 中用兩個或以上可區分的同 Role Owner Instance，驗證 Instance ID、Candidate/Branch Scope、訊息路由與工作隔離；保留獨立可追溯事件及 Evidence。若只有 Mock、無真實並發或缺少原 E01/E02 的三 Instance/重疊時間斷言，標 `G1_PARTIAL_LOCAL`，不得宣稱 E01/E02 PASS。Branch DAG、PPA、Pareto、Merge ReGate 保留 G1/G4/G5 原定順序及要求，沒有實測則 NOT_RUN。
5. **驗收與交付收斂。** 優先執行直接對應本輪功能及原定 Gate 的最小必要測試，於固定 Local SHA 做一次受影響回歸及獨立 Reviewer；每項原正式 Case 逐 ID 列 `PASS/FAIL/BLOCKED/NOT_RUN`，附 raw logs、command、tool/environment digest、source SHA、evidence SHA256、Reviewer limitation。A0 18/18 保留 Local evidence 分層，不得升格 Supervisor Verified。不得新增無關測試、重複 Review 或任意降低正式 Case 斷言。
6. **本輪交付與自主接續。** Local 提供可啟動的開發版、README 重現步驟、固定 Local Git SHA、Source+Evidence ZIP/Patch 及 SHA256；在 Sync 寫入本輪實際完成功能、實際測試及 Mock 邊界、last_effective_progress、heartbeat、Gate 狀態、具體下一動作。Local-only 即為本輪交付，不要求遠端 Source/Integrator/PR；artifact_transfer_state=UNAVAILABLE 只作事實，不列為阻礙。若 G1 所有適用正式契約有原始證據才標 Local Gate 完成並自主轉 G2；否則標部分完成，持續執行合法的 G2/G3 最小整合前置工作，不等待 Supervisor 再次分派。
7. **停止條件與升級。** 相同失敗簽章最多三次有界修復；遇到 AuthZ、安全、權限、配額、重大架構或正式 Gate 變更，保留原限制並在 Sync 提出精確人工決策，不能自行擴權。活躍 Session 每 15 分鐘輪詢本文件並更新真實 Heartbeat，Gate 轉換立即回報；無工程進展不得刷新 last_effective_progress。


### 2.12 Directive 11：全部功能實作優先，測試縮減至不妨礙功能交付的最小集合（2026-11-08）

**授權來源與最高優先任務：** 使用者明確要求「先全部做完全部的實作，測試只做最小部分，不妨礙功能交付就不做測試」。立即停止以局部 Gate PASS、反覆 Reviewer、補齊環境指紋、測試矩陣、文件整備為當前主要目標的開發方式。**從此 Directive 起，核心目標是把 v3.1 已定義的功能範圍一次實作完成並整合為可操作的 Local DEVELOPMENT VERSION。** 本節在本輪優先順序、轉段和最小測試策略上優先於 §2.8–2.11 與 §3 的先驗收再轉段語句；其餘安全、權限、架構與正式驗收要求不變。

**立即執行規則（不得等待 Supervisor 再分派）：**
1. **ACK 並接續本地實作。** 活躍 Session 讀到 `SF-DIR-20261108-11` 後在根目錄 Sync Web Edit 寫入 last_seen_directive_id、ACK 時間與實際狀態。從既有 Local `9b81128454cbd148c19e2de5940376f177a05e63` 和工作樹開始，先核對當前真正存在的能力，再直接寫缺少的功能。不要重建 Repo、新專案、重做 A0、重下載工具或重跑歷史測試。
2. **一次涵蓋所有未完成的實作，不以正式 Case 驗收當作開發依賴。** 將 G1–G7 的實作視為一個持續工程 Mission，可按功能依賴順序開發且跨 Gate 進行；**G1/G2 等 Formal Gate 未 PASS，不得阻止繼續實作後續功能**。但不得將「實作已完成」寫成「正式 Gate 已通過」。唯一有效終點是各項原定可執行功能均已實作與整合，未完成的真實依賴明確列出。
3. **完整實作清單，禁止停在 Mock：**
   - **G1 Runtime / A0X：** Requirement、Candidate 與 Branch Registry 真實持久化；Owner Role 與多個 Owner Instance 完全分離；Candidate-scoped Work Routing、Durable Fan-out/Fan-in、Lease Epoch、Quota、Lineage DAG、Crash Replay/Checkpoint、失敗隔離及可恢復的 terminal lifecycle。至少能建立同 Requirement 下多個可辨識 Owner、Candidate 與 Branch，並真正分派工作；Mock Registry 不能冒充完工。
   - **G2 Harness / MCP：** 以既有 AuthZ、Scope、typed tools、Skills/MCP 與 Session Adapter，接上本地 Native Codex，並完成架構所要求的 Claude Code 相容接口、換裝/恢復/通知處理；工具或帳號在現場不可用時可交付實作與可替換 Adapter，明確標未實際執行，不得偽造成功。
   - **G3 EDA：** 以已可執行 Icarus/VVP/Yosys 的真實 EDA Profile，完成可配置 RTL 修改、模擬、必要 Formal 流程接口、Synthesis、原始 Log/Version/SHA、Golden Model、Environment Owner、候選個別 Evidence 和可替換的商業 EDA Provider Contract；不得假造未執行之商用工具或 Formal 結果。
   - **G4 多 Owner / Branch：** 真正的 Local Git Branch/Worktree 隔離、同 Role 多個 Owner Instance、不同 Candidate 的 real defect→edit→verify、Peer/Lease/Wakeup/Recovery。Coding Agent 的本地 Git 不代表 GitHub Push 權限。
   - **G5 Parallel Exploration / Merge：** 同 Requirement 的 performance、low_power、area 三條 Branch/Owner 流程、至少一條 Nested Fork、各 Candidate 專屬 EDA/Synthesis/PPA Evidence、可重現 Pareto Selection、可稽核 Merge Conflict/Decision，以及 Merge 後以新 SHA 執行 ReGate 的完整實作。可合法取得的工具數據才算 Real PPA；Power 缺乏有效來源時標 INCOMPARABLE 並讓流程可操作，不能捏造數值。
   - **G6 可觀測性 / UI：** Event Journal/Replay、Dashboard/API 的 Owner/Branch/Candidate DAG、Status/成本/決策/Evidence Trace、失敗候選保留、PDCA 與通知鏈路，使使用者能看見系統實際執行與下一動作。
   - **G7 自主運作 / 韌性 / Governance：** Existing Authorized Control Plane 內的 Crash Recovery、No-progress Watchdog、資源公平、Quota、Scope/AuthZ、安全拒絕與故障處置，支援可中斷、可接續、不重複副作用的 Local Runtime；不得私設未授權 Windows Service、長駐背景守護者、外部連線或權限擴張。
4. **測試策略立即變更為 MINIMAL DELIVERY-BLOCKING ONLY。** 開發每個功能時只做讓下一個功能能整合的最小檢查，例如必要的匯入/編譯、啟動檢查、明顯合約錯誤、關鍵資料損壞/越權風險檢查。若測試失敗會直接阻斷功能完成，才作最小修復與重試。**不為了提高測試數或覆蓋率而新增測試；不重跑未受影響模組、全套 80 案、大型回歸、每功能獨立 Reviewer 或多輪報告。** 各功能整合完畢後，執行一次有界的最小完整 E2E Smoke，確認 Requirement→多 Owner/Branch→真實 EDA→候選選擇→Merge/ReGate→Dashboard/Event Trace 的主路徑可以啟動與前進；若這項 Smoke 失敗且阻斷產品操作，只修正阻斷缺陷。安全/授權/資料完整性已知的致命問題不能被測試策略忽略。
5. **保留 80 案正式驗收規格，但不在本輪以通過它們為交付先決條件。** docs/09 的 A0–A6 60 案與 docs/15/contracts 的 E01–E20 20 案以及 G0–G7 的 Formal PASS 條件原封不動。未真正執行的 Case 仍為 NOT_RUN；未驗證的功能標 `IMPLEMENTED_UNVERIFIED`，完成最小串接後可標 `INTEGRATED_SMOKE_PASS`（需可核對 Log）；只有符合原 Case 證據門檻才可標 `FORMAL_PASS`。本輪目標可達 `ALL_FUNCTIONS_IMPLEMENTED_LOCAL; FORMAL_ACCEPTANCE_PENDING`，不得把它寫成 Release Ready、80/80 PASS 或遠端整合。
6. **阻礙處理以完成所有可做功能為準。** 相同具體故障簽章最多三次有界修復，仍無法解決就記錄並切換其他未完成功能，不要持續困在同一測試或等待工具。工具授權、商業 EDA、外部模型不可用時實作明確的 Provider Contract 與 Local 可用路徑，誠實標示真實執行缺口；不得自行降低安全與准入條件。對於能在現有架構/權限內完成的功能，不得以「待人工核准」無限擱置。
7. **進度回報只量實作完成度。** 在 Coding Agent 的 Sync 中維護 `implementation_inventory`：每個 G1–G7 功能的 `IMPLEMENTED / PARTIAL / NOT_IMPLEMENTED / EXTERNAL_DEPENDENCY`、Local path/module、Local SHA、具體入口、上下游依賴、實際可運作範圍、剩餘缺口與 next executable action；再以一條 `implementation_remaining` 明列尚未實作功能。Heartbeats 在活躍 Session 維持原規則，只有新增實作、消除真實整合阻礙或完成可用工作鏈才算有效進展。禁止把測試數、Review 數量、Sync Commits 算成完成比例。
8. **交付收斂。** 以同一既有 Local Workspace 持續完成剩餘功能。最後交付可操作的 Local DEVELOPMENT VERSION、單一最小啟動/重現方式、功能清單、已知限制、來源與 Evidence 固定 Local SHA、ZIP/Patch SHA256，必要的 Smoke Logs；不要求無法執行的 GitHub Source Push、遠端 PR、Integrator、Artifact Transfer。Local-only 是本輪授權交付邊界，未有合法 bytes 傳遞時保持 `artifact_transfer_state=UNAVAILABLE` 且不視為開發阻礙。
9. **停止/回報規則。** 不因某一 Gate 未驗收、某個非阻斷測試未跑或 Reviewer 缺少簽核就停工。直到所有授權範圍內功能均已實作才把 Mission Implementation 標完成；若存在不能自主解除的真正權限/架構決策，精確記錄受限功能，繼續其他功能。每次重要功能群完成或阻礙改變時回報 Sync，15 分鐘輪詢只在 Session 活躍時適用。Supervisor 不會用新增測試與文件整理替代工程前進。

**指令效力：** 本節是最新的 User-directed 工作優先順序覆蓋。任何先前文字若要求「每個 Gate 先全部測試驗收才准寫下一 Gate 的功能」、「每項功能必須先 Reviewer 才能繼續」，於本輪 Implementation Mission 不適用；**原有規格、80 項 Formal Acceptance、G0–G7 名稱與正式 Release 要求繼續保留，並未撤銷。**


### 2.13 Directive 12：真正的 Select → Merge → ReGate 工程閉環，限縮 Proof／PPA 阻礙（2026-11-08T12:57:08Z）

**已確認的新工程依據：** Coding Agent 的 Directive11 Local Delivery（latest Local Source `c1ee4c63ffcc33533c1f481c7bed8dda42620806`，Local Bundle SHA256 `3f7d7973fb258c91903a1dd06a7174e31af3d8d54a00c31025c86a03070780af`）已回報 G1–G7 授權範圍內的主要實作、三個不同 RTL Owner/Branch 的真實 Codex/Icarus/Yosys、Nested Fork、Dashboard 與 Recovery。**但候選 Formal 證據 BLOCKED、Timing/Power INCOMPARABLE，Select/Merge/新 SHA ReGate 沒有實際完成，完整 E2E 仍為 PARTIAL。** 使用者要求下一階段；Supervisor 依已證實缺口指示接續，避免倒退到無限測試。與 §2.12 並行：優先完成真正可用的系統功能，不改原 80 項正式驗收要求。

**本階段主目標：在現有權限與現有 Local 工作區，完成一條有真實來源證據的 Candidate Select → 受控 Merge → 新 SHA ReGate；若合法 Proof/PPA 前置條件確實不存在，精確終止在原 Gate，交付可執行流程、最小診斷及所需批准事項，不得用假資料越過安全門檻。**

1. **立即 ACK／沿用既有成果。** 活躍 Session 讀到 `SF-DIR-20261108-12`，透過 GitHub Web UI 僅更新根目錄 Sync 的 ACK。從既有 Local `c1ee4c63ffcc33533c1f481c7bed8dda42620806` 及目前工作樹繼續，保留三條 performance、low_power、area 分支、nested fork、Source SHA、Raw Evidence、SQLite 與工具 Profile。禁止重建工程、新增大框架或為了再取得好看的數字重跑歷史 A0 和 80 案。
2. **先查既有工具可用性，限定一次短診斷。** 在已授權／已安裝的 OSS CAD Suite 與本地設定中，檢查 Yosys 內建 SAT/equivalence 能力，以及既有可執行的 formal/STA/功耗工具、合法 Golden、clock/reset/constraints、library/corner、solver 和 provider/profile。**只用真正存在且可合法使用的工具**，先建立一個最小、可重現、對 Candidate SHA 綁定的 RTL 等價／性質證明通路；必要時補最薄 Provider Adapter 或合法設定。Formal PASS 必須具正確 property、assumption、Spec/Golden SHA、tool/env digest、command、exit code、原始 log；僅模擬 PASS、語法成功或腳本回傳 0 都不能代替 Proof。
3. **PPA 資料分層，不製造假可比較性。** 使用既有真實 synthesis/STA/power 工具時，明確記錄 mapped/unmapped、constraints、library、corner、activity、units、Candidate SHA；同前提下才生成可比較數據。Yosys 186 generic cells 只作 generic synthesis evidence，不能標實體 Area/Timing/Power。若只有部分有效指標，保存有效部分，缺少的標 `UNKNOWN/INCOMPARABLE`，依原有 Comparison/Policy 決定是否可選；不自行改門檻或隱藏缺值。
4. **只在原授權及原 Gate 條件均滿足時真正走通選擇與合併。** 在合格 Candidate、合法選擇權重/授權、Head SHA fence、可比較證據到齊後，使用現有 CLI `python -m siliconforge.operations` 的 `compare → select → merge → regate` 路徑，以實際 Git Merge SHA 重新執行必要 Simulation/Formal/Synthesis/PPA，保留 Merge Conflict/Decision/Branch DAG、原始 Logs/Hash。絕不能用未證實的 `FORMAL_PASS`、假造 PPA、人工改狀態或跳過 Merge ReGate 取得成功畫面。
5. **若依賴確實不可用，不要反覆空轉。** 已存在且可合法修復的資料／接口缺陷才寫程式；同一失敗簽章最多三輪有界修復。如果缺外部 Proof Profile/solver、技術庫、真實 Timing/Power 或合法選擇權重，立即列出可複製的 `required_tool_or_input, version, purpose, existing_attempt, precise_missing_permission_or_data, smallest_safe_next_action`，將真實 Select/Merge/ReGate 標 `BLOCKED/NOT_RUN`；同時交付目前可操作的工程入口，停止無效重跑。未授權工具安裝、網路連線、外部服務、排程守護與額外權限均禁止。
6. **只做阻礙交付的最小驗證。** 每個真正的 Source/Adapter 修正只做 compile/import 與針對缺陷的短檢查；條件具備時執行 **一次**具備真實 Evidence 的完整 `Select→Merge→New SHA ReGate` Smoke。條件不具備時，做一次精確的 Gate 拒絕證據即可，**不要啟動 80 案驗收、歷史回歸、反覆 Reviewer 或衍生測試框架**。原正式 A0–A6 60 項和 E01–E20 20 項維持規格不變；未跑仍 NOT_RUN，完成實作不等於正式 PASS。
7. **回報與完成語義。** 在根目錄 Sync 回報 Directive ACK、Local Source SHA、可重現 CLI/工具設定、Proof/Timing/Power 的實際狀態、可比較性、候選/分支/合併 SHA、必要的 Raw Logs/Hash、Bundle SHA256、`implementation_remaining`、`next_executable_action`、人工核准事項。若真實 Merge/ReGate 完成，標 `LOCAL_REAL_E2E_MERGE_REGATE_REPRODUCED; FORMAL80_PENDING`（證據分級），不得自稱 Release/Remote CI 完成。若外部條件缺少，標 `LOCAL_IMPLEMENTATION_DELIVERED_WITH_EXTERNAL_GATE_DEPENDENCIES`，說清楚唯一缺口，不冒稱完成驗證。Local-only 交付即可，`artifact_transfer_state=UNAVAILABLE` 不是此輪的工程 Blocker。
8. **既有排程和 Session 限制不變。** 活躍時 15 分鐘重新讀本文件與 GitHub Web Edit Sync，只有真實進展才更新 `last_effective_progress`；本地 Session 結束後不可宣稱 24/7 自主執行。Supervisor 不修改 Coding Agent 的 Sync，也不替它偽造任務完成。

**注意：** 此指令為 G3/G5/G7 既有規格範圍的可執行工作排序與故障收斂，**不是新增 G8、不降低 PPA／Formal／Merge Release Gate、不擴張權限**。

## 3. 後續里程碑，自主往前，不用等待人工分派

| Gate | 工作範圍 | 本地完成證據與自動移轉 |
|---|---|---|
| **G0：A0 CLOSE** | 關閉 18 個 A0 ID、獨立 Review、固定 Local Commit、交付包 | 所有 A0 正式契約通過、原始 Logs/Hash、Reviewer Sign-off、Local Bundle；完成立即進入 G1 |
| **G1：A0X / E Runtime** | Exploration / Branch Registry、Owner Role 與 Instance 分離、多同 Role Instance、Candidate-scoped Routing、Durable Fan-out/Fan-in、Lease Epoch、Quota、Lineage DAG、Crash Replay | 在本地用可執行單元/失效注入證明 E01–E08 適用的 Runtime Contracts；Fake EDA 只能標 MOCK；完成進 G2 |
| **G2：A1 / MCP & Harness** | native Codex / Claude Code + MCP/Skills、AuthZ、Session 換裝、持久化通知，不自造聊天 CLI | 原 A1-01..A1-08 逐項真實 Harness 證據；不可達的外部 Harness 需具體標示，不可用 Mock 替代；獨立可行工作可平行進 G3 前置準備 |
| **G3：A2 / Real EDA** | 開發版優先 OSS CAD Suite 的 Icarus/Verilator + Yosys（必要時 SBY）；Environment Owner pin tools、APB CRC32 golden model、Formal、netlist 與可替換工具 Profile | 原 A2-01..A2-07 的實際工具與 profile/spec/source hashes；授權或無法安裝阻礙不阻止其他 Local 模組準備 |
| **G4：A3 + A3X** | RTL/Verification/Formal 多 Owner Instance、Git Branch/Worktree 隔離、真實 defect→repair→verify、Lease/Wakeup/Peer | 原 A3-01..A3-07、E09/E10 與相關隔離/重啟證據。Local Runtime 所管理的 Branch 不需要此 Coding Agent 具有遠端 Push 權限 |
| **G5：A4 + A4X** | 同一 Requirement 三路 Performance/Power/Area 真正重疊探索、一次 Nested Fork、候選個別 Simulation/Formal/Synthesis/PPA、Pareto、Merge Conflict、合併後新 SHA 重新驗證 | A4-01..A4-06；E11–E18 與 E20，必須有真實可比較 EDA 報告和 Merge 版 Evidence。沒有合理 Power 證據顯示 INCOMPARABLE，不自行宣稱通過 |
| **G6：A5 + A5X** | Event Journal Replay、Dashboard DAG、Owner/Branch/Evidence/Cost Trace、PDCA、通知 | A5-01..A5-07 及 E19；DAG 查詢完整可追溯，失敗候選也保留 |
| **G7：A6 + A6X** | 多分支 Chaos、長期 Restart/Crash、No-progress Watchdog、資源公平、安全與 Scope Gate | A6-01..A6-07、E20 回歸及剩餘全部 Required，逐 Case 回報。**全專案遠端完成**還需實際 Source Bundle 交付、Remote Integration、CI 與適用真實 EDA Gate，不能靠 Local Sync 自評 |

**自動推進政策（以 §2 的可用開發版為近期最高優先）**：G1 現有基礎可支撐 Vertical Slice 的部分應立即用於 G2/G3 的最小真實整合，不需等 G1 所有非必要增強完成；各 Gate 的正式驗收與終局定義仍維持不變。每個 Gate 的 Local 實作與驗證完成即可轉入下個不依賴遠端發布的 Gate；未達正式 Gate 不能把它升格 `VERIFIED`。依賴可並行，不做一關卡卡死全專案。正式全體 80 Required Cases 不降低、不自行擴充成無限測試清單，也不擅改架構、Autonomy Policy 或批准權限。

## 4. 有限失敗處理與資源治理

- 開發版優先追求可執行功能與交付證據；新測試框架或額外測試僅在具體缺陷、既有 Gate 或實際交付風險需要時才可擴充。不得以測試數量、Reviewer 迴圈或抽象層增長取代 Vertical Slice 的進展。

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

**EDA 專用回報**：oss_eda_install_state、oss_eda_source_and_sha256、eda_provider/profile/version、eda_actual_executions（Command/Exit Code/RTL SHA/Raw Logs）、commercial_adapter_contract_state，未執行就標 NOT_RUN；這些屬於 Coding Agent 自行回報，不得由 Supervisor 偽填。

**額外回報**：dev_version_label（必標 DEVELOPMENT VERSION / 非量產版）、dev_usable_capabilities、vertical_slice_last_run（命令、輸入、輸出、工具/環境版本、Local SHA、原始 Evidence；未執行則 NOT_RUN）、dev_delivery_state、remaining_mock_or_stub、external_harness_blocker、real_eda_blocker、bundle_transfer_state。這些屬於 Agent 自行回報欄位，Supervisor 不得直接替它寫入 Sync。

**必須回報**：每次 Gate 啟動／完成、Local Commit、真實測試新結果、重大缺陷、阻礙、指令版本改變、Artifact Ready、遠端 Integration、Session 停止。一般在活躍執行期間至少每 15 分鐘檢查一次指令並更新 Heartbeat；不活躍時不能偽造輪詢。若無實質改變，不要把 Heartbeat 或重新跑同一套測試當新工程進展。

## 6. Supervisor 的定時監督與指令修改責任

Supervisor 每兩小時巡檢**本 Repository** 的 Sync、最新 GitHub Commit/CI 與本指引的版本，並和前次狀態比對：
- 當看到 Gate 合法閉合、真實新阻礙、重複失敗、交付渠道變更或需求有新的決策，**由 Supervisor 更新這份 docs/19 文件並遞增 DIRECTIVE_ID**，不必也不應為了更新 Supervisor 版本同步改寫 Agent 的 Sync；Agent 會在下一次輪詢後自行 ACK 最新版本，Coding Agent 下次主動輪詢即可接收，不需要人類轉達。
- 更新只限安全且已授權的目標排序、下一階段、故障恢復及 Reviewer 的查核重點；**禁止自動降低測試 Gate、擅自核准公開發布、增加未授權外部工具或改變原架構意圖**。
- 除明確需要人類批准外，Supervisor 不要求人類重複搬運同一任務；若沒有重大改變，**不要製造新版本或打斷 Coding Agent**。
- Supervisor 不編輯 Agent 擁有的 Sync Status 區塊；Agent 不編輯 Supervisor 擁有的 docs/19 指引。若指令已更新而沒有 ACK，下一輪巡檢提醒或分類為執行能力限制。
- 此監督是 GitHub 可觀測層，不是 Runtime 可以直接喚醒外部 Coding Agent 的保證。若沒有活躍 Harness Session，定時讀取指令需等 Session 恢復。

## 7. 絕對禁止的完工宣稱

不得以 README/AGENTS.md/本指引更新、GitHub Sync Web Commit、Local Git Commit、79 個 Local Unit Tests、三個假平行 Worker、模擬 EDA、漂亮 Dashboard、或 A0 Mock CI Green 當成正式 SiliconForge Release。每個驗收結論必須回到 `docs/09_ACCEPTANCE_TEST_MATRIX.md` 和 `docs/15_PARALLEL_EXPLORATION_ACCEPTANCE.md`，並有對應版本的真實 Raw Evidence。

**前版更新原因／下一步（SF-DIR-20261108-02）**：使用者明確要求以可使用、可交付的「開發版本」為當前產品目標，制止 G1 局部測試與框架持續擴張。Coding Agent 下次活躍輪詢時 ACK 本版，保留既有已完成 G0 與已凍結 G1 證據；從目前 Local 版本收斂必要缺陷後，**優先啟動最小真實 Codex/Claude Harness → RTL 修改 → 真實 EDA 的 Vertical Slice**，並製作可重現、清楚標註非量產版的 Local 交付包；傳遞受阻則如實標示 Local-only，不得偽稱遠端整合。G0–G7 及正式 80 項驗收原則全部保留。

**本版更新原因／下一步（SF-DIR-20261108-03，2026-11-08T03:02:20Z）**：使用者明確授權先用免費開源 EDA 完成可用開發版本，並保留商業 EDA 可替換接口。Agent 收到新 Directive 後，優先在既有許可範圍內取得官方 Windows x64 OSS CAD Suite、以 Verilator/Icarus + Yosys 完成 Native Harness → RTL → Real EDA 最小完整修復閉環，保留輕量 Provider/Profile 結構，隨實際結果打包原始 Logs 與 SHA256，並保持 DEVELOPMENT VERSION 標記。遇到必須管理員安裝、違反政策或無法驗證來源的問題才進行精確上報；不再因缺少商業工具或未完成進階測試框架停在 Mock。原有 G0–G7、80 Required Cases、授權、正式 Gate 及 Local→GitHub 限制均維持不變。

**前版更新原因／下一步（SF-DIR-20261108-04，2026-11-08T05:13:06Z）**：最新 Sync 證實官方 OSS CAD Suite 577 MB 下載兩度停滯，形成 G2/G3 最小實際 EDA 功能的具體阻礙。Coding Agent 收到新 Directive 後，依 §2.5 停止無效重試；在既有授權內嘗試可信且更小的開源 RTL Simulation 執行檔，能執行則先跑真實 FAIL/修復/PASS，不能執行則留存證據並明確提出所需的人類離線工具傳遞協助，不再擴張 G1 框架或重複增加測試。原 G0–G7、80 項、工具與傳輸 Policy 不變。

**前版更新原因／下一步（SF-DIR-20261108-05，2026-11-08T05:50:43Z）**：使用者已將 59 個 OSS CAD Suite 的完整分卷公開至正式 SiliconForge GitHub Release，先前 577 MB 單檔下載阻礙有新的合法分片替代路徑。Coding Agent 在下次活躍輪詢後按 §2.6 先下載並驗證末卷 `.zip` 與 `.z01`，能下載才完成 `.z01` 至 `.z58` 全部 59 份、重組核對官方原始 SHA256、實際執行 APB CRC32 Native Harness→RTL→EDA 最小閉環；否則提交具體下載／解壓阻礙與證據。保留現有 G0–G7、正式 80 案、安全與 Local Source Transfer 邊界，禁止以活動數或額外框架取代交付。

**前版更新原因／下一步（SF-DIR-20261108-06，2026-11-08T06:27:19Z）**：Sync 新增可信的本地開發版事件：Icarus/Yosys 真正執行、Native Codex 修復 RTL、固定工作任務本地 E2E PASS，Local Source Bundle 已製作但仍無法取得遠端驗證。依 §2.7 優先讓這條已跑通的 Runtime→Harness→RTL→EDA 流程可用於另一項實際工作輸入，建立可重複的開發版入口與真實證據，並具體呈報 Source Bundle 交付阻礙，不新增框架或無界回歸。保留 G0–G7、60+20 正式驗收、原權限與正式發布/安全政策。

**前版更新原因／下一步（SF-DIR-20261108-07，2026-11-08T06:33:16Z）**：撤銷要求 Coding Agent 處理遠端 Source 傳輸的工作，明確 Local-only 就是本輪可用開發版交付；要求先將既有 A0 的 18/18 Local PASS 逐 Case 對照原始證據，改善誤導性的 0/80 報表。其餘依現行 Vertical Slice 方向推進。原有 G0–G7、80 個 Required Cases、正式 Gate、資安與權限限制全部保留。

**前版更新原因／下一步（SF-DIR-20261108-08，2026-11-08T07:03:19Z）**：Agent 在 Directive 07 下完成第二個真實、可設定的 Local RTL 修復與獨立 EDA 重現，並對 A0 18 個 Case 做了逐項 Mapping，明確找出 4 個實際斷言缺口及全部 18 個舊紀錄缺少環境指紋。依 §2.9 只修補 A0-03/A0-09/A0-13/A0-18，執行一次帶當次 environment_digest 的有限 A0 原定驗收輪次，證據足夠後逐項改列 Local Evidence Verified；維持功能優先、不建立新框架、不要求 GitHub Source 整合、不降低 80 個 Required Cases 或安全限制。

**本版更新原因／下一步（SF-DIR-20261108-09，2026-11-08T07:55:01Z）**：Directive 08 完成一次真實 18 案取證，獨立 Local Reviewer 回報 16 個案例已符合本地證據要求，A0-09 Ticket 未達成功終態、A0-13 缺少 Harness Exit 後 Owner 工作存續/恢復原證據與當次 Native 工具指紋。依 §2.10 限縮補足這兩項實際 Runtime 能力、驗證並維持 A0 Gate 嚴格狀態；Sync 機器時間欄位同步採真實當次值；不增加無關測試框架、不要求 GitHub Source 傳遞、不擅建新背景服務或放寬原 80 項正式驗收及安全規則。


**本版更新原因／下一步（SF-DIR-20261108-10，2026-11-08T09:59:00Z）**：使用者要求明確發布下一輪可執行指令；Sync 已回報 A0 本地 18/18 證據閉合且 G1 局部單元已有 Mock/Reviewer 證據，但真正 Domain Owner Runtime 尚未整合驗收。依 §2.11 優先完成真實 Owner→Native Harness→RTL→EDA→Evidence→Completion，驗證有限恢復及同 Role 多 Instance 的實際隔離，交付 Local 可重現版本並自主推進。原正式 80 項、G0–G7、安全與 Local-only 權限均維持。


**本版更新原因／下一步（SF-DIR-20261108-11，2026-11-08T11:48:03Z）**：使用者明確要求「先全部做完全部的實作，測試只做最小部分，不妨礙功能交付就不做測試」。Coding Agent 下一次活躍輪詢立即 ACK，改為一次完成 G1–G7 功能實作並依 §2.12 的具體清單連續整合；只保留真正阻斷交付的最小測試與主流程 Smoke，不做非必要回歸或反覆 Reviewer，正式 80 案及安全權限不降低且不虛報 PASS。Local-only 交付邊界不變。


**本版更新原因／下一步（SF-DIR-20261108-12，2026-11-08T12:57:08Z）**：Directive11 Local Development Delivery 已證明三個 Native Codex RTL Owner/Branch 有實際 Icarus/Yosys 執行，但原有候選 Formal BLOCKED、PPA INCOMPARABLE 導致實際 Select/Merge/ReGate 尚未執行。依 §2.13，優先使用現有已授權工具建立真實 Proof/可比較 PPA，再執行一次有界的候選選擇、受控合併及新 SHA ReGate；如果外部配置或數據確實缺少，精確呈報阻礙，不放寬任何 Gate，不重啟完整80項驗收或無效測試迴圈。Source Transfer 仍限本地。
