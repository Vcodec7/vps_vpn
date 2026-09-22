# 📈 VPS Status & Health Report

**Последнее обновление:** `2026-09-22 15:19:20`
**Сервер:** `212.113.101.104`

## 🖥 Операционная система и Ядро
- **ОС:** `Debian GNU/Linux 13 (trixie)`
- **Ядро:** `6.12.85+deb13-amd64`
- **Аптайм:** `up 15 minutes`
- **TCP Контроль перегрузок:** `net.ipv4.tcp_congestion_control = bbr`

## 🧠 Память (RAM & Swap)
```
total        used        free      shared  buff/cache   available
Mem:           3.8Gi       379Mi       2.7Gi       2.0Mi       985Mi       3.5Gi
Swap:          1.0Gi          0B       1.0Gi
```

## 💾 Дисковое пространство
```
Filesystem     Type  Size  Used Avail Use% Mounted on
/dev/vda2      ext4  9.8G  2.4G  7.0G  26% /
```

## 🛡 Фаервол (UFW)
```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere                   # SSH
80/tcp                     ALLOW       Anywhere                   # HTTP / ACME
443/tcp                    ALLOW       Anywhere                   # HTTPS / VLESS Reality
443/udp                    ALLOW       Anywhere                   # QUIC / Hysteria2
2053/tcp                   ALLOW       Anywhere                   # 3X-UI Web Panel
22/tcp (v6)                ALLOW       Anywhere (v6)              # SSH
80/tcp (v6)                ALLOW       Anywhere (v6)              # HTTP / ACME
443/tcp (v6)               ALLOW       Anywhere (v6)              # HTTPS / VLESS Reality
443/udp (v6)               ALLOW       Anywhere (v6)              # QUIC / Hysteria2
2053/tcp (v6)              ALLOW       Anywhere (v6)              # 3X-UI Web Panel
```

## 🔌 Активные сетевые порты и службы
```
Netid State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess                        
tcp   LISTEN 0      128          0.0.0.0:22        0.0.0.0:*    users:(("sshd",pid=5487,fd=6))
tcp   LISTEN 0      128             [::]:22           [::]:*    users:(("sshd",pid=5487,fd=7))
```
