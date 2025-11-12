
import subprocess, sys, os, pathlib

BASE = pathlib.Path(__file__).resolve().parents[1]
PY = sys.executable

def run(cmd, outfile):
    p = subprocess.run([PY, "-m", "src.main"] + cmd, cwd=BASE, capture_output=True, text=True)
    with open(BASE / "examples" / outfile, "w", encoding="utf-8") as f:
        if p.stdout:
            f.write(p.stdout)
        if p.stderr:
            f.write("\nSTDERR:\n")
            f.write(p.stderr)

# OK: test mode
run(["-p","A","-r","test_data/repo1.txt","-t","-o","out/graph.png"], "stage1_demo_ok.txt")

# OK: url mode
run(["-p","junit:junit","-r","https://repo1.maven.org/maven2","-o","out/graph.png"], "stage1_demo_ok_url.txt")

# Errors
cases = [
    (["-r","test_data/repo1.txt","-t","-o","out/graph.png"], "без --package"),
    (["-p","","-r","test_data/repo1.txt","-t","-o","out/graph.png"], "пустой --package"),
    (["-p","A","-r","not_a_url","-o","out/graph.png"], "repo не url (test_mode=False)"),
    (["-p","A","-r","test_data/not_exists.txt","-t","-o","out/graph.png"], "repo файла нет (test_mode=True)"),
    (["-p","A","-r","test_data/repo1.txt","-t","-o","out/graph.jpg"], "output не .png"),
]

lines = []
for cmd, title in cases:
    p = subprocess.run([PY, "-m", "src.main"] + cmd, cwd=BASE, capture_output=True, text=True)
    lines.append(f"=== Случай: {title}\nКоманда: python -m src.main {' '.join(cmd)}")
    if p.stdout:
        lines.append("--- STDOUT ---\n"+p.stdout.strip())
    if p.stderr:
        lines.append("--- STDERR ---\n"+p.stderr.strip())
    lines.append("")

with open(BASE / "examples" / "stage1_demo_errors.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
