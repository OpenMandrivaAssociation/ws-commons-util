Name:           ws-commons-util
Version:        1.0.1
Release:        %mkrel 6.1.2
Summary:        Common utilities from the Apache Web Services Project 

Group:          Development/Java
License:        Apache Software License
URL:            http://apache.osuosl.org/ws/commons/util/
Source0:        http://apache.osuosl.org/ws/commons/util/sources/ws-commons-util-1.0.1-src.tar.gz
Patch0:         %{name}-addosgimanifest.patch

# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=239123
ExcludeArch:    ppc64

BuildRequires:  java-rpmbuild >= 1.5
BuildRequires:  maven2
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-source
BuildRequires:  maven2-plugin-assembly
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-surefire
BuildRequires:  maven2-plugin-eclipse
BuildRequires:  junit
BuildRequires:  java-javadoc

BuildRequires:    java-gcj-compat-devel >= 1.0.31

%description 
This is version 1.0.1 of the common utilities from the Apache Web
Services Project.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
%{summary}.

%prep
%setup -q
%patch0

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
mvn-jpp \
  -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
  install javadoc:javadoc

%install
rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_javadir}
install -pm 644 target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pR target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

aot-compile-rpm

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_gcjdb}

%postun
%{clean_gcjdb}

%files
%defattr(644,root,root,755)
%doc LICENSE.txt
%{_javadir}/*.jar
%{_libdir}/gcj/*

%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
