
FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null
RUN set -xe \
    && apt-get update -y --allow-releaseinfo-change\
    && apt-get install -y --no-install-recommends ca-certificates wget apt-utils \
    && apt-get install -y --no-install-recommends xvfb x11vnc fluxbox\
    && apt-get install -y --no-install-recommends sudo \
    && apt-get install -y --no-install-recommends supervisor shadowsocks gnupg

# RUN ln -s /bin/dbus-daemon /usr/bin/dbus-daemon     # /etc/init.d/dbus has the wrong location
# RUN ln -s /bin/dbus-uuidgen /usr/bin/dbus-uuidgen   # /etc/init.d/dbus has the wrong location

ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn

RUN set -xe \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -  \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

ENV OUT=/tmp/chromedriver.zip

# COPY ./chromedriver_linux64.zip /tmp/chromedriver.zip
RUN set -xe \
 && apt-get update \
&&  apt-get install -y --no-install-recommends zip unzip \
# && wget https://chromedriver.storage.googleapis.com/2.40/chromedriver_linux64.zip -O $OUT \
&& mkdir -p /io/bin/ \
&& export VERSION=$(wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE -q -O -)  && wget https://chromedriver.storage.googleapis.com/$VERSION/chromedriver_linux64.zip -O $OUT \
&& unzip $OUT -d /io/bin/ \
&& rm $OUT \
&& chmod 755 /io/bin/chromedriver
# && echo "export PATH=$PATH:/chromedriver/bin" >> ~/.bash_profile


COPY ./requirements.txt /

RUN apt -qqy update \
  && apt -qqy --no-install-recommends install \
    python3 \
    python3-pip \
    python3-dev \
    python3-openssl \
    libssl-dev libffi-dev \
  && pip3 install --no-cache --upgrade pip==9.0.3 \
  && pip3 install --no-cache setuptools \
#   && pip3 install --no-cache numpy \
  && pip3 install --no-cache --requirement /requirements.txt \
  && rm -rf /var/lib/apt/lists/* \
  && apt -qyy clean

#========================================
# Add normal user with passwordless sudo
#========================================
RUN set -xe \
    && useradd -u 1000 -g 100 -G sudo --shell /bin/bash --no-create-home --home-dir /io user \
    && echo 'ALL ALL = (ALL:ALL) NOPASSWD: ALL' >> /etc/sudoers \
    && echo 'fs.inotify.max_user_watches=16384' >> /etc/sysctl.conf 
    # && echo 'Defaults env_keep += "DBUS_SESSION_BUS_ADDRESS"' >> /etc/sudoers \

COPY supervisord.conf /etc/
COPY entry.sh /io/entry.sh
RUN chmod +x /io/entry.sh \
&& sudo chown 1000:100 /etc/supervisord.conf

COPY fluxbox_init /io/.fluxbox/init
COPY app /io/app
COPY run.py /io/run.py
User user



RUN sudo chown 1000:100 /io/bin/chromedriver \
&& sudo chown 1000:100 /opt/google/chrome/google-chrome \
&& sudo chown -Rv 1000:100  /io \
&& sudo mkdir -p  /io/.vnc  \
&& sudo chown -Rv 1000:100  /io/.vnc  \
&& sudo mkdir -p /var/run/supervisor/ \
&& sudo mkdir -p /var/log/supervisor/ \
&& sudo chown -Rv 1000:100 /var/run/supervisor/ \
&& sudo chown -Rv 1000:100 /var/log/supervisor
# make the new volume owned by regular user

WORKDIR /io
RUN echo "export PATH=$PATH:/io/bin" >> ~/.bash_profile
ENTRYPOINT ["python3", "/io/run.py"]
# CMD ["/io/entry.sh"]