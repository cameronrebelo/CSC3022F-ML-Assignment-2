install: venv
	. venv/bin/activate; pip3 install -Ur requirements.txt
venv:
	test -d venv || python3 -m venv venv
start:
	source ./venv/bin/activate
clean:
	rm -rf venv
	find -iname "*.pyc" -delete