#!/usr/bin/env python3
"""
VPS VPN & Server Orchestrator
Автоматизирует управление сервером, применение настроек, аудит и синхронизацию с GitHub.
"""

import os
import sys
import subprocess
import paramiko
from datetime import datetime

# Обеспечиваем корректный вывод UTF-8 в Windows-консоли
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Параметры подключения к серверу
HOST = os.getenv("VPS_HOST", "212.113.101.104")
USER = os.getenv("VPS_USER", "root")
PASS = os.getenv("VPS_PASS", "dcc24e258f3a")

# Пути к Git и GitHub CLI на машине
GIT_PATH = r"C:\Users\Евгений\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\CodexTools\ssh-workspace-tooling\PortableGit\cmd\git.exe"
if not os.path.exists(GIT_PATH):
    GIT_PATH = "git"


def get_ssh_client():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=22, username=USER, password=PASS, timeout=20)
    return ssh


def run_remote(ssh, command, print_output=True):
    if print_output:
        print(f"\n[VPS EXEC] {command}")
    stdin, stdout, stderr = ssh.exec_command(command, timeout=300)
    out = stdout.read().decode("utf-8", errors="replace").strip()
    err = stderr.read().decode("utf-8", errors="replace").strip()
    if print_output and out:
        print(out)
    if print_output and err:
        print(f"[STDERR] {err}")
    return out, err


def action_optimize(ssh):
    print("=== [1/4] Обновление пакетов ОС (apt update && apt upgrade) ===")
    run_remote(
        ssh,
        "export DEBIAN_FRONTEND=noninteractive && apt-get update -y && apt-get upgrade -y && apt-get autoremove -y",
    )

    print("\n=== [2/4] Установка базовых утилит ===")
    run_remote(
        ssh,
        "export DEBIAN_FRONTEND=noninteractive && apt-get install -y curl wget git ufw htop jq tar socat fail2ban net-tools ca-certificates gnupg",
    )

    print("\n=== [3/4] Включение TCP BBR и оптимизация сети ===")
    bbr_cmds = """
    modprobe tcp_bbr 2>/dev/null || true
    echo "tcp_bbr" >> /etc/modules-load.d/bbr.conf 2>/dev/null || true
    cat << 'EOF' > /etc/sysctl.d/99-vps-vpn.conf
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1
net.core.rmem_max = 67108864
net.core.wmem_max = 67108864
net.core.rmem_default = 65536
net.core.wmem_default = 65536
net.core.netdev_max_backlog = 10000
net.ipv4.tcp_rmem = 4096 87380 67108864
net.ipv4.tcp_wmem = 4096 65536 67108864
net.ipv4.tcp_mtu_probing = 1
vm.swappiness = 10
EOF
    sysctl --system
    """
    run_remote(ssh, bbr_cmds)

    print("\n=== [4/4] Настройка Swap (1GB) ===")
    swap_cmds = """
    if [ ! -f /swapfile ]; then
        fallocate -l 1G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=1024
        chmod 600 /swapfile
        mkswap /swapfile
        swapon /swapfile
        echo '/swapfile none swap sw 0 0' >> /etc/fstab
    fi
    """
    run_remote(ssh, swap_cmds)
    print("\n✅ Оптимизация сервера успешно выполнена!")


def action_security(ssh):
    print("=== Настройка безопасности UFW и Fail2ban ===")
    sec_cmds = """
    ufw --force reset
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow 22/tcp comment 'SSH'
    ufw allow 80/tcp comment 'HTTP / ACME'
    ufw allow 443/tcp comment 'HTTPS / VLESS Reality'
    ufw allow 443/udp comment 'QUIC / Hysteria2'
    ufw allow 2053/tcp comment '3X-UI Web Panel'
    echo "y" | ufw enable
    systemctl enable --now fail2ban
    systemctl restart fail2ban
    ufw status verbose
    """
    run_remote(ssh, sec_cmds)
    print("\n✅ Безопасность настроена!")


def action_status(ssh):
    print("=== Сбор статуса и метрик сервера ===")
    uname, _ = run_remote(ssh, "uname -r", False)
    os_name, _ = run_remote(
        ssh,
        "grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '\"'",
        False,
    )
    uptime, _ = run_remote(ssh, "uptime -p", False)
    mem, _ = run_remote(ssh, "free -h", False)
    disk, _ = run_remote(ssh, "df -hT /", False)
    bbr, _ = run_remote(ssh, "sysctl net.ipv4.tcp_congestion_control", False)
    ports, _ = run_remote(ssh, "ss -tulpn", False)
    ufw, _ = run_remote(ssh, "ufw status", False)

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    status_content = f"""# 📈 VPS Status & Health Report

**Последнее обновление:** `{now_str}`
**Сервер:** `{HOST}`

## 🖥 Операционная система и Ядро
- **ОС:** `{os_name}`
- **Ядро:** `{uname}`
- **Аптайм:** `{uptime}`
- **TCP Контроль перегрузок:** `{bbr}`

## 🧠 Память (RAM & Swap)
```
{mem}
```

## 💾 Дисковое пространство
```
{disk}
```

## 🛡 Фаервол (UFW)
```
{ufw}
```

## 🔌 Активные сетевые порты и службы
```
{ports}
```
"""
    status_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "STATUS.md"
    )
    with open(status_file, "w", encoding="utf-8") as f:
        f.write(status_content)
    print(f"✅ Статус сохранен в {status_file}")


def action_git_sync(commit_msg=None):
    if not commit_msg:
        commit_msg = f"Auto-sync: update VPS configuration and status [{datetime.now().strftime('%Y-%m-%d %H:%M')}]"

    repo_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"=== Синхронизация с GitHub ({repo_dir}) ===")

    env = os.environ.copy()
    env["PATH"] = (
        r"C:\Users\Евгений\bin;C:\Users\Евгений\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\CodexTools\ssh-workspace-tooling\PortableGit\cmd;"
        + env.get("PATH", "")
    )

    try:
        subprocess.run(
            [GIT_PATH, "add", "."], cwd=repo_dir, check=True, env=env
        )
        # Check if anything to commit
        res = subprocess.run(
            [GIT_PATH, "status", "--porcelain"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            env=env,
        )
        if res.stdout.strip():
            subprocess.run(
                [
                    GIT_PATH,
                    "-c",
                    "user.name=Vcodec7",
                    "-c",
                    "user.email=vcodec7@users.noreply.github.com",
                    "commit",
                    "-m",
                    commit_msg,
                ],
                cwd=repo_dir,
                check=True,
                env=env,
            )
            print("Коммит создан.")
        else:
            print("Нет изменений для коммита.")

        subprocess.run(
            [GIT_PATH, "push", "origin", "main"],
            cwd=repo_dir,
            check=True,
            env=env,
        )
        print("🚀 Изменения успешно отправлены на GitHub!")
    except Exception as e:
        print(f"❌ Ошибка Git синхронизации: {e}")


def main():
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python manage.py optimize    - Полная оптимизация VPS (apt, BBR, sysctl, swap)")
        print("  python manage.py security    - Настройка UFW фаервола и Fail2ban")
        print("  python manage.py status      - Сбор метрик и генерация STATUS.md")
        print("  python manage.py full-cycle  - Оптимизация + Безопасность + Статус + GitHub Push")
        print("  python manage.py sync        - Синхронизация репозитория с GitHub")
        print("  python manage.py exec <cmd>  - Выполнить произвольную команду на сервере")
        return

    cmd = sys.argv[1].lower()

    if cmd == "sync":
        action_git_sync()
        return

    ssh = get_ssh_client()
    try:
        if cmd == "optimize":
            action_optimize(ssh)
            action_status(ssh)
            action_git_sync("Apply VPS optimization (BBR, Swap, sysctl tweaks, apt upgrade)")
        elif cmd == "security":
            action_security(ssh)
            action_status(ssh)
            action_git_sync("Apply UFW and Fail2ban security settings")
        elif cmd == "status":
            action_status(ssh)
            action_git_sync("Update VPS Status report")
        elif cmd == "full-cycle":
            print("\n>>> ЗАПУСК ПОЛНОГО ЦИКЛА РАБОТ <<<\n")
            action_optimize(ssh)
            action_security(ssh)
            action_status(ssh)
            action_git_sync("Full cycle: system update, BBR, sysctl, UFW security, metrics update")
        elif cmd == "exec":
            exec_cmd = " ".join(sys.argv[2:])
            run_remote(ssh, exec_cmd)
        else:
            print(f"Неизвестная команда: {cmd}")
    finally:
        ssh.close()


if __name__ == "__main__":
    main()
