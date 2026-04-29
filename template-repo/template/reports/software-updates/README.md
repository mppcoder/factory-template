# Отчеты по обновлениям ПО

Эта папка хранит report-only материалы по controlled software update governance.

Разрешено:

- baseline inventory reports;
- update intelligence summaries;
- impact classification;
- upgrade proposal drafts;
- post-upgrade verification reports после approved upgrade.

Запрещено:

- secrets, tokens, `.env` content и private transcripts;
- auto-upgrade commands без explicit approval пользователя;
- claims про background monitoring, если в repo нет реального scheduled workflow;
- silent migration на новую Ubuntu LTS.

Source artifacts:

- `.chatgpt/software-inventory.yaml`
- `.chatgpt/software-update-watchlist.yaml`
- `.chatgpt/software-update-readiness.yaml`
