# 《Technology Mapping for LUT-Based FPGA》影片教學系列

呢份 `README.md` 以 `Technology Mapping for LUT-Based FPGA` 呢本書嘅章節結構做藍本，整理成一套 16 集廣東話教學影片。每集都圍繞一個核心主題，方便你逐步錄製、剪輯同發佈。

## 影片 01：由 ASIC 到 FPGA：點解 Technology Mapping 咁重要？
簡介：由數碼系統設計流程講起，交代 ASIC、PLD、FPGA 同 SoC 之間嘅定位，並說明硬件架構點樣影響 logic synthesis。呢集會幫觀眾建立全局視角，明白點解 technology mapping 係將高階設計落地去 LUT-based FPGA 嘅關鍵步驟。

## 影片 02：Boolean Function 表示法入門
簡介：集中講解 hypercube、cube、implicant、minterm 等基本概念，再帶到 two-level representation、truth table、Karnaugh map 同 binary decision tree。呢集係全套課程嘅數學同表示法基礎，幫觀眾之後理解分解同映射方法。

## 影片 03：BDD 入門：點樣用 Binary Decision Diagram 表示邏輯
簡介：介紹 BDD 嘅核心結構、基本運算，同佢點解適合用嚟表示 Boolean function。之後會再講 software implementation 嘅基本觀念，包括節點喺記憶體點表示，以及 negation attribute 點樣幫手提升表示效率。

## 影片 04：Decomposition 理論基礎
簡介：由 functional decomposition theorem 講起，逐步拆解 complex decomposition model、iterative decomposition、multiple decomposition 同 decomposition direction。呢集重點係建立理論框架，等觀眾知道「點解可以拆」同「應該點樣拆」。

## 影片 05：用 BDD 做 Function Decomposition
簡介：聚焦喺用 BDD 進行函數分解，對比 single cut 同 multiple cut 兩大思路，並介紹 simple serial、iterative、multiple decomposition 同 SMTBDD 喺實作上嘅角色。呢集係由理論行去方法論嘅第一步。

## 影片 06：BDD Variable Ordering：次序點樣影響結果
簡介：講清楚變數排序點樣直接影響 BDD 大小、分解效果同最後 technology mapping 品質。觀眾會見到同一個 function 只要變數次序唔同，實作成本同資源使用都可以有好大分別。

## 影片 07：Nondisjoint Decomposition 深入理解
簡介：介紹 nondisjoint decomposition 嘅概念，同一般 disjoint 分解有咩唔同，亦會講到共享變數點樣改變拆解方式。呢集會幫觀眾理解更加進階、更加貼近實際 FPGA 資源利用嘅分解策略。

## 影片 08：Multi-output Function 點樣分解
簡介：由單輸出走向多輸出函數，說明點樣建立 common bound blocks、點樣形成 multioutput function，以及點樣用 PMTBDD 將多個單一函數合併處理。呢集重點係提升整體共享能力，而唔係逐個 output 各自獨立處理。

## 影片 09：Partial Sharing of Logic Resources
簡介：集中討論點樣喺多個邏輯函數之間做部分資源共享，包括 equivalence classes、SMTBDD 中嘅 partial sharing，以及用 MTBDD 搜尋可共享結構。呢集會令觀眾理解「共享」唔只係概念，而係可以系統化分析同實現。

## 影片 10：Configurable Logic Block 有咩能力同限制？
簡介：介紹 configurable logic block 嘅配置能力，分析 logic cell 嘅結構特性點樣影響可實現嘅函數形態。呢集會將抽象分解結果拉返落硬件層面，幫觀眾知道 FPGA block 本身可以做到啲乜。

## 影片 11：LUT Block 嘅 Technology Mapping
簡介：正式進入 LUT block 映射主題，講解 cutting line 點揀、映射效率點衡量、triangle tables 點樣使用，以及點樣喺 mapping 過程中考慮 nondisjoint decomposition 同 logic resource sharing。呢集係成套系列嘅核心實戰章節之一。

## 影片 12：Complex Logic Block 同 ALM Mapping
簡介：由基本 LUT block 延伸到 complex logic block，重點講 ALM block 嘅 technology mapping 方法、評估準則，以及 nondisjoint decomposition 喺複雜邏輯塊入面點樣落地。呢集特別適合想理解現代 FPGA 複合資源點樣被利用嘅觀眾。

## 影片 13：FSM 實作嘅 Decomposition 方法
簡介：先簡介 finite state machine 嘅基本背景，再聚焦 FSM 組合邏輯部分點樣映射到 configurable logic blocks。呢集會將前面學過嘅 decomposition 同 mapping 技術，帶入時序電路同控制器設計場景。

## 影片 14：Decomposition 同 Technology Mapping 演算法總覽
簡介：將前面分散講過嘅方法整理成完整演算法流程，說明由 function representation、BDD 建構、分解策略到最終 mapping 嘅步驟關係。呢集特別適合用嚟做「方法整合」，幫觀眾建立全流程思維。

## 影片 15：實驗結果與系統比較
簡介：分析書中實驗部分，包括 MultiDec 同 DekBDD 嘅比較、同學術系統及商業系統嘅對照、triangle tables 對結果嘅影響、時序電路綜合結果，以及 complex logic block mapping 嘅實驗表現。呢集重點係用數據驗證方法係咪真係有效。

## 影片 16：全書總結：由 Boolean Function 到 FPGA 實作
簡介：總結全套課程，由 Boolean function 表示、BDD、decomposition、resource sharing，一路串連到 LUT/ALM technology mapping 同實驗驗證。呢集適合作為系列收尾，幫觀眾重組知識架構，亦方便你引導佢哋進入下一階段實作或研究。
