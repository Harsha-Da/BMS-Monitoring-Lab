import socket
import struct
import threading
import time
import random
import urllib.request
import json

current_temp = 30.0

ALERTA_API_URL = "your_domain:port/api/heartbeat"
ALERTA_API_KEY = "Your_API"
ORIGIN_NAME = "your_device_name"

def send_heartbeat():
    # Background thread to send periodic heartbeats to Alerta
    while True:
        try:
            payload = {
                "origin": ORIGIN_NAME,
                "timeout": 15,  
                "tags": ["environment:Production", "protocol:Modbus"]
            }
            req = urllib.request.Request(
                ALERTA_API_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    "Authorization": f"Key {ALERTA_API_KEY}",
                    "Content-Type": "application/json"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                print(f"[Alerta] Heartbeat sent successfully (Status: {response.status})")
        except Exception as e:
            print(f"[Alerta Error] Failed to send heartbeat: {e}")

        #Heart_beat_Frequency
        time.sleep(10)
def temp_generator():
    global current_temp
    while True:
        current_temp = round(random.uniform(30.0, 40.0), 1)
        raw_val = int(current_temp * 10)
        print(f"[Modbus Live] Holding Register 1 -> {current_temp} °C (Raw: {raw_val})")
        time.sleep(10)

def handle_client(conn):
    global current_temp
    while True:
        try:
            data = conn.recv(1024)
            if not data or len(data) < 12:
                break

            trans_id, proto_id, length, unit_id = struct.unpack(">HHHB", data[:7])
            func_code = data[7]

            if func_code == 3:
                start_addr, count = struct.unpack(">HH", data[8:12])
                val = int(current_temp * 10)
                byte_count = count * 2

                regs = [val] + [0] * (count - 1)
                reg_bytes = b"".join(struct.pack(">H", r) for r in regs)

                resp_len = 1 + 1 + 1 + byte_count
                header = struct.pack(">HHHB", trans_id, proto_id, resp_len, unit_id)
                pdu = struct.pack(">BB", func_code, byte_count) + reg_bytes

                conn.sendall(header + pdu)
        except Exception:
            break
    conn.close()

def main():
    
    threading.Thread(target=temp_generator, daemon=True).start()
    threading.Thread(target=send_heartbeat, daemon=True).start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 5020))
    server.listen(5)
    print("[+] Lightweight Modbus TCP Server with Alerta Heartbeat running on port 5020...")

    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    main()


