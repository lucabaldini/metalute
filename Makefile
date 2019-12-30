test:
	pytest-3

pylint:
	pylint metalute

pyflakes:
	pyflakes metalute

mypy:
	mypy metalute

clean:
	rm -f metalute/*.pyc
	rm -rf */__pycache__

doc:
	cd docs; make html; cd -

cleandoc:
	rm -rf docs/_build
