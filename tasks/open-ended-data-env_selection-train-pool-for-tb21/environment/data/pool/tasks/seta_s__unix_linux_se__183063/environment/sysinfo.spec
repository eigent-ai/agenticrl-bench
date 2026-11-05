Name:           sysinfo
Version:        1.0
Release:        1%{?dist}
Summary:        System information display utility
License:        MIT
BuildArch:      noarch

%description
A simple utility that displays system information including hostname and uptime.

%install
mkdir -p %{buildroot}/usr/local/bin
cat > %{buildroot}/usr/local/bin/sysinfo << 'SCRIPTEOF'
#!/bin/bash
echo "System: $(hostname)"
echo "Uptime: $(uptime)"
SCRIPTEOF
chmod 755 %{buildroot}/usr/local/bin/sysinfo

%files
/usr/local/bin/sysinfo

%changelog
* Mon Jan 01 2024 Admin <admin@example.com> - 1.0-1
- Initial release
