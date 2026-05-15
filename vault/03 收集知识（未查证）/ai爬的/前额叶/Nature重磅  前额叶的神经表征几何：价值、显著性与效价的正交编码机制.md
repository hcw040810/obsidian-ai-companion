---
title: "Nature重磅 | 前额叶的神经表征几何：价值、显著性与效价的正交编码机制"
source: 知乎
url: https://zhuanlan.zhihu.com/p/1995314828739380631
date: 2026-05-12
tags: [前额叶, 知乎]
---

# Nature重磅 | 前额叶的神经表征几何：价值、显著性与效价的正交编码机制

> 来源:
> 爬取时间: 2026-05-12

---

不错过每日前沿资讯


**基本信息**

**Title:**Prefrontal neural geometry of learned cues guides motivated behaviours

**发表时间：**2026.1.7

**发表期刊:*****Nature***

**影响因子：**48.5

**获取原文：**

1. **PSY-Brain-Frontier**即可获取PDF版本
2. 点击页面底部“”即可跳转论文原网页


**研究背景**

***在生存充满不确定性的自然界中，大脑无时无刻不在进行着复杂的“价值评估”。***当草丛中传来一声异响，你是该以此为信号去捕猎（奖赏），还是该立刻逃跑（惩罚）？为了做出最优决策，大脑必须从环境线索中提取出三个关键维度的信息：

1. **显著性 (Salience)**：这个刺激有多重要？是否值得我投入注意力？（通常由刺激的物理强度或惊吓程度决定）。
2. **效价 (Valence)**：这个刺激是好的（正向）还是坏的（负向）？
3. **价值 (Value)**：结合当前的生理需求，这个刺激对我来说主观价值如何？


长期以来，认知神经科学领域面临一个巨大的挑战：这三个维度在行为上和神经表征上往往**高度相关**：例如，高价值的奖赏通常也伴随着高显著性，强烈的疼痛既是负效价也是高显著性。**这种“共线性”使得研究者难以理清大脑究竟是如何分别编码这些信息的。**

**背内侧前额叶皮层 (dmPFC)**被认为是连接环境刺激与目标导向行为的关键枢纽。虽然已有研究暗示dmPFC参与了上述维度的处理，但其神经群体究竟是混杂地编码这些信息，还是通过特定的几何结构将它们区分开来？这是一个悬而未决的谜题。本期推荐2026年1月7日发表于*Nature*的最新研究，利用**精巧的行为范式**和**双光子成像技术**，为我们揭示了dmPFC神经群体如何通过“正交几何”来解构这些动机变量。


**研究核心总结**

这项由 Daniel Jercog 团队带来的研究，通过在自由活动的雄性小鼠dmPFC区域进行大规模单神经元钙成像，结合机器学习解码技术，通过一个设计精妙的“工具性趋避任务”，**成功分离了显著性、效价和价值的神经表征**。

Fig. 1 | Behavioural framework and task used to evaluate salience, valence and value coding.

1. **核心发现：多维并存与价值主导**

研究结果表明，**dmPFC神经群体并非单一地编码某一种属性，而是通过不同的神经元子集同时对多种动机维度进行编码**。其中，**价值**(Value) 是dmPFC群体活动中最主要的编码维度。这意味着，相比于刺激的物理属性，dmPFC更关心刺激对个体当前的“主观重要性”，并据此驱动相应的行为反应。


Fig. 2 | dmPFC neural population activity consistent with value coding scheme.

1. **神经几何机制：正交编码**

这是本研究最令人兴奋的发现。为了解耦显著性和效价，研究者设计了三类刺激：

* **CSr (奖赏)**：正效价，高显著性。
* **CSs (强电击)**：负效价，高显著性（在行为反应强度上与CSr匹配）。
* **CSw (弱电击)**：负效价，低显著性。

通过构建神经状态空间（State Space），研究者发现**显著性和效价在dmPFC的神经表征中表现为近乎正交 (Orthogonal) 的信息轴**。具体而言，当研究者训练解码器区分不同效价的刺激时，该解码器无法区分不同显著性的刺激，反之亦然。这种正交的几何结构意味着，大脑可以在不干扰“好坏判断（效价）”的前提下，独立地调节“注意力强度（显著性）”，这是一种极其高效的编码策略。


Fig. 3 | Valence and salience are orthogonally represented within dmPFC networks.

1. **动态重构与因果分离**

通过“奖赏贬值（Reward Devaluation）”实验（即让小鼠喝饱水后再测试），研究者进一步验证了这种编码的独立性。结果显示，**当奖赏的主观价值降低时，CSr（奖赏线索）在神经空间中沿着显著性轴发生了特异性的移动（显著性降低），但在效价轴上保持稳定。**这说明dmPFC能够根据内部状态（如干渴程度）动态地重塑对外部线索的神经表征几何。


Fig. 4 | Identifying salience, valence and value ensembles in the dmPFC.

1. **关键意义**

该研究不仅在细胞层面解构了动机行为的神经计算机制，更重要的是**提出了dmPFC通过正交的神经流形 (Neural Manifold) 来表征复杂动机变量的理论框架**。这种几何表征使得大脑能够灵活地在不同维度上处理信息，为我们理解焦虑症、成瘾等精神疾病中出现的“价值评估异常”或“负性偏向”提供了全新的神经环路视角。


**Abstract**

Animals continuously evaluate their surroundings to decide whether to approach rewarding opportunities or avoid potential threats. Assigning the appropriate importance to environmental stimuli is not only crucial for survival but also underlies complex forms of goal-directed behaviour that are shared across species, including humans. Understanding how the brain translates such sensory cues into motivated behaviours is, therefore, central to neuroscience and psychology. The dorsomedial prefrontal cortex (dmPFC) is a critical structure that bridges relevant environmental stimuli to goal-directed behaviour. Salience, valence and value are key dimensions defining stimulus relevance, but how the dmPFC processes and organizes such dimensions to drive motivated behaviour remains unclear. Here we monitored single-neuron populations in the dmPFC using calcium imaging in freely moving male mice while discriminating between stimuli predicting different reward or punishment outcomes, which enabled an unprecedented dissociation of salience, valence and value information. We found that dmPFC populations primarily encode appetitive and aversive values of learned stimuli and that subpopulations encode valence and salience along orthogonal information axes. Our results highlight a concurrent multifaceted population coding of value, salience and valence of stimuli during associative learning within dmPFC networks, such that the geometry of dmPFC neuronal representations dynamically shapes appetitive and aversive motivated behaviours.


**请打分**

这篇刚刚登上***Nature***的研究，是否实至名归？我们邀请您作为“云审稿人”，一同品鉴。精读全文后，欢迎在**匿名投票**中打分，并在评论区分享您的深度见解。

**前沿交流****|**欢迎加入认知神经科学前沿交流群！

**⭐️****[入群链接]**


核心图表、方法细节、统计结果与讨论见原文及其拓展数据。

审核：PsyBrain 脑心前沿编辑部
