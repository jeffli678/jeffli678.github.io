---
layout: post
status: publish
title: How Sogou Browser Rewrites Search Affiliate Codes
date: '2026-08-11'
categories:
- Reversing
---

I recently poked at [Sogou Browser](https://ie.sogou.com/) (version `13.9.6121.400`) out of curiosity and found that it rewrites hundreds of affiliate codes in Baidu or Sogou search URLs. Specifically, there is a list of search affiliate codes hardcoded in the binary, and when one is seen, it is replaced. The search engine only ever sees the substituted code — the original never reaches it.

## Affiliate codes, briefly

If you have looked closely at a Baidu search URL you have seen something like this:

```
https://www.baidu.com/s?wd=something&tn=47018152_13_dg&ie=utf-8
```

That `tn=` is a Baidu Union account identifier — it tells Baidu which partner the traffic came through. This is old and well known; Firefox historically shipped `tn=suvion_dg`, Maxthon used `tn=myie2dg`. Software that ships a Baidu search box generally has its own code.

Sogou has an equivalent. Sogou search URLs carry a `p=` parameter shaped like `sogou-site-0e57098d0318a954` — a four-letter channel type and sixteen hex digits.

## Replacing the codes

When a Sogou Browser user navigates to a Baidu search carrying an affiliate code, this is what the browser actually requests:

```
in   https://www.baidu.com/s?wd=test&tn=47018152_13_dg&ie=utf-8
out  https://www.baidu.com/s?wd=test&tn=98010089_dg&ie=utf-8&ch=19
```

And the same on Sogou, with that engine's own `p=` scheme:

```
in   https://www.sogou.com/web?query=x&p=sogou-site-0e57098d0318a954&ie=utf8
out  https://www.sogou.com/web?query=x&p=sogou-addr-cc9657884708170e&ie=utf8
```

The code is swapped and the rest of the URL is left alone. On the Baidu side a `ch=19` parameter is set as well, overwriting any existing `ch` value rather than duplicating it.

Two conditions have to hold for it to fire at all. The URL must *begin* with `www.baidu.com` or `sogou.com` — a Sogou code carried by some other site, or a Baidu URL nested in a redirect wrapper, is ignored. And the code has to appear on a list built into the browser; anything else is left untouched.

## The list of codes

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

## MITM verification

To confirm my finding, I set up mitmproxy in front of the browser and observed the behavior:

| navigated to | what left the machine |
|---|---|
| baidu `tn=02049043_35_pg` | `tn=98010089_dg …&ch=19` |
| baidu `tn=00000000_xx_yy` | unchanged |
| sogou `p=sogou-site-0e57098d0318a954` | `p=sogou-addr-cc9657884708170e` |
| sogou `p=sogou-site-ffffffffffffffff` | unchanged |
| `example.com/?p=sogou-site-0e57098d0318a954&x=1` | unchanged |


You might be curious why Sogou is doing this. There are many possible reasons, and I will leave that to interested readers.
