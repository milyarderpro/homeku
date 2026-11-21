"""GitHub runner: publish a fresh branch snapshot, retrying concurrent pushes."""
from __future__ import annotations
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

def git(root, *args, check=True):
    return subprocess.run(["git", "-C", str(root), *args], check=check, text=True, capture_output=True)

def publish_actions(root, branch, runner_temp, before_push=None, attempts=5):
    report = runner_temp / "homeku-ingest-report.json"
    for attempt in range(1, attempts + 1):
        git(root, "fetch", "--no-tags", "origin", f"refs/heads/{branch}")
        with tempfile.TemporaryDirectory(prefix="homeku-publish-", dir=runner_temp) as work_name:
            work = Path(work_name) / "repo"
            git(root, "worktree", "add", "--detach", str(work), "FETCH_HEAD")
            try:
                command = subprocess.run([sys.executable, "tools/library.py", "ingest"], cwd=work, capture_output=True, text=True)
                try:
                    result = json.loads(command.stdout)
                except json.JSONDecodeError:
                    result = {"status": "failed", "error": command.stderr or command.stdout}
                result["publish_attempt"] = attempt
                report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
                verified = subprocess.run([sys.executable, "tools/library.py", "check"], cwd=work, capture_output=True, text=True)
                if verified.returncode:
                    raise RuntimeError("Full check failed; nothing pushed: " + verified.stderr)
                if command.returncode not in (0, 1) or "results" not in result:
                    raise RuntimeError("Ingest did not finish normally: " + command.stderr)
                git(work, "add", "--", "references", "catalogs", "knowledge", "data", "video")
                if git(work, "diff", "--cached", "--quiet", check=False).returncode == 0:
                    return result
                git(work, "-c", "user.name=github-actions[bot]", "-c", "user.email=41898282+github-actions[bot]@users.noreply.github.com",
                    "commit", "-m", "chore: ingest HOMEKU reference packages")
                if before_push:
                    before_push(attempt, work)
                pushed = git(work, "push", "origin", f"HEAD:refs/heads/{branch}", check=False)
                if pushed.returncode == 0:
                    return result
                git(root, "fetch", "--no-tags", "origin", f"refs/heads/{branch}")
                local_parent = git(work, "rev-parse", "HEAD^").stdout.strip()
                remote_head = git(root, "rev-parse", "FETCH_HEAD").stdout.strip()
                if local_parent == remote_head:
                    raise RuntimeError("GitHub rejected publication: " + pushed.stderr)
            finally:
                git(root, "worktree", "remove", "--force", str(work), check=False)
    raise RuntimeError("Publication lost five push races; rerun Library ingest")

def main():
    if os.environ.get("GITHUB_ACTIONS") != "true" or not os.environ.get("RUNNER_TEMP"):
        raise SystemExit("Publisher runs only inside GitHub Actions; use tools/library.py locally.")
    branch = os.environ.get("HOMEKU_BRANCH")
    if not branch or branch.startswith("-") or any(c in branch for c in "\n\r\x00"):
        raise SystemExit("Missing/invalid HOMEKU_BRANCH")
    try:
        result = publish_actions(Path(__file__).resolve().parents[2], branch, Path(os.environ["RUNNER_TEMP"]))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return int(any(r["status"] == "failed" for r in result.get("results", [])))
    except (RuntimeError, OSError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 1
