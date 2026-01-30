test:
	@TEST_DATABASE_URL='postgresql://postgres:postgres@localhost:5432/mydb' python -m pytest project/tests --junitxml=test-results/results.xml