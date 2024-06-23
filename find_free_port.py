import socket


def find_free_port(start_port=10000, max_ports=10):
    """
    Function to find a free port starting from start_port.
    Returns the first available port found.
    """
    for port in range(start_port, start_port + max_ports):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('localhost', port))
            return port
        except OSError:
            continue
        finally:
            sock.close()
    raise ("Could not find a free port in the specified range.")