---
layout: post
status: publish
title: Detecting Insecure Software Updates at Scale with LLM Agents
date: '2026-09-16'
description: I used a hierarchy of LLM agents to analyze how 3,006 open-source projects deliver software updates.
images:
- /posts/reversing/detecting_insecure_software_updates_at_scale/agent-architecture-v3.png
categories:
- Reversing
---

## TL;DR

- I used a hierarchy of low-cost source-reading agents, stronger review agents, and manual verification to trace how **3,006 open-source projects** handle software updates.
- I found **624 with an updater** that could download and then install, load, or execute code: 134 used a pinned signing key, 109 enforced a publisher identity, 332 relied only on HTTPS, and **49 used broken transport security**. The other 2,382 had no updater or were notification-only.
- In those **49 projects**, a man-in-the-middle attacker could replace update payloads and achieve remote code execution on users' machines.

Browse the [dataset](https://xusheng6.github.io/update-security-study/) or inspect and correct it in the [public repository](https://github.com/xusheng6/update-security-study).

## Why update security matters

An updater downloads code and places it inside a trusted application. It may launch an installer, replace an executable, load a plugin, or flash firmware. That makes it a natural supply-chain target.

[SolarWinds](https://www.cisa.gov/news-events/alerts/2020/12/13/active-exploitation-solarwinds-software) distributed malicious code through trusted Orion updates. In 2023, attackers compromised the [3CX](https://cloud.google.com/blog/topics/threat-intelligence/3cx-software-supply-chain-compromise) build environment after first compromising another software package. In 2025, attackers compromised infrastructure used by [Notepad++](https://notepad-plus-plus.org/news/hijacked-incident-info-update/) and selectively redirected update requests toward malicious payloads.

These incidents had different root causes, but they point to the same trust boundary: **an application should not execute a downloaded file merely because it came from its usual server**. Properly validated HTTPS blocks ordinary network interception, but it does not help when the server, CDN account, storage bucket, or deployment credentials are compromised. Independent payload signatures can protect against that narrower—but important—class of attack.

This problem is not new. A [2006 HotSec study](https://www.usenix.org/legacy/event/hotsec06/tech/full_papers/bellissimo/bellissimo.pdf) examined ten deployed update systems and found several vulnerable to weak man-in-the-middle attacks. Two decades later, [UpdSight](https://www.usenix.org/conference/usenixsecurity26/presentation/wan) tested 85 desktop applications and found 22 exploitable update vulnerabilities. Those studies performed deeper hands-on testing of smaller samples. My goal was different: use agent-assisted source review to scale the initial survey to 3,006 open-source projects, then manually review the 49 Tier-D findings.

## What I scanned

For each project, I asked:

1. Does it update itself or install executable content?
2. If so, what authenticates the content before it runs?

The agents followed the entire path:

```text
check version
  -> obtain manifest
  -> choose payload URL
  -> download payload
  -> verify or skip verification
  -> install / execute / load / flash
```

A `verifySignature()` function is not evidence by itself. It must check the relevant payload, use a trustworthy key, and stop installation on failure. Likewise, a SHA-256 value downloaded beside the payload from the same server is not independent authentication.

## The four tiers

I used tiers because update security depends on the threat model. Tier C validates HTTPS and is not immediately vulnerable to an ordinary network attacker. But a high-security user may reject it because a compromised server or CDN can replace both the package and its hash.

I also recorded the underlying facts—transport settings, signatures, trusted keys or publishers, and source locations—rather than only a verdict. Each tier summarizes the trust model of one update path, not the security of an entire project.

### A — application-pinned signing key

```python
package, signature = download_update()
trusted_key = key_embedded_in_application

if verify(trusted_key, package, signature):
    install(package)
else:
    reject()
```

Compromising the website, CDN, DNS path, or repository is insufficient without an accepted signing key. Sparkle’s EdDSA support is one example: the public key is embedded in the application while the private key should remain separate from the update server.

### B — expected operating-system publisher

```python
package = download_update()
signature = os_code_signature(package)

if signature.valid and signature.publisher == EXPECTED_PUBLISHER:
    install(package)
else:
    reject()
```

The updater enforces the expected Authenticode or platform-signing identity. Merely checking that *someone* signed the file is not enough.

### C — validated HTTPS only

```python
manifest = https_get(server, verify_certificate=True)
package = https_get(manifest.url, verify_certificate=True)

if sha256(package) == manifest.sha256:
    install(package)
```

This blocks ordinary man-in-the-middle attacks. It does not survive compromise of the authorized distribution path because the attacker can replace both the package and its server-supplied hash.

### D — broken transport, no independent signature

```python
client.verify_peer = False
client.verify_hostname = False

manifest = client.get("https://updates.example/manifest.json")
package = client.get(manifest.url)
install(package)
```

The older version is even simpler: download an executable over HTTP and run it. Either design may allow an on-path attacker to substitute code.

Some projects used HTTPS but disabled certificate validation. Static analysis cannot tell us why. CA-bundle deployment problems, old certificate stores, and forgotten debugging workarounds are plausible explanations—not established causes.

I used **N** when no in-app updater was found or the application only opened a download page. N does not mean every external package manager or manual installation route is secure.

## Results

| Label | Entries | All entries | A–D only |
|---|---:|---:|---:|
| **A** — pinned payload key | 134 | 4.5% | 21.5% |
| **B** — expected publisher | 109 | 3.6% | 17.5% |
| **C** — validated HTTPS only | 332 | 11.0% | 53.2% |
| **D** — broken transport | 49 | 1.6% | 7.9% |
| **N** — none or notification-only | 2,382 | 79.2% | — |
| **Total** | **3,006** | **100%** | — |

The dataset contained **624 entries (20.8%)** with such an updater and **2,382 (79.2%)** with no updater or only update notifications. Among the 624 updater entries, Tier C was the largest group.

These are **dataset entries**, not 3,006 verified unique applications. The corpus contains duplicate projects, platform-specific implementations, and separate application, plugin, firmware, and content channels. It was collected for breadth rather than statistical sampling. The percentages describe this dataset—not all open-source software.

## The agent architecture

I performed the core research from **August 3–23, 2026**. Claude Opus 4.8 was the strongest model I used in that Claude Code workflow, but using it to read every repository would quickly exhaust the five-hour and weekly limits. I worked with an Opus 4.8 coordinator, while many Claude Sonnet 5 agents handled the broad source review. Opus 4.8 review agents consolidated the reports and rechecked suspected Tier-D findings.

![The researcher works with an Opus 4.8 coordinator, Opus reviewers, and Sonnet 5 source-reading agents. Reviewers send Tier A, B, and C results directly to the dataset, while suspected Tier-D findings receive manual review before entering it.](/posts/reversing/detecting_insecure_software_updates_at_scale/agent-architecture-v3.png)

The bulk agents cloned source with shallow history, searched for updater code, and recorded the revision, platform, behavior, transport, verification, trust root, and `file:line` evidence. They were read-only: no builds, dependency installation, or execution of repository code.

The final expansion from 2,008 to 3,006 entries took about **15 hours** and approximately **8.5 million subagent tokens**. Small, lower-cost contexts handled the repetitive reading; higher-cost reasoning was reserved for consolidation, disagreement, and findings with security impact.

The initial pass produced **73 Tier-D candidates**. Suspected vulnerabilities entered a feedback loop: stronger agents re-read the source and tried to disprove them. That pass retained 51 as D, moved six to C, moved fourteen to N, and refuted two. Later corrections produced the published historical count of 49.

This is why the hierarchy matters. Sonnet provided coverage; the adversarial Opus pass raised the bar before I called something broken. I then read all 49 final Tier-D findings myself before disclosure.

## Responsible disclosure

I tried to contact maintainers before publishing actionable Tier-D findings. The disclosure ledger records:

- **9** GitHub Private Vulnerability Reports
- **16** coordinated-disclosure emails
- **25** projects contacted in total

I could not find a usable private contact channel for the remaining 24 Tier-D projects. Of the 25 projects I contacted, two responded positively: [FOG Project](https://github.com/FOGProject/fogproject) and [SuiteCRM](https://github.com/SuiteCRM/SuiteCRM). Both fixed the reported issues.

Writing 25 fully bespoke reports is difficult to scale. My compromise was to write the important opening myself—what I found, why I was contacting the project, and what I wanted the maintainer to do—then attach AI-assisted technical detail with the relevant code path and suggested remediation. That is not ideal, and some maintainers understandably disliked receiving AI-generated material. But silently publishing the findings, or sending no notification at all, would have been worse. The better lesson is that automation must reduce clerical work without replacing evidence review, respectful communication, or accountability for the report.

Some maintainers also challenged the threat model. Two recurring objections were that an attacker would need a fraudulent certificate for GitHub, or that an on-path attacker was unrealistic. Those objections do not apply when the updater itself disables certificate or hostname validation: the attacker can present an arbitrary certificate and does not need to break public-key cryptography or compromise a certificate authority.

An active on-path position is a real prerequisite for many Tier-D findings, and it should be stated rather than exaggerated. Possible positions include a hostile network, compromised router, malicious proxy, or redirected traffic. Server or CDN compromise is a stronger and different position—the main concern for Tier C—but repeated supply-chain incidents show that distribution infrastructure cannot be assumed infallible.

## Where I want the ecosystem to move

Tier D is the immediate problem: plaintext HTTP, disabled certificate checks, or ignored TLS errors should be fixed.

Tier C is the larger supply-chain concern. TLS may work perfectly while a compromised server returns a malicious manifest and matching payload. The Notepad++ incident shows why distribution infrastructure should not be the only trust root.

The practical direction is straightforward:

- **Tier D → C:** require HTTPS, certificate validation, and hostname validation
- **Tier C → A/B:** authenticate the payload independently of the download server
- Fail closed on missing, invalid, or unexpected signatures
- Keep signing keys separate from public distribution infrastructure
- Test corrupted, unsigned, wrongly signed, and rolled-back updates

Projects do not need to invent this themselves. [The Update Framework](https://theupdateframework.io/) provides role separation, threshold signatures, rotation, and defenses against rollback and freeze attacks. [Sparkle](https://sparkle-project.org/) supports EdDSA-signed macOS updates with a public key embedded in the application and can also require signed feeds.

The data remains public and correctable:

- [Search all 3,006 analyses](https://xusheng6.github.io/update-security-study/)
- [Review the evidence](https://github.com/xusheng6/update-security-study)
- [Propose a correction](https://github.com/xusheng6/update-security-study/issues/new)
