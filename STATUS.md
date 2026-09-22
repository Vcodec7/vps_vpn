# 📈 VPS Status & Health Report

**Последнее обновление:** `2026-09-22 16:03:26`
**Сервер:** `212.113.101.104`

## 🖥 Операционная система и Ядро
- **ОС:** `Debian GNU/Linux 13 (trixie)`
- **Ядро:** `6.12.85+deb13-amd64`
- **Аптайм:** `up 59 minutes`
- **TCP Контроль перегрузок:** `net.ipv4.tcp_congestion_control = bbr`

## 🧠 Память (RAM & Swap)
```
total        used        free      shared  buff/cache   available
Mem:           3.8Gi       471Mi       1.6Gi       2.0Mi       2.0Gi       3.4Gi
Swap:          1.0Gi          0B       1.0Gi
```

## 💾 Дисковое пространство
```
Filesystem     Type  Size  Used Avail Use% Mounted on
/dev/vda2      ext4  9.8G  3.4G  6.0G  36% /
```

## 🛡 Фаервол (UFW)
```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere                   # SSH
80/tcp                     ALLOW       Anywhere                   # HTTP / ACME
443/tcp                    ALLOW       Anywhere                  
443/udp                    ALLOW       Anywhere                  
2053/tcp                   ALLOW       Anywhere                  
2096/tcp                   ALLOW       Anywhere                  
51820/udp                  ALLOW       Anywhere                  
8443/tcp                   ALLOW       Anywhere                  
8444/tcp                   ALLOW       Anywhere                  
18550/tcp                  ALLOW       Anywhere                  
22/tcp (v6)                ALLOW       Anywhere (v6)              # SSH
80/tcp (v6)                ALLOW       Anywhere (v6)              # HTTP / ACME
443/tcp (v6)               ALLOW       Anywhere (v6)             
443/udp (v6)               ALLOW       Anywhere (v6)             
2053/tcp (v6)              ALLOW       Anywhere (v6)             
2096/tcp (v6)              ALLOW       Anywhere (v6)             
51820/udp (v6)             ALLOW       Anywhere (v6)             
8443/tcp (v6)              ALLOW       Anywhere (v6)             
8444/tcp (v6)              ALLOW       Anywhere (v6)             
18550/tcp (v6)             ALLOW       Anywhere (v6)
```

## 🔌 Активные сетевые порты и службы
```
Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess                                     
udp   UNCONN 0      0            0.0.0.0:51820      0.0.0.0:*                                               
udp   UNCONN 0      0                  *:8443             *:*    users:(("xray-linux-amd6",pid=13253,fd=8)) 
udp   UNCONN 0      0               [::]:51820         [::]:*                                               
tcp   LISTEN 0      4096       127.0.0.1:62789      0.0.0.0:*    users:(("xray-linux-amd6",pid=13253,fd=3)) 
tcp   LISTEN 0      128          0.0.0.0:22         0.0.0.0:*    users:(("sshd",pid=5487,fd=6))             
tcp   LISTEN 0      4096       127.0.0.1:11111      0.0.0.0:*    users:(("xray-linux-amd6",pid=13253,fd=10))
tcp   LISTEN 0      4096               *:443              *:*    users:(("xray-linux-amd6",pid=13253,fd=6)) 
tcp   LISTEN 0      4096               *:8444             *:*    users:(("xray-linux-amd6",pid=13253,fd=9)) 
tcp   LISTEN 0      4096               *:8443             *:*    users:(("xray-linux-amd6",pid=13253,fd=7)) 
tcp   LISTEN 0      4096               *:18550            *:*    users:(("x-ui",pid=13246,fd=10))           
tcp   LISTEN 0      128             [::]:22            [::]:*    users:(("sshd",pid=5487,fd=7))             
tcp   LISTEN 0      4096               *:2096             *:*    users:(("x-ui",pid=13246,fd=11))
```
