import sys
import os
import subprocess
import time
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_root = Path(r"D:\api\makkal-agent-ai")
test_files = sorted([f for f in repo_root.glob("test_*.py") if f.is_file()])

print("=" * 80)
print(f"🔬 RUNNING ALL AVAILABLE AUTOMATED TESTS IN MAKKAL AGENT AI ({len(test_files)} SUITES)")
print("=" * 80)

results = []

for idx, test_file in enumerate(test_files, 1):
    test_name = test_file.name
    print(f"\n[{idx:02d}/{len(test_files):02d}] Executing {test_name}...")
    start_t = time.time()
    
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    try:
        proc = subprocess.run(
            [sys.executable, "-X", "utf8", str(test_file)],
            cwd=str(repo_root),
            env=env,
            capture_output=True,
            text=True,
            timeout=90,
            encoding="utf-8",
            errors="replace"
        )
        duration = round(time.time() - start_t, 2)
        
        if proc.returncode == 0:
            print(f"  ✅ PASSED ({duration}s)")
            results.append((test_name, "PASSED", duration, ""))
        else:
            print(f"  ❌ FAILED (Exit Code {proc.returncode}) ({duration}s)")
            # Extract last few error lines
            err_output = (proc.stderr or proc.stdout)[-400:]
            results.append((test_name, f"FAILED (Code {proc.returncode})", duration, err_output))
    except subprocess.TimeoutExpired:
        duration = round(time.time() - start_t, 2)
        print(f"  ⏱️ TIMEOUT (>40s)")
        results.append((test_name, "TIMEOUT", duration, "Execution exceeded 40 seconds"))
    except Exception as e:
        duration = round(time.time() - start_t, 2)
        print(f"  ❌ ERROR: {e}")
        results.append((test_name, "ERROR", duration, str(e)))

print("\n" + "=" * 80)
print("📊 TEST EXECUTION SUMMARY REPORT")
print("=" * 80)

passed = [r for r in results if r[1] == "PASSED"]
failed = [r for r in results if r[1] != "PASSED"]

for name, status, dur, err in results:
    icon = "✅" if status == "PASSED" else "❌"
    print(f"{icon} {name:<45} | {status:<15} | {dur}s")

print("-" * 80)
print(f"Total Tests: {len(results)} | Passed: {len(passed)} | Failed/Timeout: {len(failed)}")
print("=" * 80)

if failed:
    print("\n--- Failure Details ---")
    for name, status, dur, err in failed:
        print(f"\n[FAILED] {name} ({status}):")
        print(err.strip())
