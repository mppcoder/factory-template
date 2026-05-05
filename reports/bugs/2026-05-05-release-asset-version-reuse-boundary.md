# Release asset version reuse boundary

Дата: 2026-05-05

## Симптом

После advanced automation hardening был безопасно пересобран локальный fallback archive `factory-v2.5.8.zip` для текущего repo state, но GitHub Release `v2.5.8` уже опубликован.

## Evidence / подтверждения

- current HEAD after package evidence refresh: `cc1e1e6a95d463640abe024ebf90f1d3355bf52e`;
- rebuilt archive manifest source commit: `5ecf7f1a35749452d79adc6e3f087abb5c3c200a`;
- existing GitHub Release `v2.5.8` target commitish: `fa61d8e62db4e1690fa732c5119d01df2454e966`;
- existing release URL: `https://github.com/mppcoder/factory-template/releases/tag/v2.5.8`;
- existing release assets: `factory-v2.5.8.zip`, `factory-v2.5.8.manifest.yaml`, `factory-v2.5.8.zip.sha256`.

## Classification / классификация

- layer: release publication / package evidence boundary;
- severity: medium;
- status: captured and contained;
- reusable factory issue: yes, release executor already contains the important guard: existing tag must point to current HEAD before publication proceeds.

## Решение в текущем scope

Do not upload the rebuilt local `2.5.8` archive over the already published GitHub Release. That would create tag/package truth drift.

Current local artifact remains internal fallback evidence only. Any public release publication that includes post-`fa61d8e` changes needs a new patch version or an explicit release replacement decision with audited tag/asset policy.

## Follow-up boundary

No live GitHub Release mutation was performed.
