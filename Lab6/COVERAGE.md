# Lab 6 coverage

Code coverage: 92% (35/38 statements, 13 tests).
Branch coverage: 100% (28/28 branches, 18 tests).

Run from this folder after installing `pytest` and `coverage`:

```powershell
python -m coverage run --data-file=coverage_code.dat --source=irrigation_scheduler -m pytest -q test_code_coverage.py
python -m coverage report --data-file=coverage_code.dat -m
python -m coverage run --data-file=coverage_branch.dat --branch --source=irrigation_scheduler -m pytest -q test_branch_coverage.py
python -m coverage report --data-file=coverage_branch.dat -m
```

