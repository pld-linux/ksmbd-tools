#
# Conditional build:
%bcond_with	kerberos5	# Kerberos 5 support

Summary:	cifsd kernel server userspace utilities
Name:		ksmbd-tools
Version:	3.4.3
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	https://github.com/cifsd-team/ksmbd-tools/releases/download/%{version}/%{name}-%{version}.tgz
# Source0-md5:	e034197104549fa84b4702eca78034aa
URL:		https://github.com/cifsd-team/ksmbd-tools
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake
BuildRequires:	glib2-devel
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	libnl-devel >= 3.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.671
Requires:	systemd-units >= 38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cifsd kernel server userspace utilities.

%prep
%setup -q -n %{name}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable kerberos5 krb5} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/ksmbd,%{systemdunitdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

sed -e 's#/sbin/ksmbd#%{_sbindir}/ksmbd#g' ksmbd.service > $RPM_BUILD_ROOT%{systemdunitdir}/ksmbd.service

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post ksmbd.service

%preun
%systemd_preun ksmbd.service

%postun
%systemd_reload

%triggerpostun -- ksmbd-tools < 3.4.3
%systemd_trigger ksmbd.service

%files
%defattr(644,root,root,755)
%doc AUTHORS README smb.conf.example
%dir %attr(700,root,root) %{_sysconfdir}/ksmbd
%attr(755,root,root) %{_sbindir}/ksmbd.addshare
%attr(755,root,root) %{_sbindir}/ksmbd.adduser
%attr(755,root,root) %{_sbindir}/ksmbd.control
%attr(755,root,root) %{_sbindir}/ksmbd.mountd
%{systemdunitdir}/ksmbd.service
