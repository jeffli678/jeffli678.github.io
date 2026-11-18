---
title: "Research"
---

My research uses reverse engineering and hands-on testing to examine security and privacy claims in devices and software. This page lists selected lines of work, newest first by the latest article, talk, or advisory in each project, with primary writing, talks, advisories, and selected coverage.

## [Windows coding-agent telemetry](#windows-coding-agent-telemetry) {#windows-coding-agent-telemetry}

*Latest publication: November 2026*

I examined `MissionControlAggregator.dll` and found checks for named coding agents and developer tools. On a tested Windows 11 ARM64 build, I observed matching process launches set bits in persisted state and a diagnostic event queued for upload when optional diagnostic data was enabled. The report contained tool-category bits rather than prompts or source code; my tests do not establish that this feature is active on every Windows installation or that Microsoft received the queued event.

### Publication

- [*Windows 11 Is Collecting Data on Which Coding Agents and Developer Tools You Use*](/posts/windows-coding-agent-telemetry/)
- [Initial research post on X](https://x.com/CrackmesOne/status/2122147747390468384)

### Selected coverage

- [GIGAZINE](https://gigazine.net/gsc_news/en/20261117-windows-coding-agent-telemetry/)
- [Dr. Web](https://www.drweb.de/windows-11-coding-agenten-diagnosedaten/)
- [Hacker News discussion](https://news.ycombinator.com/item?id=50524736)

## [UTM guest-to-renderer VM escape](#utm-vm-escape) {#utm-vm-escape}

*Fix released: November 2026*

I reported memory-corruption issues in UTM's VM rendering path. A malicious guest could use them to cross the guest boundary and execute code in UTM's isolated rendering process on the host. That process is sandboxed, so the release note does not claim unrestricted host execution. UTM fixed the issues in version 5.0.9 and credited my report.

### Vendor release note

- [UTM 5.0.9 release and full notes](https://github.com/utmapp/UTM/releases/tag/v5.0.9)

## [Software-update security at scale](#software-update-security) {#software-update-security}

*Study published: September 2026; public advisory: November 2026*

I examined software-update mechanisms across thousands of applications, using automated analysis and manual validation to identify update paths that could expose users to untrusted code. The study distinguishes findings by how an updater retrieves, authenticates, and executes updates, and includes responsible-disclosure outcomes. The public SnappyMail advisory credits my report of an insecure update path; other reports from the study should be read in the context of each project's disclosure status. I also reported an insecure self-update path in the closed-source EastWest Installation Center. EastWest confirmed the finding, implemented HTTPS and certificate checks, restricted redirects, and added publisher-signature verification before launching an installer. I tested a macOS build provided by EastWest and confirmed that it addressed the reported issue. Its public update notes do not yet identify a release containing this fix.

### Publications and data

- [*Detecting Insecure Software Updates at Scale with LLM Agents*](/posts/reversing/detecting_insecure_software_updates_at_scale/main/)
- [Public dataset and study site](https://xusheng6.github.io/update-security-study/)

### Public advisory and fixes

- [SnappyMail GHSA-j9c4-gf64-rph2](https://github.com/the-djmaze/snappymail/security/advisories/GHSA-j9c4-gf64-rph2)
- [Akaunting update fix (pull request #3401)](https://github.com/akaunting/akaunting/pull/3401)
- [FOG Project update fix](https://github.com/FOGProject/fogproject/commit/a92d061e0790a40a6edf6ed80fc5852b9e0cef07)
- [Cemu update fix](https://github.com/cemu-project/Cemu/commit/a1cd67ca111437db680fa3560a19a8a34d085926)
- [EastWest Installation Center updates](https://www.soundsonline.com/support/updates)

## [Bring Your Own Trusted Caller (BYOTC)](#byotc) {#byotc}

*Latest presentation: October 2026*

This research examines Windows drivers that authorize powerful operations based on the identity of a trusted user-mode client. If an attacker can control that client or its creation path, the driver's caller check may no longer protect the privileged operation. The published first installment analyzes Malwarebytes Chameleon and System Informer; the BSides Portland presentation describes additional product-specific cases, with each demonstration limited to what was verified.

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

## [Encrypted USB drives and copy protection](#encrypted-usb) {#encrypted-usb}

*Latest publication: October 2026*

I tested encrypted USB drives and USB copy-protection tools to find out whether passwords actually protect the stored files. The failures differed by product: an internal SD card held plaintext, USB commands exposed passwords, software used fixed keys or built-in recovery accounts, and one drive accepted an unlock command derived from data available before sign-in. My [dedicated research index](https://encrypted-usb.fail/) documents each product, its evidence and limitations, vendor responses, and a larger coverage archive.

**Project site:** [encrypted-usb.fail](https://encrypted-usb.fail/)

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

## [Affinity document and QuickLook parser vulnerabilities](#affinity) {#affinity}

*Public advisories: October 2026*

I audited Affinity by Canva's document parser and macOS QuickLook thumbnail and preview paths. Seven public CVE records credit me with findings involving inadequate bounds checks, incomplete UTF-8 handling, image-buffer size calculation, and untrusted pointer dereferences. Crafted Affinity documents could trigger crashes or memory-safety failures when processed by affected versions.

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

## [ClamXAV privileged-helper vulnerability](#clamxav) {#clamxav}

*Public advisory: September 2026; CVE published October 2026*

I reported a local privilege-escalation vulnerability in ClamXAV's privileged helper. A race condition and insufficient file validation could allow a local attacker to execute code with system privileges in affected versions 3.3 through 3.11. Canimaan fixed the issue in ClamXAV 3.11.1 and credited the report in its release notes.

### Advisory

- [ClamXAV 3.11.1 security update and researcher credit](https://www.clamxav.com/version-history/)

### CVE

- [CVE-2026-105773](https://www.cve.org/CVERecord?id=CVE-2026-105773)

## [Windows UCPD and default-association protection](#windows-ucpd) {#windows-ucpd}

*Latest publication: August 2026*

Windows' User Choice Protection Driver (UCPD) began by guarding default-browser registry keys, then grew into a broader kernel policy engine. I traced its rules and bypass responses, decoded a signed dynamic-policy blob carried in the registry, and compared 38 historical binaries representing 24 versions. The work shows how Microsoft expanded its protected surface and changed the conditions under which a process is trusted.

### Publications

- [*Inside Windows' Default Browser Protection*](https://binary.ninja/2025/03/25/default-browser-upcd.html)
- [*The Binary Hiding in Your Registry: Cracking Windows UCPD's Dynamic Rules*](https://binary.ninja/2026/08/04/ucpd-dynamic-rules.html)
- [*How Windows UCPD Grew from a 29 KB Registry Filter into a 196 KB Policy Engine*](/posts/reversing/ucpd_evolution/main/)

### Research materials

- [UCPD analysis databases and tooling](https://github.com/xusheng6/ucpd_analysis)

## [Invisible watermarks in Microsoft Paint and Photos](#paint-photos-watermarks) {#paint-photos-watermarks}

*Latest publication: August 2026*

I reverse engineered the AI image-generation paths in Paint and Photos and found an invisible watermark separate from Paint's optional visible Copilot logo. In the local-generation path I analyzed, a Microsoft service supplied a GUID during prompt moderation, and the application embedded that value in the generated image. I also traced the separate C2PA provenance path. The report distinguishes the code paths from behavior that could not be exercised on my test hardware.

### Publication

- [*Microsoft Paint and Photos Embed Server-Issued GUIDs as Invisible Watermarks in Locally-Generated Images*](/posts/reversing/mspaint_invisible_watermark/main/)

### Selected coverage

- [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/microsoft-paint-and-photos-apps-add-invisible-watermark-to-ai-generated-content-developer-reverse-engineers-guid-embedding)
- [Cybernews](https://cybernews.com/privacy/microsoft-ai-images-hidden-tracking-id/)
- [Hacker News discussion](https://news.ycombinator.com/item?id=49421158)

## [Windows Health and Optimized Experiences service (WHESVC)](#whesvc) {#whesvc}

*Publication: August 2026*

I reverse engineered Windows' Health and Optimized Experiences service to investigate claims that it was spyware. The service runs compiled Lua scripts with SYSTEM privileges, gathers device-health and performance information, and writes a local JSON summary. My analysis describes its native interfaces and observed behavior; it did not establish a routine upload of that summary or support the broad spyware claim.

### Publication and materials

- [*Windows' Performance Optimizer Is More Capable Than It Needs to Be*](/posts/reversing/whesvc/main/)
- [Analysis repository](https://github.com/xusheng6/whesvc-analysis)

### Selected coverage

- [Neowin](https://www.neowin.net/news/reverse-engineer-explains-if-microsofts-windows-11-performance-service-is-really-spyware/)
- [Clubic](https://www.clubic.com/actualite-626866-accuse-d-espionner-les-pc-ce-service-de-windows-11-cache-en-realite-un-moteur-de-diagnostic.html)
- [9to5Windows](https://9to5windows.com/windows-11-performance-service-spyware-reverse-engineer-explained/)
