# protocol.py
import struct

MAGIC = b"MP1!"  # 4-byte protocol magic
VERSION = 1  # 1-byte protocol version

LEN_SIGN = "!I"  # 4-byte unsigned int
LEN_SIZE = struct.calcsize(LEN_SIGN)

MAX_CMD_SIZE = 1024
MAX_DATA_SIZE = 10 * 1024 * 1024  # 10 MB


def send_bytes(sock, data: bytes):
    """Send all bytes over a socket (safe, no sendall)."""
    total = 0
    while total < len(data):
        sent = sock.send(data[total:])
        if sent == 0:
            raise ConnectionError("Socket closed while sending")
        total += sent


def send_message(sock, cmd: bytes, data: bytes):
    """Send a full message with command and payload."""
    if len(cmd) > MAX_CMD_SIZE:
        raise ValueError("Command too large")
    if len(data) > MAX_DATA_SIZE:
        raise ValueError("Data too large")

    header = (
            MAGIC +
            struct.pack("!B", VERSION) +
            struct.pack(LEN_SIGN, len(cmd)) +
            struct.pack(LEN_SIGN, len(data))
    )
    send_bytes(sock, header)
    send_bytes(sock, cmd)
    send_bytes(sock, data)


def recv_exact(sock, n):
    """Receive exactly n bytes from socket."""
    out = b""
    while len(out) < n:
        chunk = sock.recv(n - len(out))
        if not chunk:
            raise ConnectionError("Socket closed while receiving")
        out += chunk
    return out


def recv_message(sock):
    """Receive a full message and return (cmd, data)."""
    header = recv_exact(sock, 4 + 1 + LEN_SIZE + LEN_SIZE)
    magic = header[:4]
    version = header[4]
    cmd_len = struct.unpack(LEN_SIGN, header[5:9])[0]
    data_len = struct.unpack(LEN_SIGN, header[9:13])[0]

    if magic != MAGIC:
        raise ValueError("Invalid magic header")
    if version != VERSION:
        raise ValueError("Protocol version mismatch")
    if cmd_len > MAX_CMD_SIZE:
        raise ValueError("Command too large")
    if data_len > MAX_DATA_SIZE:
        raise ValueError("Data too large")

    cmd = recv_exact(sock, cmd_len)
    data = recv_exact(sock, data_len)
    return cmd, data
