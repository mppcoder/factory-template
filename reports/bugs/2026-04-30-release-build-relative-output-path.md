# Defect capture: RELEASE_BUILD relative output path

Дата: `2026-04-30`.

## Симптом

Команда:

```bash
bash RELEASE_BUILD.sh _incoming/factory-v2.5.2.zip
```

проходила staging audit, но падала на этапе `zip`:

```text
zip I/O error: No such file or directory
zip error: Could not create output file (_incoming/factory-v2.5.2.zip)
```

## Причина

`RELEASE_BUILD.sh` вычислял absolute `OUT_DIR`, но оставлял `OUT_ZIP` в исходном относительном виде. После перехода в `.release-stage` команда `zip` пыталась писать relative path внутри staging directory.

## Классификация слоя

- task class: release
- layer: factory-producer-owned release packaging
- affected artifact: `RELEASE_BUILD.sh`

## Remediation

`OUT_ZIP` нормализован в absolute path после вычисления `OUT_DIR` и `OUT_BASE`.

## Evidence

Повторная проверка должна включать:

```bash
bash RELEASE_BUILD.sh _incoming/factory-v2.5.2.zip
sha256sum -c _incoming/factory-v2.5.2.zip.sha256
python3 template-repo/scripts/validate-release-package.py _incoming/factory-v2.5.2.zip --checksum _incoming/factory-v2.5.2.zip.sha256 --manifest _incoming/factory-v2.5.2.manifest.yaml
```
