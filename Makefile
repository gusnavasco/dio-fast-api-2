run:
	@uvicorn tdd_project.main:app --reload

precommit-install:
	@poetry run pre-commit install
