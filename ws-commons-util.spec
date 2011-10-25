%global         with_maven 1

Name:           ws-commons-util
Version:        1.0.1
Release:        18
Summary:        Common utilities from the Apache Web Services Project

Group:          System/Libraries
License:        ASL 2.0
URL:            http://apache.osuosl.org/ws/commons/util/
Source0:        http://apache.osuosl.org/ws/commons/util/sources/ws-commons-util-1.0.1-src.tar.gz
%if ! %{with_maven}
# Generated with mvn ant:ant and MANIFEST.MF added to jar task
Source1:        build.xml
Source2:        maven-build.xml
Source3:        MANIFEST.MF
%else
Patch0:         %{name}-addosgimanifest.patch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  jpackage-utils >= 1.5
%if %{with_maven}
BuildRequires:  maven2
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-source-plugin
BuildRequires:  maven-assembly-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-eclipse-plugin
BuildRequires:  maven-doxia
BuildRequires:  maven-doxia-sitetools
%else
BuildRequires:  ant
%endif
BuildRequires:  junit
BuildRequires:  java-javadoc

Requires(post): jpackage-utils
Requires(postun): jpackage-utils

%description
This is version 1.0.1 of the common utilities from the Apache Web
Services Project.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description    javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{version}
%if ! %{with_maven}
cp -p %{SOURCE1} .
cp -p %{SOURCE2} .
cp -p %{SOURCE3} .
%else
%patch0
%endif

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
%if %{with_maven}
mvn-jpp \
  -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
  install javadoc:javadoc
%else
ant -Dmaven.mode.offline=true -Dmaven.repo.local=`pwd`/.m2 \
  -Djunit.skipped=true -Dmaven.test.skip=true javadoc package
%endif

%install
install -dm 755 $RPM_BUILD_ROOT%{_javadir}
install -pm 644 target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# install maven pom file
install -Dm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

# ... and maven depmap
%add_to_maven_depmap org.apache.ws.commons %{name} %{version} JPP %{name}
# and alternative depmap used by upstream
%add_to_maven_depmap org.apache.ws.commons.util %{name} %{version} JPP %{name}

install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pR target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :


%files
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_javadir}/*.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE.txt
%doc %{_javadocdir}/%{name}

