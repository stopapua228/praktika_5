
import argparse, sys, os, re
from urllib.parse import urlparse

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="depviz-stage1",
        description="Вариант №30 — Этап 1: CLI параметры и валидация"
    )
    p.add_argument("-p", "--package", required=True, help="Имя анализируемого пакета")
    p.add_argument("-r", "--repo", required=True, help="URL репозитория или путь к файлу тестового репозитория")
    p.add_argument("-t", "--test", action="store_true", help="Режим работы с тестовым репозиторием (файл вместо URL)")
    p.add_argument("-o", "--output", required=True, help="Имя сгенерированного PNG файла")
    return p

def is_url(s: str) -> bool:
    try:
        u = urlparse(s)
        return u.scheme in ("http", "https") and bool(u.netloc)
    except Exception:
        return False

def validate_args(args) -> list[str]:
    errors = []

    # package: non-empty, some minimal sanity check
    if not args.package or not str(args.package).strip():
        errors.append("Параметр --package обязателен и не может быть пустым.")

    # repo: depends on test flag
    if args.test:
        if not os.path.isfile(args.repo):
            errors.append(f"--repo должен указывать на существующий файл (тестовый режим): {args.repo}")
    else:
        if not is_url(args.repo):
            errors.append(f"--repo должен быть валидным URL (http/https), получено: {args.repo}")

    # output: must end with .png; create parent dir if needed
    if not args.output.lower().endswith(".png"):
        errors.append("--output должен оканчиваться на .png")

    parent = os.path.dirname(os.path.abspath(args.output)) or "."
    try:
        os.makedirs(parent, exist_ok=True)
        # check write permission by attempting to create and delete a temp file
        test_path = os.path.join(parent, ".depviz_write_test.tmp")
        with open(test_path, "wb") as tmp:
            tmp.write(b"ok")
        os.remove(test_path)
    except Exception as e:
        errors.append(f"Нет прав на запись в каталог для --output: {parent} ({e})")

    return errors

def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    errors = validate_args(args)
    if errors:
        for e in errors:
            print(f"Ошибка: {e}", file=sys.stderr)
        return 2

    # Этап 1: печать *всех* параметров в формате ключ=значение
    ordered = [
        ("package", args.package),
        ("repo", args.repo),
        ("test_mode", str(bool(args.test))),
        ("output_png", args.output),
    ]
    for k, v in ordered:
        print(f"{k}={v}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
