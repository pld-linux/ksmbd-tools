#
# Conditional build:
%bcond_with	kerberos5	# Kerberos 5 support

Summary:	cifsd kernel server userspace utilities
Summary(pl.UTF-8):	Narzędzia przestrzeni użytkownika do serwera cifsd w jądrze
Name:		ksmbd-tools
Version:	3.5.2
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	https://github.com/cifsd-team/ksmbd-tools/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	62e6a4e93c2958295ec993c77ee3bbb6
URL:		https://github.com/cifsd-team/ksmbd-tools
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.44
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	libnl-devel >= 1:3.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.671
Requires:	glib2 >= 1:2.44
Requires:	systemd-units >= 38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cifsd kernel server userspace utilities.

%description -l pl.UTF-8
Narzędzia przestrzeni użytkownika do serwera cifsd w jądrze.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable kerberos5 krb5} \
	--disable-silent-rules \
	--with-systemdsystemunitdir="%{systemdunitdir}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/ksmbd,%{systemdunitdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/ksmbd/ksmbd.conf.example

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
%doc AUTHORS README.md ksmbd.conf.example
%dir %attr(700,root,root) %{_sysconfdir}/ksmbd
%attr(755,root,root) %{_sbindir}/ksmbd.addshare
%attr(755,root,root) %{_sbindir}/ksmbd.adduser
%attr(755,root,root) %{_sbindir}/ksmbd.control
%attr(755,root,root) %{_sbindir}/ksmbd.mountd
%attr(755,root,root) %{_libexecdir}/ksmbd.tools
%{systemdunitdir}/ksmbd.service
%{_mandir}/man5/ksmbd.conf.5*
%{_mandir}/man5/ksmbdpwd.db.5*
%{_mandir}/man8/ksmbd.addshare.8*
%{_mandir}/man8/ksmbd.adduser.8*
%{_mandir}/man8/ksmbd.control.8*
%{_mandir}/man8/ksmbd.mountd.8*
