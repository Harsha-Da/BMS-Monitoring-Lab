import socket
import struct
import threading
import time
import math

current_temp = 25.0

def temp_generator():
    global current_temp
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        current_temp = round(32.5 + 7.5 * math.sin(elapsed / 3), 1)
        print(f"[Modbus Live] Holding Register 1 -> {current_temp} °C (Raw: {in>
        time.sleep(1)

def handle_client(conn):
    global current_temp
    while True:
        try:
            data = conn.recv(1024)
            if not data or len(data) < 12:
                break

            # Modbus TCP Header (MBAP): Transaction ID, Protocol ID, Length, Un>
            trans_id, proto_id, length, unit_id = struct.unpack(">HHHB", data[:>
            func_code = data[7]

            # Function Code 3: Read Holding Registers
            if func_code == 3:
                start_addr, count = struct.unpack(">HH", data[8:12])
                val = int(current_temp * 10)  # 
                byte_count = count * 2

 # Register values 
                regs = [val] + [0] * (count - 1)
                reg_bytes = b"".join(struct.pack(">H", r) for r in regs)

                resp_len = 1 + 1 + 1 + byte_count  # Unit ID + Func + ByteCount>
                header = struct.pack(">HHHB", trans_id, proto_id, resp_len, uni>
                pdu = struct.pack(">BB", func_code, byte_count) + reg_bytes
                conn.sendall(header + pdu)
        except Exception:
            break
    conn.close()

def main():
    threading.Thread(target=temp_generator, daemon=True).start()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 5020))
    server.listen(5)
    print("[+] Lightweight Modbus TCP Server running on port 5020...")

    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start>

if __name__ == "__main__":
    main()
