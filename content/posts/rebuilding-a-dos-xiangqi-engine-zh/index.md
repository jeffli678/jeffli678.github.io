---
layout: post
status: publish
draft: false
build:
  list: never
aliases:
- /zh-cn/posts/rebuilding-a-dos-xiangqi-engine/
title: "让《象棋大师 III：将族》重新运行起来"
date: '2026-09-08 00:00:00 -0400'
description: 用 Codex 将一款 1992 年的 DOS 象棋引擎重写为 C，并与原版逐一比较了四十多万个测试局面。
categories:
- Reverse Engineering
tags:
- Xiangqi
- DOS
- software preservation
- reverse engineering
- game AI
---

[English version](/posts/rebuilding-a-dos-xiangqi-engine/)

《象棋大师 III：将族》是一款曾经很受欢迎的 DOS 象棋游戏。开发公司的[历史介绍](https://games.sina.com.cn/zhuanqu/guangpu/intro.shtml)称，它累计卖出了 20 万套。我年轻时和它下过不少棋，大部分都赢了。我是一名[象棋国际特级大师](https://xusheng.dev/posts/grandmaster/)，赢它倒不算意外，但我仍觉得它是个值得一战的对手。

我父亲也喜欢象棋，年轻时玩过这款游戏。后来我发现了他的游戏盘，也拿来玩了一阵。它发行于 **1992 年**，正好是我出生的那一年。

{{< figure src="/posts/rebuilding-a-dos-xiangqi-engine/jiangzu-title.png" alt="DOSBox-X 中的《将族》标题画面：金色书法和红色印章" caption="《将族》的标题画面。截图来自 [DOSBox-X](https://dosbox-x.com/)，原游戏美术的权利归其各自权利人所有。" >}}

我很喜欢它的界面，尤其是选择对手的页面。里面有《西游记》中的人物，每个角色都有头像和一段介绍。

{{< figure src="/posts/rebuilding-a-dos-xiangqi-engine/opponent-selection.png" alt="翻开的书本式选人界面，展示 Spoon Sa 的头像、简介和棋力等级" caption="选择对手的界面，当前选中的是英文版中的 Spoon Sa。" >}}

后来，我不想每次都启动 DOS 才能和它下棋。能不能把引擎重写出来，放到现代象棋界面里运行？

**太长不看：** 在 Codex 的帮助下，我用 C 重写了这款引擎，加入 UCI/UCCI 支持，并用 **408,708 个测试用例**与原版进行比较。[代码在 GitHub 上](https://github.com/xusheng6/cch-cms1)。

## 游戏的来历

这款游戏由**虞希舜**和**光谱资讯**开发。它源于虞希舜早期编写的象棋程序，后来加入图形界面、不同角色和挑战赛制，成为商业 DOS 游戏。[这篇历史回顾](https://read.99csw.com/book/579/18112.html)介绍了 1992 年的《将族》如何从此前的程序发展而来。

游戏里的 36 个对手看起来各有个性，实际用的却是同一个引擎。其中七个采用固定的两层搜索，大致相当于走一步、看对方应一步，遇到吃子等战术情况还会继续搜索。其余对手使用不同的对局时限，引擎据此分配思考时间。例如，Bogey 是 1 分钟，Hand 是 8 分钟，Skeleton 是 47 分钟。这些都是整局时限，不是每步可以想那么久。

所以，角色主要改变的是搜索预算，而不是引擎对棋局的理解。有些角色的实际设置甚至完全一样。

## 重写引擎

我让 Codex 分析游戏并编写可移植的 C 版本。我们用 [Binary Ninja](https://binary.ninja/) 和反汇编分析 DOS 代码，再通过 [DOSBox-X](https://dosbox-x.com/) 运行游戏，保存初始化后的内存。

{{< figure src="/posts/rebuilding-a-dos-xiangqi-engine/game-board.png" alt="原版象棋对局界面，左侧上下分别是 Spoon Sa 和玩家的头像" caption="与 Spoon Sa 对弈的原版界面。重写项目只包含引擎，没有重做这套图形界面。" >}}

引擎位于 `CMS1.EXE`，由游戏主程序 `CCH.EXE` 加载。它采用传统的象棋引擎设计：用 alpha-beta 搜索分析着法和应对，再用人工编写的规则与数值表评估局面。

让重写版能下棋，只完成了一部分工作。它很快就在许多局面上与原版一致，但仍有不少不一致的情况。我想要的不只是一个下得还可以的引擎，而是尽量还原这个引擎本来的选择。

这就需要恢复那些细节：准确的评估常量、着法顺序、重复局面的处理，以及搜索中的特殊分支。

重写版大约有 [**3,400 行 C 代码**](https://github.com/xusheng6/cch-cms1/tree/main/port)。

## 建立反馈循环

与其反复告诉 Codex“再准确一点”，我更希望有一套能不断重复的测试流程。

我们用 [Unicorn](https://www.unicorn-engine.org/) 搭建了测试工具，直接执行原版的 16 位引擎代码，不再需要操作 DOS 图形界面。这样就可以：

1. 从合法的走子历史生成一大批局面。
2. 关闭开局库，让原版和重写版以相同深度搜索。
3. 比较它们选择的着法和给出的分数。
4. 分析差异、修复重写版，再生成新局面重复测试。

我理解的 **harness engineering**，在这里就是给编程智能体配上一套能运行代码、衡量结果并提供明确反馈的工具。原程序就是参照，不必仅凭一段翻译出来的代码“看着没问题”来判断它是否正确。

有些差异非常小。比如一次，两边选择了同一步棋，但原版给 157 分，重写版给 156 分。最后发现，原因是在应对炮将军时，搜索解将着法的顺序不同。修正顺序后，这个差异就消失了。

测试越来越快，我也不断要求扩大样本。一批全部匹配，就再生成一批。

![测试用例数量随开发检查点增长，最终达到 408,708](/posts/rebuilding-a-dos-xiangqi-engine/progress.svg)

图中展示的是测试集的增长，不是准确率。最终，重写版在 **408,708 个用例**上给出了与原版相同的着法和分数。大部分测试深度为 2–4 层，另有一小批更深的搜索。最后三批新生成的浅层测试各有 20,000 个用例，都没有发现差异。

这不代表重写版在所有局面下都与原版一致。[程序等价性在一般情况下是不可判定的](https://arxiv.org/abs/2507.07480)；对这个项目来说，持续测试后不再发现差异，已经让我有足够信心认为重写成功了。

## 棋力如何？

我也想大致测一下它的棋力。全力运行的 [Pikafish（皮卡鱼）](https://github.com/official-pikafish/Pikafish) 太强，所以我们使用了带有棋力校准功能的版本：`UCI_LimitStrength` 开启降棋力模式，`UCI_Elo` 设置目标等级分。

对阵设为 1400 的皮卡鱼，CCH 取得了 13 胜、11 负。据此估算，它在**皮卡鱼的引擎等级分标尺上约为 1,429 分**。样本不大，误差范围也很宽，不能当作正式的人类棋手等级分。这些比赛也发生在最后一轮还原修正之前。

我们还测试了另一个开源象棋引擎 ElephantEye（象眼）。它远弱于全力运行的皮卡鱼，但仍明显强于 CCH：对阵我们扩大缓存后的实验版 CCH，它取得了 8–0 的成绩。[验证说明](https://github.com/xusheng6/cch-cms1/blob/main/VALIDATION.md#strength-is-a-different-question)中记录了这些比较的局限。

这并不影响我对这款游戏的感情。我想找回的是父亲和我都下过棋的老对手，而不是把它变成今天的冠军。

现在，重写版可以原生运行，支持 UCI 和 UCCI，也能接入我的象棋界面 Pikaboard。[代码仓库](https://github.com/xusheng6/cch-cms1)包含引擎和基本测试，不包含原游戏程序、开局库或美术资源，但保留了从原版恢复的数值表。相关来源和许可范围见 [NOTICE](https://github.com/xusheng6/cch-cms1/blob/main/NOTICE.md)。

这个和我同年出生的引擎，还可以继续下棋。
