.PHONY := help

help:
	@echo ""
	@echo " Usage: make <target>"
	@echo ""
	@echo " Targets:"
	@echo "    run          run feedify (requires setup)"
	@echo "    setup        prepare environment to run feedify"
	@echo "    setup_dev    prepare environment to develop feedify"
	@echo "    test         run test (requires setup_dev)"
	@echo ""


run:
	@source venv/bin/activate && python -m feedify

setup:
	python3 -m virtualenv venv
	@source venv/bin/activate && python -m pip install -r requirements.txt
	cp config.json.example config.json

	@echo "Done."
	@echo ""
	@echo "Edit config.json to configure feedify."

setup_dev:
	@source venv/bin/activate && python -m pip install -r requirements-dev.txt

test:
	pytest tests
