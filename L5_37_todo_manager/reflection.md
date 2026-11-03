# Reflection: Static Code Analysis

The supplied handout mentions reflection questions but does not list their wording. These four responses address its stated learning outcomes and can be adapted if separate questions are provided.

## 1. What issues did the analysis tools identify?

Pylint identified the shared mutable default argument, inconsistent search returns, missing encoding, naming violations, and missing documentation. Flake8 identified four whitespace violations. Bandit identified shell execution using an email address, unsafe pickle loading, the pickle import, and standard random selection. The baseline Pylint score was 5.09/10.

## 2. Which fixes were most important, and why?

The shell command injection and unsafe deserialization were the highest priorities because they could allow unintended code execution. The email helper now uses SMTP directly and persistence uses JSON. Changing the labels default to None and copying supplied lists prevents state from leaking between tasks or back into the caller's list. Labels are now saved with each task. Old pickle data is deliberately not deserialized.

## 3. How did the tools complement each other, and how were fixes verified?

Pylint focused on quality and maintainability, Flake8 on formatting, and Bandit on security patterns. Their reports needed interpretation: using random for task suggestions was not a cryptographic vulnerability in this program, although switching to secrets removed the reported finding. All three tools were rerun after the changes: Pylint reached 10.00/10, Bandit reported no findings, and Flake8 reported no violations. The demo still completes a task, orders pending tasks, searches titles, and restores four saved tasks. Separate behavior checks cover labels, priority validation, IDs, JSON round trips, import side effects, and email construction without sending mail.

## 4. What did this exercise show about static analysis and its limitations?

Static analysis provides fast, repeatable feedback and helps prioritize fixes, but a clean report does not prove that software is correct or secure. Manual review also found import-time execution, possible ID reuse after deletion, and missing priority validation. Behavioral checks are needed alongside linting. The SMTP helper was checked with a mock; actual delivery still depends on a configured SMTP relay and was not tested. Future work could validate the complete schema of externally supplied JSON and add application-specific error handling.
