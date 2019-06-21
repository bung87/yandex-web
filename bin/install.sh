#! /usr/env bash
OS="`uname`"
case $OS in
  'Linux')
    OS='Linux'
    alias ls='ls --color=auto'
    ;;
  'FreeBSD')
    OS='FreeBSD'
    alias ls='ls -G'
    ;;
  'WindowsNT')
    OS='Windows'
    ;;
  'Darwin')
    OS='Mac'
    ;;
  'SunOS')
    OS='Solaris'
    ;;
  'AIX') ;;
  *) ;;
esac



if [ $OS == "Linux" ]; then

    FILE_NAME="chromedriver_linux64.zip"

elif [ $OS == "Mac" ]; then

    FILE_NAME="chromedriver_mac64.zip"
fi

OUT="chromedriver.zip"
VERSION = $(wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE -q -O -)
wget https://chromedriver.storage.googleapis.com/$VERSION/$FILE_NAME -O $OUT
unzip $OUT -d ./bin/

echo "export PATH=$PATH:$(pwd)/bin" >> ~/.bash_profile

