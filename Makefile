test:
	pytest-3

pylint:
	pylint metalute

pyflakes:
	pyflakes metalute

mypy:
	mypy metalute

doc:
	cd docs; make html; cd -

cleandoc:
	rm -rf docs/_build
