%define modname sphinx
%define soname %{modname}.so
%define inifile A79_%{modname}.ini

Summary:	Client extension for Sphinx
Name:		php-%{modname}
Version:	1.2.0
Release:	%mkrel 2
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/sphinx/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	file
BuildRequires:	sphinxclient-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This extension provides bindings for libsphinxclient, client library for
Sphinx.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# lib64 fix
perl -p -i -e "s|/lib\b|/%{_lib}|g" *.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_libdir}/php/extensions

install -m0755 modules/%{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}

[%{modname}]
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml CREDITS
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-2mdv2012.0
+ Revision: 795500
- rebuild for php-5.4.x

* Tue Apr 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-1
+ Revision: 789001
- 1.2.0

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-9
+ Revision: 761293
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-8
+ Revision: 696469
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-7
+ Revision: 695464
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-6
+ Revision: 646684
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-5mdv2011.0
+ Revision: 629744
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-4mdv2011.0
+ Revision: 628050
- ensure it's built without automake1.7

* Tue Nov 23 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-3mdv2011.0
+ Revision: 600182
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-2mdv2011.0
+ Revision: 588721
- rebuild

* Sun Sep 19 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-1mdv2011.0
+ Revision: 579828
- 1.1.0

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.4-2mdv2010.1
+ Revision: 514654
- rebuilt for php-5.3.2

* Mon Mar 01 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.4-1mdv2010.1
+ Revision: 512914
- 1.0.4

* Wed Jan 13 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-1mdv2010.1
+ Revision: 490652
- 1.0.3

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2mdv2010.1
+ Revision: 485482
- rebuilt for php-5.3.2RC1

* Wed Dec 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1mdv2010.1
+ Revision: 475235
- 1.0.2

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-7mdv2010.1
+ Revision: 468253
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-6mdv2010.0
+ Revision: 451357
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1.0.0-5mdv2010.0
+ Revision: 397602
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-4mdv2010.0
+ Revision: 377027
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-3mdv2009.1
+ Revision: 346620
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2mdv2009.1
+ Revision: 341798
- rebuilt against php-5.2.9RC2

* Sat Jan 31 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdv2009.1
+ Revision: 335728
- 1.0.0

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-3mdv2009.1
+ Revision: 323078
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-2mdv2009.1
+ Revision: 310306
- rebuilt against php-5.2.7

* Fri Aug 01 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-1mdv2009.0
+ Revision: 259519
- 0.2.0

* Sat Jul 26 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2009.0
+ Revision: 250265
- import php-sphinx


* Sat Jul 26 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2009.0
- initial Mandriva package
