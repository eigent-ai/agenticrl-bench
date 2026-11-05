.PHONY: audit clean

audit: build
	python3 tools/audit_roles.py --config tools/roles_config.yaml --output build/audit_report.json templates/

build:
	mkdir -p build

clean:
	rm -rf build
