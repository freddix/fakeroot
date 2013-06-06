Summary:	Fake root environment
Name:		fakeroot
Version:	1.19
Release:	1
License:	GPL v3+
Group:		Development/Tools
Source0:	ftp://ftp.debian.org/debian/pool/main/f/fakeroot/%{name}_%{version}.orig.tar.bz2
# Source0-md5:	3a00a1264cb31a815552050ef0c2468b
URL:		http://fakeroot.alioth.debian.org/
BuildRequires:	acl-devel
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	libtool >= 2:2.2
Requires:	util-linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_prefix}/%{_lib}/libfakeroot

%description
fakeroot runs a command in an environment were it appears to have root
privileges for file manipulation. This is useful for allowing users to
create archives (tar, ar, .deb etc.) with files in them with root
permissions/ownership. Without fakeroot one would have to have root
privileges to create the constituent files of the archives with the
correct permissions and ownership, and then pack them up, or one would
have to construct the archives directly, without using the archiver.

fakeroot works by replacing the file manipulation library functions
(chmod(), stat() etc.) by ones that simulate the effect the real
library functions would have had, had the user really been root. These
wrapper functions are in a shared library libfakeroot.so*, which is
loaded through the LD_PRELOAD mechanism of the dynamic loader.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libfakeroot.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS DEBUG README
%attr(755,root,root) %{_bindir}/faked
%attr(755,root,root) %{_bindir}/fakeroot
%dir %{_libdir}
%attr(755,root,root) %{_libdir}/libfakeroot*.so
%{_mandir}/man1/faked.1*
%{_mandir}/man1/fakeroot.1*
%lang(de) %{_mandir}/de/man1/*
%lang(es) %{_mandir}/es/man1/*
%lang(fr) %{_mandir}/fr/man1/*
%lang(nl) %{_mandir}/nl/man1/*
%lang(sv) %{_mandir}/sv/man1/*

