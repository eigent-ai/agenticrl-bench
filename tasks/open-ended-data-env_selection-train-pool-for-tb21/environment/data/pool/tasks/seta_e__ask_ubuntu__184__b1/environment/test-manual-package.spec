Name:    test-manual-package
Version: 1.0.0
Release: 1%{?dist}
Summary: A test package for manual installation
License: MIT
BuildArch: noarch
Requires: wget, jq

%description
A test package that was manually built for testing RPM removal.

%install
mkdir -p %{buildroot}/usr/local/bin
cat > %{buildroot}/usr/local/bin/test-manual-tool << 'SCRIPT'
#!/bin/bash
echo 'Test manual tool'
SCRIPT
chmod +x %{buildroot}/usr/local/bin/test-manual-tool

%files
/usr/local/bin/test-manual-tool

%changelog
* Mon Jan 01 2024 Test User <test@example.com> - 1.0.0-1
- Initial package
