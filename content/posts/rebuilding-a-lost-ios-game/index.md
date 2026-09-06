---
layout: post
status: publish
draft: false
title: "Rebuilding a Lost iOS Game: From Screenshots to Reverse Engineering to AI"
date: '2026-09-06 00:00:00 -0400'
description: How I recovered a delisted iOS puzzle game, reconstructed its exact mechanics, and benchmarked several agents that learned to play it.
images:
- /posts/rebuilding-a-lost-ios-game/hexris-piece-catalog.png
categories:
- Reverse Engineering
tags:
- iOS
- reverse engineering
- game AI
- Flutter
---

My wife used to play an iOS puzzle game called *Block Crush Blitz*. When we wanted to install it on a new iPad in march 2026, we found that it was no longer available in the App Store. She liked the game, and it did not look too complicated to recreate. So I decided to give it a try. Happy wife, happy life.

I started by asking [Claude](https://claude.ai/) to rewrite it from screenshots. That got us a working game quite quickly, but some of the pieces were different from the original. To figure out which pieces should actually appear, I eventually had to download the old app, buy an iPhone, jailbreak it, and reverse engineer the executable. Then I got distracted by another idea: how well could an AI play this game?

## The first attempt: rebuild what I could see

In March 2026, I gave Claude screenshots of the original game and asked it to recreate it. The rules are simple: drag a piece onto the board, and when a line is full, the blocks on that line disappear. On the hexagonal board, lines can run in three directions.

I asked Claude to reproduce the shapes and colors in the images. I used [Flutter](https://flutter.dev/) so I could run it on both the iPad and my Mac, and I called the remake [Hexris](https://github.com/xusheng6/hexris). The source code is available in that GitHub repository. After a few rounds of fixing dragging and adjusting the piece sizes, it was playable.

{{< image src="/posts/rebuilding-a-lost-ios-game/hexris-game.png" alt="The first Hexris remake running in hex mode" style="display: block; max-height: 600px; max-width: 100%; width: auto; height: auto; margin: 1.5rem auto;" >}}

However, after playing it for a while, we noticed that some pieces did not seem to belong. The remake generated shapes that we did not remember seeing in the original, and some were quite difficult to place.

I tried removing the shapes that seemed wrong. This improved the game, but I was still relying on memory. I did not know whether I had removed the right pieces, or whether the remaining ones appeared with the right frequencies.

At that point I wanted to find the original app and look at its code. There had to be a piece generator somewhere in it.

## Recovering a delisted IPA

Getting a copy was harder than I expected. The app was no longer listed in either the Chinese or US App Store. I also thought I might have saved a copy on my Mac, but could not find one.

Fortunately, my wife's Apple ID had acquired it in 2016. Although the listing was gone, Apple still had a copy available to that account. An archived store page helped us identify the App Store ID, `1052414239`, and bundle ID, `com.balabafire.1010hex`.

I used [ipatool-py](https://github.com/yuhao7370/ipatool-py) to download it from Apple. The downloader needed some fixes because Apple's authentication endpoints had changed, but eventually it worked. I got version 1.7, an IPA of about 11 MB.

Of course, an IPA downloaded from the App Store is still encrypted with FairPlay. Both the ARMv7 and ARM64 slices had `cryptid 1`. I could inspect the resources and some unencrypted data, but the code I needed was in the encrypted region.

## Why a virtual iPhone was not enough

I did not have a jailbroken device, so I first looked into using [Corellium](https://www.corellium.com/). I hoped I could sign into the account on a virtual iPhone, launch the app, and dump the decrypted code there.

That did not work out. Corellium requires an already-decrypted IPA for this use; its virtual devices cannot run the encrypted App Store copy through the normal Apple services. I had the wrong half of the solution.

I bought an iPhone 8 Plus and jailbroke it with [palera1n](https://github.com/palera1n/palera1n). Getting the phone into DFU mode took many attempts. I watched videos, retried the button sequence, and kept seeing the Apple logo. After replacing the USB cable, I finally got it working. I had spent quite a bit of time blaming my button timing.

I then signed into the account that had acquired the app and installed the encrypted copy using `appinst`, with [AppSync Unified](https://github.com/akemin-dayo/AppSync) on the phone. It launched! This worked because the authorization to use the purchased app was tied to the Apple ID, rather than limited to the device on which it was originally downloaded. I could use that account on the newly bought iPhone to run the encrypted copy, even though the app was no longer listed in the store.

For the dump, I used [ipadecrypt](https://github.com/londek/ipadecrypt), which handled the device-side helper and produced a decrypted IPA for analysis. It used [OpenSSH](https://www.openssh.com/) to communicate with the phone, with the USB connection forwarded through `iproxy` from [libusbmuxd](https://github.com/libimobiledevice/libusbmuxd).

This was a nice discovery on its own. An app disappearing from the store does not necessarily mean its binary is lost. In this case, a previous purchase let me download it, and a compatible physical device let me run it. It still depends on Apple serving the app and on the old app working on the available iOS version. A purchase record alone cannot guarantee either of those things.

## Reverse engineering the game

The game uses [Cocos2d-x](https://github.com/cocos2d/cocos2d-x) and native C++. Before decryption, we had already checked the resources for shape definitions. There were UI scenes and sprite atlases, but no gameplay scripts or per-piece images. The game draws pieces by repeating a single hexagonal sprite. The actual shapes were defined in the executable.

With the decrypted ARM64 code open in [Binary Ninja](https://binary.ninja/), we could finally follow the catalog construction and random selection routines. The answer to my original question was quite specific: hex mode has **22 possible pieces**, consisting of a one-cell dot and 21 four-cell shapes. Each entry is selected uniformly, with a probability of `1/22`, or about 4.545%.

There were also two masks elsewhere in the configuration that looked like pieces, but they were not added to the active catalog. Simply collecting every shape-like constant would have given us the wrong answer. We needed to follow how the generator used them.

![The 22 recovered hex pieces](/posts/rebuilding-a-lost-ios-game/hexris-piece-catalog.png)

We also checked the surrounding rules. The board has 61 cells, with nine across the middle. Full lines clear along three axes. A used tray slot is replaced immediately, and the game ends when none of the three available pieces can fit. The level calculation does not change the active hex piece distribution in version 1.7; all 22 entries are already available at level one.

Scoring was another difference from the first remake. Ordinary placement gives no points. When a move clears lines, it awards:

```text
distinct cells removed + lineCount × (10 + 5 × (lineCount - 1))
```

Intersections count only once among removed cells. The line bonuses are therefore 10, 30, 60, and 100 points for one, two, three, and four simultaneous lines.

The square mode turned out to use a different generator. It selects one of nine shape families using integer weights totaling 20, then selects an orientation uniformly within that family. For example, the dot and 3×3 square each occur 5% of the time, while the 2×2 square occurs 15%. Hex mode is simpler: all 22 active catalog entries are equally likely.

I asked AI to add the recovered rules to Hexris as an optional Classic mode, keeping Undo for convenience. The previous version remains the default, so we can play either one.

## Then I wondered: can an AI play it?

After getting the rules working, I suddenly wanted to see how well an AI could play. I asked the coding agent to try a few approaches using a simulator of the recovered hex rules.

We compared random moves, a greedy player that evaluates one move at a time, a trained version of that evaluator, and two search methods that look ahead at possible future pieces. Each played the same 20 seeded games, with a limit of 1,000 moves per game:

| Agent | Mean score | Median score |
|---|---:|---:|
| Random | 49.75 | 18.5 |
| Greedy | 1,055.30 | 899.5 |
| Learned linear | 1,061.95 | 661.0 |
| Sampled expectimax | **3,721.55** | 2,537.0 |
| Stochastic rollout | 3,256.90 | **2,777.0** |

Looking ahead helped much more than tuning the evaluator. Expectimax had the highest average score, with its best game reaching 10,346. Rollout had a slightly better median, but took more than twice as long.

I also tried a small neural network. Combined with search, it averaged 2,532 points in a separate test, versus 5,074 for the handwritten evaluator on the same seeds. So the neural version did not improve things this time.

My wife's best was around **6,000 points**. This was not a controlled comparison, but it was fun to see some of the agents' games exceed that score.

I originally expected to spend a little time getting Claude to draw a board and some pieces. I certainly did not expect to buy an old iPhone to find out which pieces belonged in it. But now I think it is totally worth the time and effort!
