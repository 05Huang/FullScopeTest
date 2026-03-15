

# run_rewrite.py
import subprocess

# 用 UTF-8 打开文件，避免中文报错
with open("rewrite_history.py", "r", encoding="utf-8") as f:
    callback_code = f.read()

subprocess.run([
    "git",
    "filter-repo",
    "--force",
    "--commit-callback",
    callback_code
], check=True)