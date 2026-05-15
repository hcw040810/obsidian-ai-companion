---
title: "我用两周半 Vibe Coding 做了一个前额叶训练的微信小程序"
source: 掘金
url: https://juejin.cn/post/7637404920498323497
date: 2026-05-12
tags: [前额叶, 掘金]
---

# 我用两周半 Vibe Coding 做了一个前额叶训练的微信小程序

> 来源:
> 爬取时间: 2026-05-12

---

.markdown-body{word-break:break-word;line-height:1.75;font-weight:400;font-size:16px;overflow-x:hidden;color:#252933}.markdown-body h1,.markdown-body h2,.markdown-body h3,.markdown-body h4,.markdown-body h5,.markdown-body h6{line-height:1.5;margin-top:35px;margin-bottom:10px;padding-bottom:5px}.markdown-body h1{font-size:24px;line-height:38px;margin-bottom:5px}.markdown-body h2{font-size:22px;line-height:34px;padding-bottom:12px;border-bottom:1px solid #ececec}.markdown-body h3{font-size:20px;line-height:28px}.markdown-body h4{font-size:18px;line-height:26px}.markdown-body h5{font-size:17px;line-height:24px}.markdown-body h6{font-size:16px;line-height:24px}.markdown-body p{line-height:inherit;margin-top:22px;margin-bottom:22px}.markdown-body img{max-width:100%}.markdown-body hr{border:none;border-top:1px solid #ddd;margin-top:32px;margin-bottom:32px}.markdown-body code{word-break:break-word;border-radius:2px;overflow-x:auto;background-color:#fff5f5;color:#ff502c;font-size:.87em;padding:.065em .4em}.markdown-body code,.markdown-body pre{font-family:Menlo,Monaco,Consolas,Courier New,monospace}.markdown-body pre{overflow:auto;position:relative;line-height:1.75}.markdown-body pre>code{font-size:12px;padding:15px 12px;margin:0;word-break:normal;display:block;overflow-x:auto;color:#333;background:#f8f8f8}.markdown-body a{text-decoration:none;color:#0269c8;border-bottom:1px solid #d1e9ff}.markdown-body a:active,.markdown-body a:hover{color:#275b8c}.markdown-body table{display:inline-block!important;font-size:12px;width:auto;max-width:100%;overflow:auto;border:1px solid #f6f6f6}.markdown-body thead{background:#f6f6f6;color:#000;text-align:left}.markdown-body tr:nth-child(2n){background-color:#fcfcfc}.markdown-body td,.markdown-body th{padding:12px 7px;line-height:24px}.markdown-body td{min-width:120px}.markdown-body blockquote{color:#666;padding:1px 23px;margin:22px 0;border-left:4px solid #cbcbcb;background-color:#f8f8f8}.markdown-body blockquote:after{display:block;content:""}.markdown-body blockquote>p{margin:10px 0}.markdown-body ol,.markdown-body ul{padding-left:28px}.markdown-body ol li,.markdown-body ul li{margin-bottom:0;list-style:inherit}.markdown-body ol li .task-list-item,.markdown-body ul li .task-list-item{list-style:none}.markdown-body ol li .task-list-item ol,.markdown-body ol li .task-list-item ul,.markdown-body ul li .task-list-item ol,.markdown-body ul li .task-list-item ul{margin-top:0}.markdown-body ol ol,.markdown-body ol ul,.markdown-body ul ol,.markdown-body ul ul{margin-top:3px}.markdown-body ol li{padding-left:6px}.markdown-body .contains-task-list{padding-left:0}.markdown-body .task-list-item{list-style:none}@media (max-width:720px){.markdown-body h1{font-size:24px}.markdown-body h2{font-size:20px}.markdown-body h3{font-size:18px}}.markdown-body pre,.markdown-body pre>code.hljs{color:#333;background:#f8f8f8}.hljs-comment,.hljs-quote{color:#998;font-style:italic}.hljs-keyword,.hljs-selector-tag,.hljs-subst{color:#333;font-weight:700}.hljs-literal,.hljs-number,.hljs-tag .hljs-attr,.hljs-template-variable,.hljs-variable{color:teal}.hljs-doctag,.hljs-string{color:#d14}.hljs-section,.hljs-selector-id,.hljs-title{color:#900;font-weight:700}.hljs-subst{font-weight:400}.hljs-class .hljs-title,.hljs-type{color:#458;font-weight:700}.hljs-attribute,.hljs-name,.hljs-tag{color:navy;font-weight:400}.hljs-link,.hljs-regexp{color:#009926}.hljs-bullet,.hljs-symbol{color:#990073}.hljs-built\_in,.hljs-builtin-name{color:#0086b3}.hljs-meta{color:#999;font-weight:700}.hljs-deletion{background:#fdd}.hljs-addition{background:#dfd}.hljs-emphasis{font-style:italic}.hljs-strong{font-weight:700}
> 体验方式在最后～

最近花了两周半的时间vibe coding了一款微信小程序，这也是属于自己的第一款产品，叫「前额叶专注训练」，定位是前额叶训练小游戏。简单说，就是把舒尔特方格、数字记忆、N-Back、Stroop、go/no-go、河内塔、24 点这类认知训练任务，包装成一个轻娱乐产品：用户每天玩几局，训练自己的专注能力和记忆力。

这个项目从需求讨论、技术方案、功能实现，都是我跟 AI 一轮一轮聊出来的，自己没有写过一行代码，整个过程大概两周半，从五月初开始规划，到五月前开发完成并发布上线，备案的过程也是开始开发的时候就完成了。写这篇文章是想分享下vibe coding的一些感受。


## 第一，让AI写代码之前，一定要把需求聊清楚

从一开始的windsurf、cursor、trae到claude code和codex，我都使用过，在这里不讨论谁好用谁不好用，不管使用哪个代码编辑器，不管写多大的功能还少就是一个小的迭代，我的习惯都是先跟AI把需求聊明白，我习惯在每次对话后加上一句：先产出实现方案，等我同意再开始写代码。这样做的好处就是不用每次AI生成的代码不满意再回退，经常用AI编程的应该都深有感受，AI生成的代码一次次的回退是很招人烦的。所以，千万不要一上来就跟 AI 说“帮我写一个xxx小程序”，“帮我实现一个xxx功能”。这样做运气好的话能得到理想的效果，但是不保证每次运气都那么好。

我一开始也只是一个很模糊的想法：想做一个训练前额叶能力的小程序，而且我只知道一个舒尔特方格（我承认这个是从别人那得到的灵感），后来跟 AI 聊了之后，发现有好多可以实现的小游戏都可以用来训练专注力和注意力，这就是和AI先聊的好处。这个过程中，AI 的作用不是替我拍板，而是不断帮我把想法摊开。比如我说想做“脑力训练”，它会继续追问或展开成工作记忆、持续注意、抑制控制、认知灵活性、计划决策这些方向。然后我们再反过来判断，这些方向能不能变成普通用户愿意玩的小游戏。

确定了大概要做的内容，之后就是产出产品文档，有了产品文档之后，再让AI帮忙产出技术文档，有了这两份文档，基本是就知道该怎么实现了。另外还有一点，一定要分阶段实现，每一阶段开发完成后一定要验证，有bug就让AI改，避免最后整体验证bug数量过多的问题。

所以 vibe coding 第一步不是写代码，而是把需求聊到足够具体。你越能说清楚边界，AI 写出来的东西越接近你想要的效果。反过来，如果自己都没想清楚，AI 只会很努力地把混乱放大。

## 先实现一个能跑通的MVP版本

需求聊完之后，我没有一开始就让它帮我做完整的项目。而是先是做一个能跑通的版本，这个版本一定能跑通你的核心流程，比如我的小程序的核心流程就是用户能打开一款游戏去玩，所以我的第一版的功能就是：用户能打开小程序，能登录，能看到第一款游戏，能开始一局游戏即可。

这个链路跑通以后，说明第一版本的代码没问题，此时再往上叠加其他功能才最合适。否则你可能做了很多页面，但核心闭环其实是断的。

这样后面加游戏就和第一个游戏的开发一样，变成了一个固定流程：

1. 写游戏组件；
2. 写游戏定义；
3. 注册到游戏列表；
4. 在云函数里补评分规则。

所以项目后来能比较快地扩到 12 款游戏，不是因为每款游戏都随便生成一下就完了，而是因为前面先把模式定住了。AI 很适合在这种稳定模式下继续扩展。如果每个页面都从零开始聊，速度反而会越来越慢。

这也是我对 MVP 的理解：不是做一个很丑的半成品，而是先把最小闭环做扎实。它可以功能少，但关键链路一定要能跑。

## 即使产品失败了，没人用也不要气馁

忘了之前在哪看的，说独立开发人员在开发一款应用前都会有一种错觉，觉得自己的应用一定会火，一定有人用，我就是这样。所以在上线后天天盯着数据，发现用的人少心态都不好了，但其实成功毕竟是少数的，尤其是现在有了AI的加持，上线一款应用的成本这么低，注定会有许多人的产品一定没人用。但是并不是说没人用就一点收获都没有，以前总是想着自己作出一款属于自己的产品，这不就有了，现在试错成本这么低，多做几款又何妨。所以一定要放平心态。

## 最后的感受

两周半做出一个备案上线的小程序，在没有AI之前是不可能完成的事，但有了AI之后就将这种不可能变成了可能。AI 最大的价值，是让我一直保持“下一步能做什么”的状态。它能把模糊想法变成初稿，把初稿变成代码，把报错变成修改建议，把新功能拆成文件和步骤。

所以，不必焦虑AI把我们替代了这类问题，而是要积极的拥抱AI，用AI将自己脑子中的想法落地，这才是正解。

## 打个广告，欢迎体验，有问题欢迎私聊～

打开微信搜一搜：前额叶专注训练

也欢迎扫码体验


