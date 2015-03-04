import setuptools

setuptools.setup(
    name = "opencontrail-netns",
    version = "0.1",
    packages = setuptools.find_packages(),

    entry_points = {
        'console_scripts': [
            'netns-daemon-start = opencontrail_netns.daemon_start:daemon_start',
            'netns-daemon-stop = opencontrail_netns.daemon_stop:daemon_stop',
            'vn-iface-create = opencontrail_netns.vn_iface_create:vn_iface_create',
            'vn-iface-destroy = opencontrail_netns.vn_iface_destroy:vn_iface_destroy'
        ],
    }
    )
