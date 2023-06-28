from netmiko.ssh_dispatcher import ConnectHandler


def run():
    # conn = ConnectHandler()
    conn = ConnectHandler(ip="127.0.0.1", device_type='h3c_telnet')
    print(conn)


if __name__ == '__main__':
    run()
