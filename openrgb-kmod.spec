%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

Name:     openrgb-kmod
Version:  {{{ git_dir_version }}}
Release:  1%{?dist}
Summary:  Kernel module with i2c-nct6775 and patched i2c-piix4 for use with OpenRGB
License:  GPLv2
URL:      https://github.com/KyleGospo/openrgb-dkms

Source:  %{url}/archive/refs/heads/main.tar.gz
Source1:  https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/i2c/busses/i2c-piix4.c

Patch0:   OpenRGB-kmod.patch

BuildRequires: kmodtool

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Kernel module with i2c-nct6775 and patched i2c-piix4 for use with OpenRGB. The i2c-piix4 driver supports the secondary i2c controller on several >= X370 AM4 mainboards.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c openrgb-dkms-main
cp %{SOURCE1} openrgb-dkms-main/i2c-piix4.c
%patch 0

find . -type f -name '*.c' -exec sed -i "s/#VERSION#/%{version}/" {} \+

for kernel_version  in %{?kernel_versions} ; do
  cp -a openrgb-dkms-main _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/i2c-piix4.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/i2c-piix4.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/i2c-nct6775.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/i2c-nct6775.ko
done
%{?akmod_install}

%changelog
{{{ git_dir_changelog }}}