
import subprocess, sys, os, pathlib

# Получаю абсолютный путь к корню проекта (папка на уровень выше /scripts)
BASE = pathlib.Path(__file__).resolve().parents[1]
# Определяю текущий интерпретатор Python (тот, с которым запущен скрипт)
PY = sys.executable


def run(cmd, outfile):
    # Запускаю src.main как модуль, передавая ему список аргументов cmd.
    # cwd=BASE — чтобы запуск был из корня проекта.
    # capture_output=True — чтобы перехватить stdout/stderr для записи в файл.
    p = subprocess.run([PY, "-m", "src.main"] + cmd, cwd=BASE, capture_output=True, text=True)

    # Записываю всё, что вывелось, в файл examples/outfile
    with open(BASE / "examples" / outfile, "w", encoding="utf-8") as f:
        # stdout — основной вывод программы (обычно нормальные результаты)
        if p.stdout:
            f.write(p.stdout)
        # stderr — сюда попадут ошибки, пишу их ниже с пометкой
        if p.stderr:
            f.write("\nSTDERR:\n")
            f.write(p.stderr)


# ==== корректные случаи ====
# Тестовый режим (используется локальный файл repo1.txt)
run(["-p","A","-r","test_data/repo1.txt","-t","-o","out/graph.png"], "stage1_demo_ok.txt")

# URL-режим (используется настоящий репозиторий Maven Central)
run(["-p","junit:junit","-r","https://repo1.maven.org/maven2","-o","out/graph.png"], "stage1_demo_ok_url.txt")


# ==== случаи с ошибками ====
# Список пар (аргументы, короткое описание)
cases = [
    (["-r","test_data/repo1.txt","-t","-o","out/graph.png"], "без --package"),  # нет обязательного параметра
    (["-p","","-r","test_data/repo1.txt","-t","-o","out/graph.png"], "пустой --package"),  # пустое имя пакета
    (["-p","A","-r","not_a_url","-o","out/graph.png"], "repo не url (test_mode=False)"),  # невалидный URL без --test
    (["-p","A","-r","test_data/not_exists.txt","-t","-o","out/graph.png"], "repo файла нет (test_mode=True)"),  # файл отсутствует
    (["-p","A","-r","test_data/repo1.txt","-t","-o","out/graph.jpg"], "output не .png"),  # неправильное расширение
]

lines = []
for cmd, title in cases:
    # Для каждой ошибки выполняю ту же команду и собираю её выводы
    p = subprocess.run([PY, "-m", "src.main"] + cmd, cwd=BASE, capture_output=True, text=True)
    lines.append(f"=== Случай: {title}\nКоманда: python -m src.main {' '.join(cmd)}")
    # STDOUT (если что-то было выведено)
    if p.stdout:
        lines.append("--- STDOUT ---\n" + p.stdout.strip())
    # STDERR (сообщения об ошибках)
    if p.stderr:
        lines.append("--- STDERR ---\n" + p.stderr.strip())
    lines.append("")  # пустая строка между блоками


# Сохраняю все собранные результаты ошибок в один файл для демонстрации
with open(BASE / "examples" / "stage1_demo_errors.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
