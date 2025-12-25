from __future__ import annotations
import shutil, subprocess, sys

def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None

def run(cmd):
    print(">", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    print("🔍 Validation Suite")
    if have("python"):
        run([sys.executable, "-m", "compileall", "."])
    if have("ruff"):
        run(["ruff", "check", "."])
    else:
        print("ℹ️ ruff not installed; skipping lint")
    if have("pytest"):
        run(["pytest", "-q"])
    else:
        print("ℹ️ pytest not installed; skipping tests")
    if have("bandit"):
        run(["bandit", "-q", "-r", "."])
    else:
        print("ℹ️ bandit not installed; skipping security lint")
    if have("pip-audit"):
        run(["pip-audit"])
    else:
        print("ℹ️ pip-audit not installed; skipping dependency audit")
    print("✅ Validation complete.")

if __name__ == "__main__":
    main()
