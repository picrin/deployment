%define MAJOR %(echo $MAJOR)
%define MINOR %(echo $MINOR)
%define PATCH %(echo $PATCH)
Name:           devEnvironment
Version:        %{MAJOR}.%{MINOR}
Release:        %{PATCH}
Summary:        Dev env for the project

License:        GPL
URL:            example.com

Requires:  golang >= 1.0.0

%description
A simple website in go

%files
