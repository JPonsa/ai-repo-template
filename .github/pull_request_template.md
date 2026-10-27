## Summary

<!-- The problem, the approach, and the trade-offs. State the issue this
closes: "Closes #N". -->

## Evidence

<!-- Paste the evidence block produced by the `verify` skill. The commit
must equal HEAD of this pull request. Evidence from an earlier commit is
stale and is rejected. -->

```text
<!-- factory:evidence
commit: <sha>
check: uv run scripts/factory.py check
result: pass
risk: low
-->
```

<!-- Attach the observed output of the check, at minimum the last line.
Never report success without observed output. -->

## Merge Danger

<!-- What can break after this merges, and how to revert it. Name the
blast radius: files, callers, and dependent tickets. -->
