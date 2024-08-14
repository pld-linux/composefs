#
# Conditional build:
%bcond_without	man		# man page (requires go-md2man)
%bcond_without	static_libs	# static libraries
#
# can use ABI-compatible tool, e.g. x86_64 on x32 build host
%ifnarch %{go_arches} x32
%undefine	with_man
%endif
Summary:	Tools to handle creating and mounting composefs images
Summary(pl.UTF-8):	Narzędzia do obsługi tworzenia i montowania obrazów composefs
Name:		composefs
Version:	1.0.4
Release:	1
License:	LGPL v2.1+, parts GPL v2 or Apache v2.0 (library), GPL v3+ (tools)
Group:		Libraries
#Source0Download: https://github.com/containers/composefs/releases
Source0:	https://github.com/containers/composefs/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	91814fcb4b66ce07ced300fc323e3217
URL:		https://github.com/containers/composefs
%if %{with man}
BuildRequires:	go-md2man
%endif
BuildRequires:	libfuse3-devel >= 3.10.0
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libfuse3 >= 3.10.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The composefs project combines several underlying Linux features to
provide a very flexible mechanism to support read-only mountable
filesystem trees, stacking on top of an underlying "lower" Linux
filesystem.

%description -l pl.UTF-8
Projekt composefs łączy kilka funkcji systemu Linux, aby dostarczyć
bardzo elastyczny mechanizm obsługujący drzewa systemów plików
montowalne tylko do odczytu, budowane w oparciu o "niższe" linuksowe
systemy plików.

%package libs
Summary:	Shared library for generating and using composefs images
Summary(pl.UTF-8):	Biblioteka współdzielona do generowania i wykorzystywania obrazów composefs
License:	LGPL v2.1+, parts GPL v2 or Apache v2.0
Group:		Libraries

%description libs
Shared library for generating and using composefs images.

%description libs -l pl.UTF-8
Biblioteka współdzielona do generowania i wykorzystywania obrazów
composefs.

%package devel
Summary:	Header files for composefs library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki composefs
License:	LGPL v2.1+, parts GPL v2 or Apache v2.0
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	openssl-devel

%description devel
Header files for composefs library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki composefs.

%package static
Summary:	Static composefs library
Summary(pl.UTF-8):	Statyczna biblioteka composefs
License:	LGPL v2.1+, parts GPL v2 or Apache v2.0
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static composefs library.

%description static -l pl.UTF-8
Statyczna biblioteka composefs.

%prep
%setup -q

%build
%configure \
	%{!?with_man:--disable-man} \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcomposefs.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/composefs-info
%attr(755,root,root) %{_bindir}/mkcomposefs
%attr(755,root,root) %{_sbindir}/mount.composefs
%if %{with man}
%{_mandir}/man1/composefs-info.1*
%{_mandir}/man1/mkcomposefs.1*
%{_mandir}/man1/mount.composefs.1*
%{_mandir}/man5/composefs-dump.5*
%endif

%files libs
%defattr(644,root,root,755)
%doc BSD-2-Clause.txt README.md
%attr(755,root,root) %{_libdir}/libcomposefs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcomposefs.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcomposefs.so
%{_includedir}/libcomposefs
%{_pkgconfigdir}/composefs.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcomposefs.a
%endif
