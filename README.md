# yandex-web


## Requirements

- [Python 3](https://www.python.org/downloads) Tested with 3.4.3, 3.6.1
- [selenium](http://selenium-python.readthedocs.io/installation.html) Tested with 2.53.6, 3.4.2
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) Tested with 2.24, 2.29
- [Chrome Web Browser](https://www.google.com/chrome/browser/desktop) compatible with the ChromeDriver version you downloaded. (Eg. ChromeDriver 2.29 supports Chrome v56-58) You can get this info from the ChromeDriver download page.

## Installation

`sh ./bin/install`  
`pip3 install -r requirements.txt`  

## Usage  

### local  

`EMAIL=<your email> PASS='<your password>'python3 run.py <task_type> <task_args>`

task type and args:
 * accept_invitation
 * follow "url"
 * forward "url"
 * reg 'first name' 'last name'
 

### docker

build docker image  

`docker build . -t yandex`  
`docker build -f vnc.Dockerfile . -t yandex-vnc` 
envs:  

* EMAIL required: account email
* PASS required: account password
* KEEP_SESSION: no-empty character

when `KEEP_SESSION`  

add `-v /var/run/snc:/var/run/snc` to docker run command.  
and make sure host machine /var/run/snc is writable.

run it temporarily
`docker run --shm-size=128m --rm --env EMAIL=<EMAIL> --env PASS='<PASS>' --env HEADLESS=1 yandex follow "https://www.yandex.com/company/yandex/"`

run it temporarily and exports vnc to 6900 port  

`docker run --shm-size=128m --rm -it -p 6900:5900 --env EMAIL=<EMAIL> --env PASS='<PASS>' yandex-vnc`

run it temporarily  with socks5 proxy and exports vnc to 6900 port  

`docker run --shm-size=128m --rm -it -p 6900:5900 --env EMAIL=<EMAIL> -v $(pwd)/shadowsocks.json:/io/shadowsocks.json --env PASS='<PASS>' yandex-vnc`  

visit vnc address through browser:  

`vnc://localhostOrRemoteAddr:6900`  
password:`hola`  

**note** 
open chrome devtools will increase memory usage continually  

### Disclaimer

Not affiliated with yandex.
