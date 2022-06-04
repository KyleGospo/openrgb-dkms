%global debug_package %{nil}
%global dkms_name openrgb
%global kernel_version 5.17

Name:       %{dkms_name}-dkms
Version:    %{kernel_version}.{{{ git_dir_version }}}
Release:    1%{?dist}
Summary:    DKMS kernel module with i2c-nct6775 and patched i2c-piix4 for use with OpenRGB
License:    GPLv2
URL:        https://github.com/KyleGospo/openrgb-dkms
BuildArch:  noarch

# Source file:
# https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/drivers/i2c/busses/i2c-piix4.c
Source0:    https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/i2c/busses/i2c-piix4.c?h=v%{kernel_version}#/i2c-piix4.c
Source1:    i2c-nct6775.c
Source2:    Makefile
Source3:    dkms.conf

# OpenRGB i2c-piix4 patch:
Patch0:     OpenRGB.patch

Provides:   %{dkms_name}-dkms = %{version}
Requires:   dkms
Requires:   openrgb

%description
DKMS kernel module with i2c-nct6775 and patched i2c-piix4 for use with OpenRGB. The i2c-piix4 driver supports the secondary i2c controller on several >= X370 AM4 mainboards.

%prep
%setup -q -T -c -n %{name}-%{version}
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} .
%patch0 -p0

%build

%install
# Create empty tree
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr * %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

install -d %{buildroot}%{_sysconfdir}/modules-load.d
cat > %{buildroot}%{_sysconfdir}/modules-load.d/i2c-openrgb.conf << EOF
i2c-piix4
i2c-nct6775
i2c-dev
EOF

%post
dkms add -m %{dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry
dkms remove -m %{dkms_name} -v %{version} -q --all || :

%files
%{_usrsrc}/%{dkms_name}-%{version}
%{_sysconfdir}/modules-load.d/i2c-openrgb.conf

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
{{{ git_dir_changelog }}}