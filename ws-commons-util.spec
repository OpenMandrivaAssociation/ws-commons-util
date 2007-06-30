%define gcj_support 1

Name:           ws-commons-util
Version:        1.0.1
Release:        %mkrel 1.1
Epoch:          0
Summary:        Common utilities from the Apache Web Services Project 

Group:          Development/Java
License:        Apache License
URL:            http://apache.osuosl.org/ws/commons/util/
Source0:        http://apache.osuosl.org/ws/commons/util/sources/ws-commons-util-1.0.1-src.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  jpackage-utils >= 0:1.5

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel >= 0:1.0.31
Requires(post):   java-gcj-compat >= 0:1.0.31
Requires(postun): java-gcj-compat >= 0:1.0.31
%endif

%description 
This is version 1.0.1 of the common utilities from the Apache Web
Services Project.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation

%description    javadoc
%{summary}.

%prep
%setup -q

%build

cd src/main/java
find ./ -name \*.java | xargs %{javac}
find ./ -name \*.class| xargs %{jar} cvf %{name}-%{version}.jar
mkdir html
find ./ -name \*.java | xargs %{javadoc} -d html

%install
rm -rf $RPM_BUILD_ROOT

cd src/main/java
install -dm 755 $RPM_BUILD_ROOT%{_javadir}
install -pm 644 %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pR html/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(644,root,root,755)
%doc LICENSE.txt
%{_javadir}/*.jar
%if %{gcj_support}
%{_libdir}/gcj/*
%endif

%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
