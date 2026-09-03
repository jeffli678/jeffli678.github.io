---
layout: post
status: publish
title: How Zoom Detects Google Meet Without Microphone Access
date: '2026-09-02'
description: Reverse engineering Zoom Workplace reveals how it uses macOS Control Center logs and the Windows microphone consent store to identify microphone-using apps.
images:
- /posts/reversing/zoom_my_notes_detector/social-preview-v3.jpg
categories:
- Reversing
---

## TL;DR

- Zoom can notice that Google Meet, Teams, Slack, and other applications may be in a meeting and offer to start My Notes
- On macOS, Zoom monitors Control Center's `sensor-indicators` log stream
- The messages contain records such as `[mic] Google Chrome (com.google.Chrome)`
- Zoom extracts an application identity and detects when microphone use starts or stops
- On Windows, it obtains equivalent application-usage information from the per-user Capability Access Manager microphone records in the registry
- Reading this metadata requires neither administrator/root privileges nor Zoom microphone permission

## Why does Zoom know that Chrome is using the microphone?

Zoom's My Notes feature can take notes during meetings hosted in applications
such as Google Meet, Microsoft Teams, and Slack. Before the user starts it, Zoom
can display a **Take Note** prompt when it thinks a third-party meeting is in
progress.

That raised an interesting question: how does Zoom recognize the other
application before it has started taking notes?

The answer differs by platform. On macOS, Zoom parses human-readable Unified
Logging output. On Windows, it enumerates microphone-usage records in the
registry.

## The macOS detector

I statically analyzed the arm64 build of Zoom Workplace 7.1.5 (84650).

The implementation is in a class named `PrivacyEventMonitor` inside
`viper.framework`. Its relevant methods are:

```text
-[PrivacyEventMonitor startMonitoring]
-[PrivacyEventMonitor handleLogOutput:]
-[PrivacyEventMonitor parseSystemLogLine:]
-[PrivacyEventMonitor parseAttributionsStringForMicrophone:]
-[PrivacyEventMonitor notifyMacAppStateChange:previousStates:]
```

`startMonitoring` launches `/usr/bin/log`:

```sh
/usr/bin/log stream \
  --type log \
  --level default \
  --predicate 'subsystem == "com.apple.controlcenter" AND category == "sensor-indicators"' \
  --style compact
```

macOS Control Center maintains the orange and green privacy indicators for
microphone and camera use. The same subsystem writes the currently responsible
applications to Unified Logging. A microphone record for Chrome looks like:

```text
Sorted active attributions from SystemStatus update: [mic] Google Chrome (com.google.Chrome)
```

macOS has already supplied the display name and bundle ID. Zoom keeps entries
marked `[mic]`, parses those two fields, and compares each new attribution list
with the previous one. An application appearing or disappearing becomes a
microphone-start or microphone-stop event; no audio analysis is involved.

## From Chrome to Google Meet

The UI layer contains a product category named `chrome`, labels it **Google
Meet**, and applies notification and per-application blacklist settings. The
overall flow is:

```text
Chrome opens the microphone
  -> macOS updates Control Center's sensor attribution
  -> Control Center emits a sensor-indicators log record
  -> Zoom extracts “Google Chrome” and “com.google.Chrome”
  -> Zoom detects an application-state transition
  -> product mapping and notification policy
  -> optional “Take Note” prompt
```

This is more accurately called **microphone-use detection** than meeting
detection. Chrome could be accessing the microphone for a reason unrelated to
Google Meet. Zoom's higher layers decide whether the signal should produce a
prompt.

## The Windows detector

I also statically analyzed Zoom Workplace for Windows x64 7.1.8.46825. Its
detector is in `viper_async_device.dll` and reads this per-user registry key:

```text
HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\
CapabilityAccessManager\ConsentStore\microphone
```

Zoom opens the key with `KEY_READ`, enumerates packaged application entries and
the `NonPackaged` subtree used by classic desktop applications, and queries
each entry's 64-bit `LastUsedTimeStop` value. A zero value represents an access
interval that has not ended, so Zoom treats that application as currently using
the microphone.

The Windows flow is therefore:

```text
Chrome opens the microphone
  -> Windows updates ConsentStore\microphone\NonPackaged
  -> LastUsedTimeStop remains zero while access is active
  -> Zoom enumerates the registry records
  -> Zoom identifies Chrome's executable
  -> product mapping and notification policy
  -> optional “Take Note” prompt
```

This part uses ordinary registry APIs. I found no ETW consumer, audio-session
observer, or PCM processing in the application-attribution routine. Static
analysis does not establish its polling interval, the feature flags controlling
it, or whether detection metadata is included in telemetry.

## Does this require permission?

I tested Zoom's exact `/usr/bin/log stream` predicate as an ordinary user,
without `sudo`, and macOS accepted it. Reading the records did not require
Microphone, Screen Recording, System Audio Recording, or Accessibility
permission.

On Windows, the key is under `HKEY_CURRENT_USER` and Zoom requests only
`KEY_READ`, so it likewise requires neither elevation nor microphone access.

Neither mechanism should be treated as a stable application API. Zoom depends
on undocumented macOS log formatting and Windows registry implementation
details that either operating-system vendor could change.

It is a clever use of privacy bookkeeping that both operating systems already
expose—and a reminder that privacy indicators can themselves become a source of
cross-application activity information.
