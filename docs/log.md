# Update log

Newest first. One entry per merged change. Date headings use `YYYY-MM-DD`.

## 2026-10-25

* **Change**: Extended `factory.py audit` to the full drift report and
  added the metrics document (#9).
* **Change**: Added the risk gate, stack detection in `check`, CI, and
  issue templates (#8).
* **Creation**: Added a decision record: the owner's merge is the human
  approval for high-risk diffs (#8).
* **Creation**: Added `.factory/factory.py` with `check` and `docs`, the
  OKF bundle, and the instruction router (#3).
* **Change**: Normalised line endings and added `.gitattributes` (#2).

## 2026-10-26

* **Change**: Fixed the friction the dry run found — path-based reserved
  docs, CI risk-gate and secret-scan fixes, setup-project setup steps,
  and TEMPLATE.md expectations (#9).
* **Change**: Removed the update log from the protected paths: the
  logging rule no longer closes the agent lane (#19).
* **Creation**: Recorded the research on the mattpocock
  software-factory-skill branch with per-feature recommendations (#19).
* **Change**: Aligned the factory vocabulary with the upstream
  software-factory skill: glossary terms for the three brakes, the
  ticket tracker, the ticket source, and the ratchet (#19).
* **Creation**: Recorded the research on running the factory under a
  protected main branch, with a ruleset profile (#25).
* **Creation**: Recorded the research on GitHub Copilot as a reviewer
  in the factory loop, including the gate defect it exposes (#20).
* **Creation**: Recorded the research on packaging the template as a skill or plugin with a setup wizard (#21).
