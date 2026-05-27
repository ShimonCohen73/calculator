Run the calculator test suite with coverage and give me a summary report.

Steps:
1. Activate the virtual environment by running: `source venv/Scripts/activate`
2. Run: `pytest tests/ -v --cov=src --cov-report=term-missing`
3. Report how many tests passed and failed
4. List any failing tests with the failure reason
5. List any functions in src/ that have less than 80% coverage
6. Give an overall health assessment: is this codebase in good shape?