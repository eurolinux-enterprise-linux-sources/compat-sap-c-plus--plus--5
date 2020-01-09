# SAP HACK: Start custom scl information for SAP build.
%global scl 1
%global scl_prefix compat-sap-
%global _root_prefix /opt/rh/SAP
%global _root_infodir %{_root_prefix}/%{_infodir}
%global _root_mandir %{_root_prefix}/%{_mandir}
# END SAP HACK.
%{?scl:%global __strip strip}
%{?scl:%global __objdump objdump}
%global DATE 20160406
%global SVNREV 234777
%global gcc_version 5.3.1
# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%global gcc_release 6
%global mpc_version 0.8.1
%global _unpackaged_files_terminate_build 0
%global multilib_64_archs sparc64 ppc64 s390x x86_64
%ifarch x86_64
%global multilib_32_arch i686
%endif
Summary: SAP HANA based on GCC 5
Name: %{?scl_prefix}c++-5
ExclusiveArch: x86_64

Version: %{gcc_version}
Release: %{gcc_release}%{?dist}
# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group: Development/Languages
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-5-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
Source1: http://www.multiprecision.org/mpc/download/mpc-%{mpc_version}.tar.gz
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
BuildRequires: binutils >= 2.19.51.0.14-33
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, texinfo, sharutils
#BuildRequires: systemtap-sdt-devel >= 1.3
# For VTA guality testing
BuildRequires: gdb
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
Requires: binutils >= 2.19.51.0.14-33
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
Requires: libgcc >= 4.1.2-43
Requires: libgomp >= 4.4.4-13
BuildRequires: gmp-devel >= 4.1.2-8
BuildRequires: mpfr-devel >= 2.2.1
%if 0%{?rhel} >= 7
BuildRequires: libmpc-devel >= 0.8.1
%endif
AutoReq: true
AutoProv: false
%global oformat %{nil}
%global oformat2 %{nil}
%ifarch %{ix86}
%global oformat OUTPUT_FORMAT(elf32-i386)
%endif
%ifarch x86_64
%global oformat OUTPUT_FORMAT(elf64-x86-64)
%global oformat2 OUTPUT_FORMAT(elf32-i386)
%endif
Requires: libstdc++ >= 4.4.4-13

Patch0: gcc5-hack.patch
Patch1: gcc5-java-nomulti.patch
Patch2: gcc5-ppc32-retaddr.patch
Patch3: gcc5-rh330771.patch
Patch4: gcc5-i386-libgomp.patch
Patch5: gcc5-sparc-config-detection.patch
Patch6: gcc5-libgomp-omp_h-multilib.patch
Patch7: gcc5-libtool-no-rpath.patch
Patch8: gcc5-isl-dl.patch
Patch10: gcc5-libstdc++-docs.patch
Patch11: gcc5-no-add-needed.patch
Patch12: gcc5-libgo-p224.patch
Patch13: gcc5-aarch64-async-unw-tables.patch
Patch14: gcc5-libsanitize-aarch64-va42.patch
Patch15: gcc5-rh1279639.patch

Patch1000: gcc5-libstdc++-compat.patch
Patch1001: gcc5-libgfortran-compat.patch
Patch1002: gcc5-alt-compat-test.patch
Patch1003: gcc5-libquadmath-compat.patch
Patch1004: gcc5-libstdc++44-xfail.patch
Patch1005: gcc5-rh1118870.patch
Patch1006: gcc5-isl-dl2.patch

%global gcc_target_platform %{_target_platform}

%description
This carries runtime compatibility libraries needed for SAP HANA.

%prep
%setup -q -n gcc-%{version}-%{DATE} -a 1
%patch0 -p0 -b .hack~
%patch1 -p0 -b .java-nomulti~
%patch2 -p0 -b .ppc32-retaddr~
%patch3 -p0 -b .rh330771~
%patch4 -p0 -b .i386-libgomp~
%patch5 -p0 -b .sparc-config-detection~
%patch6 -p0 -b .libgomp-omp_h-multilib~
%patch7 -p0 -b .libtool-no-rpath~
%patch11 -p0 -b .no-add-needed~
%patch12 -p0 -b .libgo-p224~
rm -f libgo/go/crypto/elliptic/p224{,_test}.go
%patch13 -p0 -b .aarch64-async-unw-tables~
%patch14 -p0 -b .libsanitize-aarch64-va42~
%patch15 -p0 -b .rh1279639~
sed -i -e 's/ -Wl,-z,nodlopen//g' gcc/ada/gcc-interface/Makefile.in

%patch1000 -p0 -b .libstdc++-compat~
%patch1001 -p0 -b .libgfortran-compat~
%ifarch %{ix86} x86_64
%if 0%{?rhel} < 7
# On i?86/x86_64 there are some incompatibilities in _Decimal* as well as
# aggregates containing larger vector passing.
%patch1002 -p0 -b .alt-compat-test~
%endif
%endif
%if 0%{?rhel} < 7
%patch1003 -p0 -b .libquadmath-compat~
%endif
%if 0%{?rhel} == 6
# Fix this up
#%patch1004 -p0 -b .libstdc++44-xfail~
%endif
%patch1005 -p0 -b .rh1118870~

echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

%if 0%{?rhel} == 6
# Default to -gdwarf-3 rather than -gdwarf-4
sed -i '/UInteger Var(dwarf_version)/s/Init(4)/Init(3)/' gcc/common.opt
sed -i 's/\(may be either 2, 3 or 4; the default version is \)4\./\13./' gcc/doc/invoke.texi
%endif

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h
cp -a libstdc++-v3/config/cpu/i{4,3}86/opt

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

sed -i -e 's/Common Driver Var(flag_report_bug)/& Init(1)/' gcc/common.opt

%build

# Undo the broken autoconf change in recent Fedora versions
export CONFIG_SITE=NONE

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

%if 0%{?rhel} < 7
mkdir mpc mpc-install
cd mpc
../../mpc-%{mpc_version}/configure --disable-shared \
  CFLAGS="${CFLAGS:-%optflags} -fPIC" CXXFLAGS="${CXXFLAGS:-%optflags} -fPIC" \
  --prefix=`cd ..; pwd`/mpc-install
make %{?_smp_mflags}
make install
cd ..
%endif

%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}

CC=gcc
CXX=g++
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mfpmath=sse/-mfpmath=sse -msse2/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
CONFIGURE_OPTS="\
	--prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla \
	--enable-shared --enable-threads=posix --enable-checking=release \
	--enable-multilib \
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object \
	--enable-linker-build-id \
	--enable-plugin --with-linker-hash-style=gnu \
	--enable-initfini-array \
	--disable-libgcj \
	--with-default-libstdcxx-abi=gcc4-compatible \
	--disable-libquadmath \
	--disable-libsanitizer \
	--disable-libvtv \
	--disable-libgomp \
	--disable-libitm \
	--disable-libssp \
	--disable-libatomic \
	--disable-libcilkrts \
	--disable-libmpx \
%if 0%{?rhel} < 7
        --with-mpc=`pwd`/mpc-install \
%endif
	--without-isl \
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%ifarch %{ix86}
	--with-arch=i686 \
%endif
%ifarch x86_64
	--with-arch_32=i686 \
%endif
	--build=%{gcc_target_platform} \
	"

CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	GCJFLAGS="$OPT_FLAGS" \
	../configure --enable-bootstrap \
	--enable-languages=c,c++,lto \
	$CONFIGURE_OPTS


GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS"

%install
rm -fr %{buildroot}

%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}
cd obj-%{gcc_target_platform}

TARGET_PLATFORM=%{gcc_target_platform}
cp %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so.6.0.* %{buildroot}%{_root_prefix}/%{_lib}/compat-sap-c++-%{gcc_version}.so

%check
cd obj-%{gcc_target_platform}

%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}

# run the tests.
make %{?_smp_mflags} -k check RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
( LC_ALL=C ../contrib/test_summary -t || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}' > testresults
rm -rf gcc/testsuite.prev
mv gcc/testsuite{,.prev}
rm -f gcc/site.exp
make %{?_smp_mflags} -C gcc -k check-gcc check-g++ ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}' compat.exp struct-layout-1.exp" || :
mv gcc/testsuite/gcc/gcc.sum{,.sent}
mv gcc/testsuite/g++/g++.sum{,.sent}
( LC_ALL=C ../contrib/test_summary -o -t || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}' > testresults2
rm -rf gcc/testsuite.compat
mv gcc/testsuite{,.compat}
mv gcc/testsuite{.prev,}
echo ====================TESTING=========================
cat testresults
echo ===`gcc --version | head -1` compatibility tests====
cat testresults2
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
for i in `find gcc/testsuite.compat -name \*.log | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/`basename $i`.compat || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_root_prefix}
%dir %{_root_prefix}/%{_lib}
%{_root_prefix}/%{_lib}/compat-sap-c++-%{gcc_version}.so

%changelog
* Thu May 12 2016 Marek Polacek <polacek@redhat.com> 5.3.1-6
- update from DTS gcc-5.3.1-6

* Thu Mar 17 2016 Marek Polacek <polacek@redhat.com> 5.3.1-1
- rebase to 5.3
- rename the DSO and the package to allow using more versions of the library

* Fri Jul 31 2015 Marek Polacek <polacek@redhat.com> 5.2.1-1
- rebase to 5.2

* Thu Jul 30 2015 Marek Polacek <polacek@redhat.com> 4.9.2-1
- rebase to 4.9

* Wed May 20 2015 Marek Polacek <polacek@redhat.com> 4.8.2-16
- backport PR59224 fix again

* Wed Mar 18 2015 Marek Polacek <polacek@redhat.com> 4.8.2-15
- rebase to 4.8 (#1198501)

* Tue Apr 01 2014 Marek Polacek <polacek@redhat.com> 4.7.2-10
- backport PR59224 fix

* Tue Mar 25 2014 Marek Polacek <polacek@redhat.com> 4.7.2-9
- clarify description (#1080544)

* Wed Mar 12 2014 Marek Polacek <polacek@redhat.com> 4.7.2-8
- rename sap-compat-c++.so to compat-sap-c++.so

* Wed Mar 05 2014 Marek Polacek <polacek@redhat.com> 4.7.2-7
- run the testsuite
- fix up Provides
- update description

* Wed Mar 05 2014 Marek Polacek <polacek@redhat.com> 4.7.2-6
- build only compat-sap-c++, that only installs sap-compat-c++.so

* Tue Mar 04 2014 Jonathan Wakely <jwakely@redhat.com> 4.7.2-6
- adjust gcc47-ppl-check.patch
- remove gdb files from %files

* Mon Oct 15 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-5
- update from the 4.7 branch
  - GCC 4.7.2 release
- operator new[] overflow checking (#850911, PR c++/19351)
- selected debug info quality improvements (#851467)

* Fri Sep 14 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-8
- adjust doxygen configgen.py for older python (#856725)

* Wed Sep  5 2012 Marek Polacek <polacek@redhat.com> 4.7.1-7.3
- use --with-expatlibdir when building graphviz

* Thu Aug 23 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-7.2
- redefine __strip and __objcopy macros

* Wed Aug 22 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-7.1
- install gfortran.1 manual page and gfortran info pages (#850448)

* Mon Aug 13 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-7
- update from the 4.7 branch
- backport -mrdseed, -mprfchw and -madx support

* Fri Jul 20 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-5
- update from the 4.7 branch

* Mon Jul 16 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-3
- update from the 4.7 branch
  - C++11 ABI change - std::list and std::pair in C++11 ABI compatible again
    with C++03, but ABI incompatible with C++11 in GCC 4.7.[01]
- backport -mrtm and -mhle support

* Fri Jun 29 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-1
- update from the 4.7 branch
  - GCC 4.7.1 release
- enable build_gfortran (#819596)

* Mon May 28 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-5.2
- selected 4.7 backports (#825827)
  - fix i?86 8-bit mem += val ICE (PR target/53358)
  - alias handling fix (PR tree-optimization/53364)
  - vectorizer complex handling fix (PR tree-optimization/53366)
  - VRP bitfield fix (PRs tree-optimization/53438, tree-optimization/53505)
  - VRP NVR fix (PR tree-optimization/53465)

* Wed May  9 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-5.1
- remove html docs from %{?scl_prefix}libstdc++%{!?scl:47}-devel
  package now that they are in %{?scl_prefix}libstdc++%{!?scl:47}-docs

* Mon May  7 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-5
- update from 4.7 branch
- build libstdc++ docs with doxygen 1.8.0 instead of 1.7.1

* Fri May  4 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-4
- update from 4.7 branch
- fix up gcc-ar, gcc-nm and gcc-ranlib (#818311, PR plugins/53126)
%if 0%{?rhel} == 6
- configure for i686 rather than i586 by default
%endif
- add %{?scl_prefix}libstdc++%{!?scl:47}-docs subpackage

* Wed Apr 18 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-2
- update from 4.7 branch
%if 0%{?scl:1} && 0%{?rhel} == 5
- allow building of the package even when %{name} is already
  installed (#808628)
%endif

* Tue Mar 27 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-1.1
- update from trunk and 4.7 branch
  - GCC 25th Anniversary 4.7.0 release
%if 0%{?scl:1} && 0%{?rhel} == 5
- configure with --enable-build-id (#804963)
%endif
- enable libitm build (#800503)
- fix up libgomp.so, so that libgomp isn't linked always statically

* Mon Mar  5 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.18.1
- add a few missing copyright boilerplates to libstdc++_nonshared.a
  sources

* Wed Feb 29 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.18
- update from trunk
- apply patch0 (#797774)
- remove libquadmath.so.debug from debuginfo (#797781)
- add some further binaries (#797660)

* Sat Feb 25 2012 Jeff Law <law@redhat.com> 4.7.0-0.17
- xfail tests which are expected to fail

* Fri Feb 24 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.16
- new package
