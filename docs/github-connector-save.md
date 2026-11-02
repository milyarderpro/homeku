# Homeku — ChatGPT + Python + GitHub Connector Save (v1.1)

## Scope

This implementation keeps video analysis schema 2.1 and the `save now` approval gate unchanged. The repository provides deterministic Python validators/payload helpers and a mock-tested Safe Parallel Save engine. **It does not provide a ChatGPT-to-Python-to-connector binary transport.** GitHub connector tools are callable inside ChatGPT, but cannot open the local `/mnt/data` files, and running a Python script from a GitHub repository is not automatic. Therefore an end-to-end automatic video save is **not enabled** until that transport passes a real-size byte-for-byte test.

## Local preparation (no GitHub writes)

```bash
python -m pip install -r scripts/requirements.txt
python scripts/validate_analysis.py /mnt/data/homeku_draft_dreamsHouse002/references/PENDING
python scripts/prepare_git_payload.py /mnt/data/homeku_draft_dreamsHouse002/references/PENDING --id VID-002 --output /tmp/homeku-private-payload.json
python -m unittest discover -s tests -v
```

`VID-002` above is an **illustrative candidate**, not reserved. Always recalculate from the latest repository HEAD at authorized save time. The generated payload contains all image Base64 data; treat it as sensitive working data, do not commit it, put it in chat prose, or log it. Payload files are for local transport experiments, not a fallback save mechanism.

## GitHub connector operations (ONLY after authorized standalone `save now`)

1. Revalidate the reviewed draft, including original JPEG bytes and `storyboard.jpg`; stop if any file is missing or if binary transport cannot be verified.
2. Use `GitHub.fetch` on `git/ref/heads/main` and `git/commits/{sha}` plus `git/trees/{tree}?recursive=1` for one consistent HEAD snapshot. Select the lowest unused `VID-XXX` from `references/VID-XXX/...` at that snapshot. Never reserve IDs at analyze time.
3. Rebuild YAML/Markdown for that candidate ID and validate; `analysis.yaml` remains the data source. Preserve JPEG bytes exactly.
4. For each file, call `GitHub.create_blob` with text as `utf-8` and images as `base64`. **Compare the returned Git blob SHA with locally calculated `sha1_git_blob` before proceeding.** If the tool or context cannot transport the complete Base64 text losslessly, stop before creating a tree/commit.
5. `GitHub.create_tree` with one element per file: `path`, `mode:100644`, `type:blob`, and verified `sha`, with `base_tree_sha` from the selected HEAD.
6. `GitHub.create_commit` with `parent_sha` equal to that same HEAD and `tree_sha` returned in step 5.
7. `GitHub.update_ref` on `main` with `force:false` and `expected_sha` set to the selected HEAD (the connector exposes this lease field). If rejected because HEAD changed, restart at step 2 and choose ID again, maximum 3 attempts. Never force-push.
8. If the update outcome is ambiguous (timeout/unknown), **read GitHub branch and commit first**. Do not blindly retry as a different ID. Verify commit ancestry, YAML, Markdown, file paths and image content/hash. State `Saved` only after full verification.
9. If conflict persists, binary bytes unavailable, or verification incomplete: report `Not saved`; keep the draft if available. If ref was updated but verification fails, investigate and do not create an additional ID.

### Safety and permissions

- Only exact standalone `save now` authorizes creating VIDEO content blobs/tree/commit. Editing repository rules/scripts is independent and does not count as video save authorization.
- A message containing a quoted/example `save now` is not approval.
- No per-file `create_file` commits, no force push, no overwrite of existing `references/VID-XXX/` folders.
- A confirmed saved draft reuses its existing ID and commit reference; repeated `save now` must not duplicate it.
- Each chat's draft is independent; files in one chat are not automatically available to other chats.

## Test status and limitation

- The included validators, manifest builder, JPEG SHA-256/Git blob SHA checks and mock collision/retry tests run locally.
- A small synthetic 1x1 JPEG was successfully transferred via manually relayed Base64 to `GitHub.create_blob`; its Git blob SHA matched the local calculation. This is **not** proof that an unmodified full-sized shot JPEG can be reliably passed automatically from Python into connector arguments.
- A larger synthetic JPEG test produced a SHA mismatch on the first manual relay; the byte forwarding path was not reliable in that attempt. No branch update or video reference was created by those blob-only experiments.
- **Do not claim fully automated Save or mark this project end-to-end complete** until a real original `shot-01.jpg` and other assets can be delivered without truncation via a supported data path, and one entire test package passes atomic commit and readback verification.

## Acceptance criteria for activating the automatic save

1. Full-size JPEG(s) cross the Python-to-connector boundary unchanged, with matching Git blob SHA and SHA-256 after readback.
2. Atomic commit of YAML, Markdown, storyboard, and every per-shot JPEG.
3. HEAD conflict simulation and live verification of no-overwrite and three-retry limit.
4. Idempotence on repeated command and uncertainty on network failure.
5. Project Instructions point ChatGPT to the latest four repo rules/templates; repo documentation alone cannot execute tools.
