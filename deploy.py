import paramiko
import sys
import os

HOST = os.getenv("VPS_HOST", "212.113.101.104")
USER = os.getenv("VPS_USER", "root")
PASS = os.getenv("VPS_PASS", "dcc24e258f3a")

def run_ssh_command(ssh, cmd):
    print(f"\n[EXEC] {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    while True:
        line = stdout.readline()
        if not line:
            break
        print(line, end="")
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if err:
        print(f"[STDERR] {err}")

def main():
    print(f"Подключение к {HOST} ({USER})...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=22, username=USER, password=PASS, timeout=15)
    print("Успешное подключение к VPS!")

    if len(sys.argv) > 1:
        cmd = " ".join(sys.argv[1:])
        run_ssh_command(ssh, cmd)
    else:
        print("Использование: python deploy.py <команда>")
        print("Пример: python deploy.py 'uname -a'")

    ssh.close()

if __name__ == "__main__":
    main()
