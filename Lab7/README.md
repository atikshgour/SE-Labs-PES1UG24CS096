# Lab 7: Irrigation scheduler fuzz testing

The assigned Lab 7 starter application is reproduced in `original_processor.py`.
`processor.py` contains the corrected version; `test_processor.py` contains
Hypothesis tests for all three functions plus explicit invalid-input cases.

Run from this directory:

```powershell
python -m pip install hypothesis pytest
python processor.py
python -m pytest test_processor.py -q
```

Input contract: zone areas must be positive finite numbers; moisture readings
must be integers from 0 to 100; water inputs must be nonnegative finite numbers.
Malformed input raises `ValueError`.

## PDF screenshot checklist

Use four terminal screenshots in this order, with the command and output visible:

1. **Original run:** `python original_processor.py`, entering `north:120`,
   `40,35,50`, and `120|8`. This is the assigned original code, before fixes.
2. **Failing fuzz tests:** Run
   `python -m pytest test_original_processor.py -q --tb=short`. This replay
   uses the same tests against the original code without changing the final
   files. `evidence/before_fuzz_tests.txt` records the observed failures.
3. **Corrected run:** `python processor.py` with the same three inputs.
4. **Final tests:** `python -m pytest test_processor.py -q`, showing all tests pass.

Add the final `processor.py` and `test_processor.py` source to the PDF as code
pages or readable screenshots. The four terminal screenshots are execution
evidence; source code pages are separate from them.
