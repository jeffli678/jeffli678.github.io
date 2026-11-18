---
title: "Research"
---

I take apart software and devices to test their security and privacy claims. Projects are ordered by their latest publication, talk, or advisory.

## [Windows tracks coding-agent use](#windows-coding-agent-telemetry) {#windows-coding-agent-telemetry}

*Latest publication: November 2026*

Windows records which coding agents and developer tools you run. I found the feature in a Windows 11 component and observed a diagnostic event queued for upload when optional diagnostics were enabled. The event records the coding agent itself, not prompts or source code.

### Publication

- [*Windows 11 Is Collecting Data on Which Coding Agents and Developer Tools You Use*](/posts/windows-coding-agent-telemetry/)
- [Initial research post on X](https://x.com/CrackmesOne/status/2122147747390468384)

### Selected coverage

- [Hackaday](https://hackaday.com/2026/11/17/coding-on-windows-redmond-may-already-know/)
- [GIGAZINE](https://gigazine.net/gsc_news/en/20261117-windows-coding-agent-telemetry/)
- [Dr. Web](https://www.drweb.de/windows-11-coding-agenten-diagnosedaten/)
- [Hacker News discussion](https://news.ycombinator.com/item?id=50524736)

## [UTM VM escape](#utm-vm-escape) {#utm-vm-escape}

*Fix released: November 2026*

A malicious VM guest could execute code in UTM’s host-side renderer. The renderer remains sandboxed, but the flaw crossed the guest boundary. UTM credited my report and fixed the issue in version 5.0.9.

### Vendor release note

- [UTM 5.0.9 release and full notes](https://github.com/utmapp/UTM/releases/tag/v5.0.9)

## [Software-update security at scale](#software-update-security) {#software-update-security}

*Study published: September 2026; public advisory: November 2026*

An updater can turn a network attack into code execution. I studied 3,006 open-source project entries and found 49 update paths with broken transport security. A separate study of 1,000 binary-distributed products found 10 vulnerable product-and-platform paths. The work led to public fixes and an advisory.

### Publications and data

- [*Detecting Insecure Software Updates at Scale with LLM Agents*](/posts/reversing/detecting_insecure_software_updates_at_scale/main/)
- [Public dataset and study site](https://xusheng6.github.io/update-security-study/)

### Advisory, fixes, and vendor follow-up

- [SnappyMail GHSA-j9c4-gf64-rph2](https://github.com/the-djmaze/snappymail/security/advisories/GHSA-j9c4-gf64-rph2)
- [Akaunting update fix (pull request #3401)](https://github.com/akaunting/akaunting/pull/3401)
- [FOG Project update fix](https://github.com/FOGProject/fogproject/commit/a92d061e0790a40a6edf6ed80fc5852b9e0cef07)
- [Cemu update fix](https://github.com/cemu-project/Cemu/commit/a1cd67ca111437db680fa3560a19a8a34d085926)
- [EastWest Installation Center updates](https://www.soundsonline.com/support/updates)

## [Bring Your Own Trusted Caller (BYOTC)](#byotc) {#byotc}

*Latest presentation: October 2026*

Some Windows drivers trust the caller more than the request. I showed how control of a trusted client can open a path to privileged driver operations. The research includes a published analysis, a BSides Portland talk, and accepted LOLDrivers entries.

### Publication

- [*Bring Your Own Trusted Caller (BYOTC): A New Way to Exploit Vulnerable Windows Drivers (Part 1)*](/posts/byotc/main/)

### Talk

- [BSides Portland, October 23, 2026: speaker and talk listing](https://bsidespdx.org/events/2026/speakers)

### Accepted LOLDrivers entries

- [Malwarebytes Chameleon (`mbamchameleon.sys`)](https://www.loldrivers.io/drivers/c2feb6de-46fe-44ab-93c2-634ea6ab83a2/)
- [Panda Security (`pskmad.sys`)](https://www.loldrivers.io/drivers/b9216fc9-860e-43ae-8db2-e970c7e76b46/)
- [Huorong (`sysdiag.sys`)](https://www.loldrivers.io/drivers/11d2230e-d9a4-5841-a508-ca8ffa827e56/)
- [Antiy ATool (`AToolsKrnl64.sys`)](https://www.loldrivers.io/drivers/643b121c-f883-5699-a032-f07c1e9eecfd/)
- [360 Total Security (`360FsFlt_win10.sys` and `360Box64_win10.sys`)](https://www.loldrivers.io/drivers/5cb0463b-cf28-56b7-b5cc-f2003c5c78d1/)

## [Encrypted USB drives that failed to protect files](#encrypted-usb) {#encrypted-usb}

*Latest publication: October 2026*

One “encrypted” USB drive stored files on an ordinary, unencrypted SD card. Across other products, I found exposed passwords, fixed keys, and bypassable unlock checks. The [project site](https://encrypted-usb.fail/) tracks each device, vendor response, and the broader coverage.

### Publications

- [*Discovering a Backdoor and Flaws in More Encrypted USB Drives*](https://binary.ninja/2026/10/22/breaking-more-encrypted-usb-drives-with-ai.html)
- [RE//verse 2026 talk, *Breaking Encrypted USB Drives with Time-Travel Debugging*](https://www.youtube.com/watch?v=Rv6jdnQ4YhY)
- [*Examining USB Copy Protection* in *Paged Out!*, issue 5](https://pagedout.institute/download/PagedOut_005.pdf)

### CVEs

- Lenovo [CVE-2025-13453](https://www.cve.org/CVERecord?id=CVE-2025-13453)
- Lenovo [CVE-2025-13454](https://www.cve.org/CVERecord?id=CVE-2025-13454)
- Lenovo [CVE-2025-13455](https://www.cve.org/CVERecord?id=CVE-2025-13455)

### Selected coverage

- [Tom's Hardware](https://www.tomshardware.com/tech-industry/cyber-security/lenovo-fingerprint-usb-stick-sold-as-aes-256-encrypted-had-a-plain-sd-card-inside-ai-assisted-follow-up-finds-a-backdoor-and-hardcoded-keys-in-other-secure-usb-products)
- [GIGAZINE](https://gigazine.net/news/20261102-lenovo-fingerprint-usb-not-encrypted/)
- [*Security Now!* episode 1103](https://www.grc.com/sn/SN-1103-Notes.pdf)
- [More coverage and publications](https://encrypted-usb.fail/)

## [Seven Affinity CVEs](#affinity) {#affinity}

*Public advisories: October 2026*

Seven Affinity flaws received CVEs. I found memory-safety problems in document parsing and macOS QuickLook previews that could be triggered by crafted Affinity files. Canva credits the research in its security advisory.

### Canva advisory and credit

- [Canva Trust: Affinity vulnerabilities and researcher credit](https://trust.canva.com/?tcuUid=1998378a-9134-47e9-b761-7a49d5fd6bfb)

### CVEs

- [CVE-2026-96393](https://www.cve.org/CVERecord?id=CVE-2026-96393) — out-of-bounds pointer dereference in document parsing
- [CVE-2026-96394](https://www.cve.org/CVERecord?id=CVE-2026-96394) — out-of-bounds read in QuickLook image dimensions
- [CVE-2026-96395](https://www.cve.org/CVERecord?id=CVE-2026-96395) — out-of-bounds heap read in QuickLook
- [CVE-2026-96396](https://www.cve.org/CVERecord?id=CVE-2026-96396) — image-buffer integer overflow in QuickLook
- [CVE-2026-101094](https://www.cve.org/CVERecord?id=CVE-2026-101094) — heap buffer over-read in UTF-8 parsing
- [CVE-2026-101130](https://www.cve.org/CVERecord?id=CVE-2026-101130) — heap buffer over-read in string-array parsing
- [CVE-2026-103220](https://www.cve.org/CVERecord?id=CVE-2026-103220) — raster-data out-of-bounds read and untrusted pointer dereference

## [ClamXAV privilege escalation](#clamxav) {#clamxav}

*Public advisory: September 2026; CVE published October 2026*

A local attacker could gain system privileges through ClamXAV’s helper. I reported the race condition; ClamXAV 3.11.1 fixed it and credited the finding.

### Advisory

- [ClamXAV 3.11.1 security update and researcher credit](https://www.clamxav.com/version-history/)

### CVE

- [CVE-2026-105773](https://www.cve.org/CVERecord?id=CVE-2026-105773)

## [Windows default-browser protection](#windows-ucpd) {#windows-ucpd}

*Latest publication: August 2026*

Windows’ default-browser protection grew into a much broader policy engine. I traced the rules that decide which processes may change protected settings and compared 24 versions to show how that protection evolved.

### Publications

- [*Inside Windows' Default Browser Protection*](https://binary.ninja/2025/03/25/default-browser-upcd.html)
- [*The Binary Hiding in Your Registry: Cracking Windows UCPD's Dynamic Rules*](https://binary.ninja/2026/08/04/ucpd-dynamic-rules.html)
- [*How Windows UCPD Grew from a 29 KB Registry Filter into a 196 KB Policy Engine*](/posts/reversing/ucpd_evolution/main/)

### Research materials

- [UCPD analysis databases and tooling](https://github.com/xusheng6/ucpd_analysis)

## [Invisible IDs in Paint and Photos images](#paint-photos-watermarks) {#paint-photos-watermarks}

*Latest publication: August 2026*

Paint and Photos embed invisible, server-issued IDs in AI images generated locally. I traced how the apps receive an ID during prompt moderation and place it in the image, separately from Paint’s optional visible Copilot logo and C2PA metadata.

### Publication

- [*Microsoft Paint and Photos Embed Server-Issued GUIDs as Invisible Watermarks in Locally-Generated Images*](/posts/reversing/mspaint_invisible_watermark/main/)

### Selected coverage

- [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/microsoft-paint-and-photos-apps-add-invisible-watermark-to-ai-generated-content-developer-reverse-engineers-guid-embedding)
- [Cybernews](https://cybernews.com/privacy/microsoft-ai-images-hidden-tracking-id/)
- [Hacker News discussion](https://news.ycombinator.com/item?id=49421158)

## [What Windows WHESVC really does](#whesvc) {#whesvc}

*Publication: August 2026*

The Windows service called “spyware” turned out to be a powerful local diagnostics engine. I unpacked its scripts and traced the health reports it writes.

### Publication and materials

- [*Windows' Performance Optimizer Is More Capable Than It Needs to Be*](/posts/reversing/whesvc/main/)
- [Analysis repository](https://github.com/xusheng6/whesvc-analysis)

### Selected coverage

- [Neowin](https://www.neowin.net/news/reverse-engineer-explains-if-microsofts-windows-11-performance-service-is-really-spyware/)
- [Clubic](https://www.clubic.com/actualite-626866-accuse-d-espionner-les-pc-ce-service-de-windows-11-cache-en-realite-un-moteur-de-diagnostic.html)
- [9to5Windows](https://9to5windows.com/windows-11-performance-service-spyware-reverse-engineer-explained/)
