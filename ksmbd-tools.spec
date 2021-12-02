#
# Conditional build:
%bcond_with	kerberos5	# Kerberos 5 support

Summary:	cifsd kernel server userspace utilities
Name:		ksmbd-tools
Version:	3.4.2
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	https://github.com/cifsd-team/ksmbd-tools/releases/download/%{version}/%{name}-%{version}.tgz
# Source0-md5:	7c22829d3aa2cf1ee60e284fbda2af4c
URL:		https://github.com/cifsd-team/ksmbd-tools
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake
BuildRequires:	glib2-devel
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	libnl-devel >= 3.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.527
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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README smb.conf.example
%attr(755,root,root) %{_sbindir}/ksmbd.addshare
%attr(755,root,root) %{_sbindir}/ksmbd.adduser
%attr(755,root,root) %{_sbindir}/ksmbd.control
%attr(755,root,root) %{_sbindir}/ksmbd.mountd
