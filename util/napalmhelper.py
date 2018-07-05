from napalm.base import get_network_driver
import sys

from celery import shared_task

class NapalmHelper:

    @shared_task
    def configure_device(target, config, commit=False):
        vendor = "iosxr"
        username = "vrnetlab"
        password = "VR-netlab9"
        driver = get_network_driver(vendor)

        with driver(target, username, password) as device:
            device.load_merge_candidate(config=config)

            diff = device.compare_config()

            if commit:
                device.commit_config()

            return diff



if __name__ == '__main__':
    config = "hostname foo"
    print(NapalmHelper.configure_device(target="172.17.0.2", config=config, commit=True))
