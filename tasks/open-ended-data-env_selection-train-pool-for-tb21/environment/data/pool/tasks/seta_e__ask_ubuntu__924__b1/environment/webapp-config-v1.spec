Name:           webapp-config-v1
Version:        2.0.0
Release:        1
Summary:        Modern webapp configuration package
License:        MIT
BuildArch:      noarch

%description
Provides routing rules for the webapp.

%install
mkdir -p %{buildroot}/etc/webapp
echo "# Modern routing rules v2.0" > %{buildroot}/etc/webapp/routing.rules
echo "route / -> backend-v2" >> %{buildroot}/etc/webapp/routing.rules
echo "route /api -> api-server-v2" >> %{buildroot}/etc/webapp/routing.rules

%files
/etc/webapp/routing.rules
