# Интеграции

Перечислите внешние сервисы, API и обмены данными.

## Google Drive Sources Folder

Если проект использует отдельную папку Google Drive для staging/export Sources, launcher при создании проекта потребует реальный URL, а дальше он хранится через:

- `.chatgpt/google-drive-sources.yaml`
- `.env`
- переменная `GOOGLE_DRIVE_FOLDER_URL`

Шаблонный пример лежит в:

- `.chatgpt/google-drive-sources.yaml`
- `.env.example`

Приоритет рекомендуется такой:

1. `.chatgpt/google-drive-sources.yaml`
2. `.env`
3. явный CLI override `--folder-url`

Для каждого развёрнутого боевого проекта URL папки должен задаваться отдельно. Не наследуйте бездумно folder URL от `factory-template`, если проекту нужна своя dedicated папка.
