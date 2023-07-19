%if 0%{?fedora}
%global debug_package %{nil}
%endif

Name:     openrgb
Version:  {{{ git_dir_version }}}
Release:  1%{?dist}
Summary:  Kernel module with i2c-nct6775 and patched i2c-piix4 for use with OpenRGB
License:  GPLv2
URL:      https://github.com/KyleGospo/openrgb-dkms

Source:   %{url}/archive/refs/heads/main.tar.gz

Provides: %{name}-kmod-common = %{version}
Requires: %{name}-kmod >= %{version}

BuildRequires: systemd-rpm-macros

%description
Kernel module with i2c-nct6775 and patched i2c-piix4 for use with OpenRGB. The i2c-piix4 driver supports the secondary i2c controller on several >= X370 AM4 mainboards.

%prep
%setup -q -c openrgb-dkms-main

%files
%doc openrgb-dkms-main/README.md
%license openrgb-dkms-main/LICENSE

%changelog
{{{ git_dir_changelog }}}
