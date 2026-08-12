---
layout: post
status: publish
title: How Sogou Browser Rewrites Search Affiliate Codes
date: '2026-08-11'
categories:
- Reversing
---

I have been poking at [Sogou Browser](https://ie.sogou.com/) for a while. This post is about one specific behavior I found in a bundled plugin: when you visit a Baidu or Sogou search URL whose affiliate code appears in a list built into the browser, the browser substitutes one of its own codes before the request goes out. The search engine only ever sees the substituted code — the original never reaches it.

One naming note before we start. The product is called Sogou Browser, but the files on disk still use an older `SogouExplorer` name, so that is what you will see in the paths below.

## Affiliate codes, briefly

If you have looked closely at a Baidu search URL you have seen something like this:

```
https://www.baidu.com/s?wd=something&tn=47018152_13_dg&ie=utf-8
```

That `tn=` is a Baidu Union (百度联盟) account identifier — it tells Baidu which partner the traffic came through. This is old and well known; Firefox historically shipped `tn=suvion_dg`, Maxthon used `tn=myie2dg`. Software that ships a Baidu search box generally has its own code.

Sogou has an equivalent. Sogou search URLs carry a `p=` parameter shaped like `sogou-site-0e57098d0318a954` — a four-letter channel type and sixteen hex digits. I could not find any public documentation for this one.

## What it does

The whole behavior fits in four lines. Navigate to a Baidu search carrying an affiliate code, and this is what the browser actually requests:

```
in   https://www.baidu.com/s?wd=test&tn=47018152_13_dg&ie=utf-8
out  https://www.baidu.com/s?wd=test&tn=98010089_dg&ie=utf-8&ch=19
```

And the same on Sogou, with that engine's own `p=` scheme:

```
in   https://www.sogou.com/web?query=x&p=sogou-site-0e57098d0318a954&ie=utf8
out  https://www.sogou.com/web?query=x&p=sogou-addr-cc9657884708170e&ie=utf8
```

The code is swapped and the rest of the URL is left alone. Two conditions have to hold for it to fire at all. The URL must *begin* with `www.baidu.com` or `sogou.com` — a Sogou code carried by some other site, or a Baidu URL nested in a redirect wrapper, is ignored. And the code has to appear on a list built into the browser; anything else is left untouched.

The Baidu side does one thing more, reconciling a `ch=` parameter alongside the swap. An existing value is overwritten in place rather than duplicated:

```
in   https://www.baidu.com/s?wd=test&tn=47018152_13_dg&ch=7&ie=utf-8
out  https://www.baidu.com/s?wd=test&tn=98010089_dg&ch=19&ie=utf-8
```

## Which codes, and what they become

The lists live in a plugin called `QBSafe.dll`, loaded at browser startup, which receives every navigation URL.

For Sogou URLs there are three tables of strings in `.data`, holding 128, 219 and 246 entries — 593 in total, every one of the form `sogou-<four letters>-<sixteen hex>`, and every one distinct. Each table has a single replacement, and the tables are tried in order with the first match winning:

| entries | replaced with |
|---|---|
| 128 | `sogou-clse-f507783927f2ec27` |
| 219 | `sogou-clse-60a70bb05b08d6cd` |
| 246 | `sogou-addr-cc9657884708170e` |

For Baidu URLs there are eleven codes built directly on the stack, all mapping to one replacement:

```
tn=93912046_hao_pg   tn=68082196_oem_dg   tn=18029102_oem_dg
tn=39042058_2_oem_dg tn=02049043_35_pg    tn=47018152_13_dg
tn=02049043_32_pg    tn=47018152_8_dg     tn=02049043_50_pg
tn=93139410_hao_pg   tn=02049043_30_pg
                  ↓
            tn=98010089_dg     (plus ch=19)
```

Note that `tn=98010089_dg` does not itself appear on the list, which is what keeps the substitution from looping forever on its own output.

One implementation detail, in case you go looking. The swap is not literally a string replace: it keeps everything before the match, appends the replacement, then resumes from the next `&` rather than from the end of the matched code. For a normal URL this makes no difference, since these codes occupy the whole parameter value. It only shows up if the value has trailing content, which then gets dropped along with the code.

## On the wire

If you want to reproduce this, run the real installer rather than unpacking it. In the unpacked tree `QBSafe.dll` sits in a GUID-named folder that the browser does not look in, so the plugin never loads and nothing happens.

With the browser installed and mitmproxy in front of it, I launched a search carrying `tn=47018152_13_dg`. The only request that reached Baidu was:

```
GET https://www.baidu.com/s?wd=claude&tn=98010089_dg&ie=utf-8&ch=19
```

The original code appears zero times in the outbound capture. A short battery with controls behaved exactly as the harness predicted:

| navigated to | what left the machine |
|---|---|
| baidu `tn=02049043_35_pg` | `tn=98010089_dg …&ch=19` |
| baidu `tn=00000000_xx_yy` | unchanged |
| sogou `p=sogou-site-0e57098d0318a954` | `p=sogou-addr-cc9657884708170e` |
| sogou `p=sogou-site-ffffffffffffffff` | unchanged |
| `example.com/?p=sogou-site-0e57098d0318a954&x=1` | unchanged |

One detail worth being precise about. Internally this is not an edit of the navigation already in flight — the plugin hands back a replacement URL and the browser starts a fresh navigation to it. But the first navigation is abandoned before it issues a network request, so there are two navigations inside the browser and only one HTTP request to the search engine.

The browser's history database records only the replacement:

```
https://www.baidu.com/s?wd=claude&tn=98010089_dg&ie=utf-8&ch=19
```

The URL originally requested is in neither `urls` nor `visits`, because the handler sets `should_replace_current_entry`.

## Counting it

It is tempting to say "604 affiliates", and that would be wrong.

604 is the number of distinct *codes*: 593 Sogou plus 11 Baidu. But the eleven Baidu codes are only **seven distinct account numbers** — `02049043` appears four times with different sub-channel suffixes, `47018152` twice. And on the Sogou side the hex values are opaque, so there is no way to tell from the binary how many parties those 593 channel IDs belong to.

The defensible statement is that **604 affiliate codes collapse into 4** — three Sogou destinations and one Baidu destination.

One structural note. The 593 Sogou codes break down by channel type as 375 `site`, 82 `netb`, 43 `wsse`, 34 `clse`, 17 `navi`, 17 `brse`, 16 `addr` and a few others, while the three destinations are typed `clse`, `clse` and `addr`. Both sides belong to the same `sogou-*` scheme, so this rule maps identifiers within one namespace onto three others in it, rather than mapping between two search providers the way the Baidu rule does. What the four-letter type codes denote is not something I could determine.

## Caveats

This is one build, `13.9.6121.400`, on one machine, and I have not surveyed other versions.

I make no claim about the commercial arrangements behind any of these identifiers. I do not know what agreements exist between the parties involved, and nothing in the binary speaks to that question. This post documents what the code does, which is what I set out to determine.
