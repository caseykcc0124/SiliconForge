# 19｜SiliconForge Supervisor Work Order：自主連續開發與動態指令通道

> **DIRECTIVE_ID: SF-DIR-20261108-05**
>
> **DIRECTIVE_STATUS: ACTIVE**
>
> **UPDATED_AT_UTC: 2026-11-08T05:50:43Z**
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

**本版更新原因／下一步（SF-DIR-20261108-05，2026-11-08T05:50:43Z）**：使用者已將 59 個 OSS CAD Suite 的完整分卷公開至正式 SiliconForge GitHub Release，先前 577 MB 單檔下載阻礙有新的合法分片替代路徑。Coding Agent 在下次活躍輪詢後按 §2.6 先下載並驗證末卷 `.zip` 與 `.z01`，能下載才完成 `.z01` 至 `.z58` 全部 59 份、重組核對官方原始 SHA256、實際執行 APB CRC32 Native Harness→RTL→EDA 最小閉環；否則提交具體下載／解壓阻礙與證據。保留現有 G0–G7、正式 80 案、安全與 Local Source Transfer 邊界，禁止以活動數或額外框架取代交付。
