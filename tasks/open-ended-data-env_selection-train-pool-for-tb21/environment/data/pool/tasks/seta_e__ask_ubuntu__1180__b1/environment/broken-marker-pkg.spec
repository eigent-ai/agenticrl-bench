Name: broken-marker-pkg
Version: 1.0
Release: 1
Summary: Marker package with broken scriptlet
License: MIT
BuildArch: noarch

%description
A test package with a broken post-install scriptlet.

%install
mkdir -p %{buildroot}/var/lib/broken-marker
echo "broken marker" > %{buildroot}/var/lib/broken-marker/README

%files
/var/lib/broken-marker/README

%post
exit 1

%preun
exit 1
