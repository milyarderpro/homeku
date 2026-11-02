# Homeku v1.2 — GitHub Actions Sequential Save

## Tested basis

The branch test at run 41448098825 succeeded with the real dreamsHouse002.mp4 and committed four shot JPEGs plus one storyboard on actions-jpg-test. This v1.2 production workflow builds on the same FFmpeg/Pillow approach. It replaces the previous unsuccessful ChatGPT Python → Git Data API Base64 JPEG path.

## Requirements

- Users place source MP4s in main/video/<filename>.mp4 **before** asking ChatGPT to analyze them. main/video files stay permanently unless the owner explicitly deletes them.
- ChatGPT can read the source video's Git blob SHA using GitHub connector Git tree. Ideally verify local uploaded MP4 bytes match the same Git blob SHA.
- User's standalone exact message save now is mandatory for ChatGPT to write requests/save.json. Before that, repo is read-only.
- GitHub Actions repository setting must permit workflows to write repository contents; workflow declares permissions.contents:write. Workflow is triggered by a push to requests/save.json.
- GitHub connector writes only UTF-8 request text (update_file); no binary blob/Base64 bridge.

## Request format (one reusable file)

requests/save.json starts as {"schema_version":"1.0","status":"idle"}.
An approved request is:

    {
      "schema_version": "1.0",
      "status": "approved",
      "request_id": "dreamsHouse002-20261102-001",
      "video": {
        "path": "video/dreamsHouse002.mp4",
        "blob_sha": "<actual 40-hex git blob sha>"
      },
      "keyframe_times_s": [3.1, 9.2, 13.7, 18.1],
      "analysis_yaml": "<complete YAML schema 2.1 with id PENDING, NOT an abbreviated placeholder>"
    }

Do not use made-up timestamps, blob SHA, or sample truncated YAML in real requests. Request IDs must be stable and unique, at least 8 characters. Separate analyses are saved sequentially. Wait for the prior status to be confirmed before replacing this file.

## GitHub Actions execution

1. On push of requests/save.json, checkout branch, ensure FFmpeg and PyYAML/Pillow, pull latest branch.
2. scripts/save_analysis_action.py validates all fields, video path and exact Git blob SHA, YAML, shot sequence and frame times.
3. Reject already-saved request IDs by scanning analysis.md request markers.
4. Allocate next available VID-XXX and generate each shot JPEG directly from checked-out video. Render storyboard.jpg and analysis.md from YAML. Validate package with scripts/validate_analysis.py.
5. Atomically commit only references/VID-XXX/ and requests/result.json (never MP4 or the original request) to the same branch, without force.
6. Fetch the remote branch and verify commit reachability and package validation.
7. For failures, workflow reports failure in Actions logs. requests/result.json is only updated on success, and can contain a previous request; compare request_id before believing status.

GitHub-generated commits made with GITHUB_TOKEN do not retrigger the push workflow. Source MP4 upload does not trigger save; only requests/save.json updates do.

## Sequential rules and safety

- No worker queue, parallel reservations, lock service or Git Data API Base64 JPEG transport.
- No accidental duplicate: immutable request_id marker in each analysis.md, and detected repeats become already_saved.
- No overwrite: next VID allocated only when saving and folder must not exist.
- No partial video package commit: extraction/validation occur before git add/commit.
- If push rejected due to branch update, job fails (no force); inspect status, then retry with the **same request_id** after resolving the branch state.
- Request identity must be matched to a real source in main/video/. A local uploaded video with the same name is not enough if SHA differs.
- During an end-to-end proof run on branch actions-jpg-test, all generated reference files stay in that branch; no production reference is touched.

## How ChatGPT should report results

After update_file success: "Processing" with request_id. Inspect GitHub Actions workflow run for the request commit, and requests/result.json. "Saved" only when the latest run succeeded and result.request_id matches and references files are verified. "Not saved" on failure.

## Quick manual test

1. Upload a known MP4 to video/ on main or actions-jpg-test (for test only). No additional branch for normal use.
2. Read the file's Git blob SHA from GitHub's tree API.
3. Build a complete approved request JSON, including full YAML and one timestamp per shot.
4. Change requests/save.json via GitHub connector update_file. The push should trigger .github/workflows/save-analysis.yml.
5. Confirm status=success, result.json matches request_id, and references/VID-XXX/ contains exactly 2 text files + one JPG per shot + one storyboard. Also verify the commit/branch.

## Cleanup from v1.1

Removed:
- scripts/prepare_git_payload.py
- scripts/save_analysis.py
- scripts/verify_analysis.py (unused local-only SHA check)
- tests/test_git_payload.py
- tests/test_parallel_save.py
- docs/github-connector-save.md
- tests/fixtures/github-blob-smoke.jpg
- scripts/action_jpg_smoke.py and the temporary .github/workflows/test-jpg-extraction.yml, after v1.2 smoke validation

Retained:
- templates YAML 2.1 / Markdown
- rules/analysis.md
- scripts/validate_analysis.py / tests/test_validation.py

No rule or test assumes that ChatGPT can transfer raw MP4 or JPG bytes to the connector.
