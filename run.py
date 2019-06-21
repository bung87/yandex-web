from app.driver_wrapper import DriverWrapper
from app.pages.yandex import Yandex
import time
from os import path
import sys
import signal
import subprocess
from selenium.common.exceptions import NoSuchWindowException
import traceback
import argparse
import base64

def main():
    parser = argparse.ArgumentParser(prog='yandex-web')
    parser.add_argument('task_type', help='task type')
    parser.add_argument('task_args', nargs='*', default=[], help='task args')
    parsed = parser.parse_args()
    task_type = parsed.task_type
    wrapper = DriverWrapper()
    yandex = Yandex(wrapper)
  
    def nice_quite():
        wrapper.driver.quit()
        wrapper.driver.stop_client()
        yandex.stop()
        exit(1)

    def signal_term_handler(signal, frame):
        nice_quite()

    signal.signal(signal.SIGINT, signal_term_handler)
    signal.signal(signal.SIGILL, signal_term_handler)
    signal.signal(signal.SIGTERM, signal_term_handler)

    try:

        if task_type == "reg":
            yandex.reg(*parsed.task_args)
        elif task_type == "auth":
            yandex.auth_task(*parsed.task_args)
        elif task_type == "reg_test":
            # PASS='' PHONE=''  python run.py reg_test 'first_name' 'last_name'
            first_name = base64.b64encode( parsed.task_args[0].encode() )
            last_name = base64.b64encode( parsed.task_args[1].encode() )
            yandex.reg(first_name.decode(),last_name.decode())
        yandex.stop()
    except KeyboardInterrupt:
        nice_quite()
    except NoSuchWindowException:
        nice_quite()
    except Exception as e:
        sys.stderr.write(traceback.format_exc())
        nice_quite()

if __name__ == "__main__":
    main()
