Name:           secpatch-app
Version:        1.0
Release:        1%{?dist}
Summary:        Security monitoring application
License:        MIT
BuildArch:      noarch

%description
A security monitoring application used in production.

%install
mkdir -p %{buildroot}/opt/secpatch-app
echo "secpatch-app version 1.0" > %{buildroot}/opt/secpatch-app/version.txt

%files
/opt/secpatch-app/version.txt
