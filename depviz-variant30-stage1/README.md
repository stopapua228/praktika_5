Вариант №30, **Этап 1**

CLI‑прототип для визуализатора графа зависимостей.
Этот репозиторий содержит первый этап: чтение параметров
из командной строки, печать всех параметров в формате `ключ=значение` и обработку ошибок.




```bash
python3 -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1
```

## Запуск (Этап 1)
Помощь:
```bash
python3 -m src.main -h
```

Корректный запуск в **тестовом режиме** (файл существует, расширение `.png`):
```bash
python3 -m src.main -p A -r test_data/repo1.txt -t -o out/graph.png
```

Корректный запуск с **URL‑репозиторием**:
```bash
python3 -m src.main -p junit:junit -r https://repo1.maven.org/maven2 -o out/graph.png
```

Ожидаемый вывод (пример):
```
package=A
repo=test_data/repo1.txt
test_mode=True
output_png=out/graph.png
```

## Демонстрация ошибок
Скрипт `scripts/run_demo.py` создаёт примеры выходов:
- `examples/stage1_demo_ok.txt` — корректный вызов (тестовый режим)
- `examples/stage1_demo_ok_url.txt` — корректный вызов (URL)
- `examples/stage1_demo_errors.txt` — набор некорректных вызовов и сообщения об ошибках

Запуск:
```bash
python3 scripts/run_demo.py
```

## Критерии соответствия (Этап 1 — Вариант №30)
- Источник параметров — **опции командной строки**.
- Параметры: `--package`, `--repo`, `--test` (флаг тестового репозитория), `--output` (PNG).
- При запуске печатаются **все параметры** в формате `ключ=значение`.
- Реализована и продемонстрирована **валидация/обработка ошибок** для всех параметров:
  - пустое имя пакета;
  - `--repo` не URL при `--test=False`;
  - отсутствующий файл при `--test=True`;
  - `--output` без расширения `.png` или в несуществующую директорию (создаётся автоматически).
