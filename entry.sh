#!/bin/bash

set -xe
export DBUS_SESSION_BUS_ADDRESS=/dev/null
# sudo service dbus restart
VNC_STORE_PWD_FILE=/io/.vnc/passwd
if [ ! -e "${VNC_STORE_PWD_FILE}" -o -n "${VNC_PASSWORD}" ]; then
    # mkdir -vp ~/.vnc

    # the default VNC password is 'hola'
    x11vnc -storepasswd ${VNC_PASSWORD:-hola} ${VNC_STORE_PWD_FILE}
fi

# default CHROME is the stable version
export CHROME=${CHROME:-/opt/google/chrome/google-chrome}

export PYTHONIOENCODING=utf_8
# retain running as pid 1
# if [ -z "${HEADLESS+x}" ];then
CONFIG=/etc/supervisord.conf 
# fi

if [ -f /io/shadowsocks.json ]; then
   echo -e "[program:ss]\npriority=0\ncommand=sslocal -c /io/shadowsocks.json\n" >> ${CONFIG}
fi
# if [ ! -z "${VNC}" ];then
#     echo -e "[program:x11vnc]\nenvironment=XAUTHLOCALHOSTNAME=localhost\ncommand=x11vnc -noxdamage -rfbport 5900 -display :10.0 -rfbauth /io/.vnc/passwd -forever -shared" >> ${CONFIG}   
# fi

exec supervisord -c ${CONFIG}
