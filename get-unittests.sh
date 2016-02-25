#!/bin/sh

VERSION="$1"
TAG="$2"

if test -d ansible-temp ; then
  pushd ansible-temp
  git checkout devel
  git pull --rebase
  popd
else
  git clone https://github.com/ansible/ansible.git ansible-temp
fi

pushd ansible-temp
if test -n "$TAG" ; then
  git checkout "$TAG"
fi
popd
tar -cJvf "ansible-unittests-$VERSION.tar.xz" -C ansible-temp/ test/units
