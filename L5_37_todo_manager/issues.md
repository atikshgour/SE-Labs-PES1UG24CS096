# Static analysis issues

Line numbers refer to the original `todo_manager.py`, preserved in the before reports. Severity for non-Bandit items is a review assessment. All listed issues have been fixed.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (B605) | Security - High | 57 | The email address is concatenated into an `os.system` command and can introduce shell commands. | Use `EmailMessage` and `smtplib` with no shell. The helper now requires an SMTP relay, defaulting to localhost:25. |
| Unsafe deserialization (B301) | Security - Medium | 47 | Loading an untrusted pickle can execute code. | Replace pickle persistence with JSON and convert JSON keys back to integer task IDs on load. Old pickle files are not loaded. |
| Mutable default argument (W0102) | Bug - Medium | 11-13 | The default labels list is shared across calls; the function also mutates caller-supplied lists and discards the labels. | Default to `None`, copy supplied labels, and store an independent list on each task. |
| Pickle import (B403) | Security - Low | 3 | Bandit flags importing a module associated with unsafe serialization. | Remove the import after adopting JSON. |
| Random selection (B311) | Security tool finding - Low | 70 | Bandit flags the standard random generator. Task suggestions do not require cryptographic randomness, so this is low practical risk here. | Use `secrets.choice` to satisfy the lab's zero-finding target; handle an empty pending list. |
| Inconsistent returns (R1710) | Maintainability - Low | 33-36 | Search returns an ID explicitly but falls through implicitly when there is no match. | Return `None` explicitly for an unsuccessful search. |
| Missing encoding (W1514) | Portability - Low | 51 | JSON output depends on the platform's default encoding. | Specify UTF-8 for all JSON reads and writes. |
| Naming conventions (C0103) | Style - Low | 11-55 | Camel-case function names and variables violate Python naming conventions. | Rename functions and local variables to snake_case and the shared task mapping to `TASKS`. |
| Missing documentation (C0114, C0116) | Maintainability - Low | 1, 11-60 | The module and public functions lack docstrings. | Add concise module and function docstrings. |
| Whitespace (E225, E303, E261, E231) | Style - Low | 12, 40, 69, 74 | Missing operator/comma/comment spacing and excess blank lines. | Apply consistent PEP 8 spacing and blank lines. |
| Import side effects | Manual review - Medium | 80 | Importing the module executes the demo and writes files. | Add a `__main__` guard. |
| Invalid priority and ID reuse | Manual review - Medium | 12, 14, 29 | Invalid priorities fail later during sorting; length-based IDs can overwrite tasks after deletion. | Validate priority before insertion and allocate IDs above the current maximum. |

## Verification and reports

- Before: `pylint_before.txt` (5.09/10), `bandit_before.txt` (1 high, 1 medium, 2 low), `flake8_before.txt` (4 violations).
- After: `pylint_report.txt` (10.00/10), `bandit_report.txt` (no findings), `flake8_report.txt` (empty means no violations).
- Demonstrations: `demo_before.txt` and `demo_after.txt`. Random suggestions and timestamps can differ; task ordering, completion, search results, and restored task count are preserved.
- Additional behavior checks are recorded in `verification_report.txt`.

The default persistence file is now `tasks.json`; the old `tasks.pkl` is a legacy artifact and is never read by the cleaned program. Function names now use snake_case. No lint rules or Bandit checks were suppressed.
