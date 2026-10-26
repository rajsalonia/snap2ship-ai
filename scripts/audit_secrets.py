"""Check version-controlled and unignored source without printing secret values."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
paths = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT).decode().split("\0")
patterns = [re.compile(rb"AIza[0-9A-Za-z_-]{35}"), re.compile(rb"gh[pousr]_[0-9A-Za-z]{30,}"),
            re.compile(rb"github_pat_[0-9A-Za-z_]{30,}"), re.compile(rb"sk-proj-[0-9A-Za-z_-]{25,}"),
            re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")]
failures = []
for name in sorted(set(paths)):
    if not name:
        continue
    path = ROOT / name
    if not path.is_file():
        continue
    if (path.name == ".env" or path.name.startswith(".env.")) and not path.name.endswith(".example"):
        failures.append(name + ": environment file must not be published")
    data = path.read_bytes()
    if any(pattern.search(data) for pattern in patterns):
        failures.append(name + ": possible credential found (value omitted)")
if failures:
    print("\n".join(failures))
    raise SystemExit(1)
print(f"Secret audit passed: {len(set(paths) - {''})} source/artifact files checked. No recognized credentials or private environment files found.")
