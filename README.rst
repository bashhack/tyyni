# Tyyni
---

# Dev Workflow

## Testing

A TDD flow is encouraged, and to faciliate this `pytest` is used alongside the following plugins: `pytest-watch`, `pytest-testmon`, `pytest-cov` and `pytest-sugar`.

If using Honcho to orchestrate processes, simply run: `honcho start -f Procfile.dev` or execute `ptw --runner "pytest --testmon"` directly from the command-line.

