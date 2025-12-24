import socket
import ssl

def check_port(host, port):
    print(f"Checking {host}:{port}...")
    try:
        sock = socket.create_connection((host, port), timeout=5)
        print(f"✅ Connected to {host}:{port}")
        sock.close()
        return True
    except Exception as e:
        print(f"❌ Failed to connect to {host}:{port} - {e}")
        return False

host = "smtp.titan.email"
check_port(host, 587)
check_port(host, 465)
