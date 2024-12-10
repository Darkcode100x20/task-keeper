# GitHub Actions Workflow Documentation

## Overview
The CI workflow automates testing for the Flask Todo application on every push and pull request to the main branch.

## Workflow Configuration
File: `.github/workflows/ci.yml`

### Trigger Events
```yaml
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
```
## Jobs and Steps

### Test Job
Environment: Ubuntu Latest
Steps:
- *Checkout repository*
  - Uses: actions/checkout@v3
  - Purpose: Clones repository code
- *Python Setup*
  - Uses: actions/setup-python@v4
  - Version: Python 3.10
  - Purpose: Configures Python environment
- *Dependencies Installation*
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-cov
```
- *Test Execution*
  - Runs: pytest
  - Execute all test cases
  - Generates coverage report

## Usage

### Automated Triggers
- Push to main branch
- Pull request to main branch

### Manual Trigger
```bash 
gh workflow run "CI for Flask App"
 ```
### Viewing results
1) navigate to repository's Action tab
2) Select "CI for Flask App" workflow
3) Click specific workflow run
4) View job details and test results