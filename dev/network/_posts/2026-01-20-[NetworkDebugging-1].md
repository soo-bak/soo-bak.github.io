---
layout: single
title: "네트워크 디버깅 (1) - 계층별 진단 도구 - soo:bak"
date: "2026-01-20 22:31:19 +0900"
description: 계층별 문제 해결, ARP, ping, traceroute, 포트 상태 확인, DNS 진단 도구를 설명합니다.
tags:
  - 네트워크
  - 디버깅
  - ping
  - traceroute
  - DNS
  - netstat
---

## 네트워크 문제를 어떻게 진단하는가

"인터넷이 안 돼요."

가장 흔하지만 가장 모호한 문의입니다.

<br>

이 시리즈에서 다루어 온 [네트워크 통신의 원리](/dev/network/NetworkCommunication-1/), [TCP/IP 스택](/dev/network/SocketTransport-1/), [라우팅](/dev/network/Routing-1/), [DNS](/dev/network/DNS-1/) 등의 지식은 단순히 이론으로 끝나지 않습니다. 문제가 발생했을 때 원인을 빠르게 찾아내는 것이 이 지식의 실전적 가치입니다.

<br>

네트워크는 여러 계층이 쌓여 동작하기 때문에, 문제의 원인도 물리 계층부터 애플리케이션 계층까지 어디에나 있을 수 있습니다. 문제 해결의 첫 단계는 **어디서** 문제가 발생하는지 찾는 것입니다.

---

## 문제 해결 방법론

### 계층별 접근

[OSI 모델과 TCP/IP 스택](/dev/network/NetworkCommunication-1/)을 따라 아래에서 위로 확인합니다.

<br>

```
확인 순서:
┌─────────────────────────────────────┐
│ 7. 애플리케이션  ← HTTP, DNS 확인   │
├─────────────────────────────────────┤
│ 4. 전송 계층     ← 포트, 연결 확인  │
├─────────────────────────────────────┤
│ 3. 네트워크 계층 ← IP, 라우팅 확인  │
├─────────────────────────────────────┤
│ 2. 데이터 링크   ← MAC, ARP 확인    │
├─────────────────────────────────────┤
│ 1. 물리 계층     ← 케이블, 연결 확인│
└─────────────────────────────────────┘
```

<br>

### 분할 정복

네트워크 경로의 중간 지점을 먼저 확인하여 문제 범위를 절반으로 좁힙니다.

<br>

```
클라이언트 ─── 스위치 ─── 라우터 ─── 인터넷 ─── 서버
                            │
                     여기까지 정상 응답?
                       → 오른쪽(서버 방향) 확인

                     여기서 응답 실패?
                       → 왼쪽(클라이언트 방향) 확인
```

<br>

### 가설과 검증

네트워크 문제 해결에서 가장 효과적인 방법은 가설 기반 접근입니다. 증상을 관찰한 뒤 하나의 가설을 세우고, 해당 가설을 검증할 수 있는 최소한의 테스트를 수행합니다. 예를 들어 "DNS 문제"라는 가설이 있다면, 도메인 대신 IP 주소로 직접 접속해보는 것으로 즉시 검증할 수 있습니다.

<br>

1. 증상 관찰
2. 가설 수립 (예: "DNS 문제 같다")
3. 테스트 (예: "IP로 직접 접속해보자")
4. 결과 확인
5. 가설 수정 또는 다음 단계

---

## L2 진단: 데이터 링크 계층

### ARP 테이블 확인

```bash
# Linux
ip neigh show
# 또는
arp -a

# 결과 예시:
# 192.168.1.1 dev eth0 lladdr 00:11:22:33:44:55 REACHABLE
# 192.168.1.100 dev eth0 lladdr aa:bb:cc:dd:ee:ff STALE
```

<br>

ARP 테이블의 각 항목은 상태(state)를 가지며, 이 상태가 현재 L2 통신의 건강 상태를 직접적으로 보여줍니다. REACHABLE이나 STALE은 정상 범위이지만, INCOMPLETE이나 FAILED는 대상 호스트에 도달할 수 없음을 의미합니다.

상태 의미:
- **REACHABLE**: 최근 확인됨
- **STALE**: 오래됨, 재확인 필요
- **INCOMPLETE**: ARP 응답 없음 (문제!)
- **FAILED**: ARP 실패

<br>

INCOMPLETE이나 FAILED가 있으면:
- 대상이 네트워크에 없음
- 대상이 ARP에 응답하지 않음
- L2 연결 문제

<br>

### MAC 주소 문제

```bash
# 인터페이스 MAC 확인
ip link show eth0
# link/ether 00:11:22:33:44:55 brd ff:ff:ff:ff:ff:ff
```

<br>

MAC 충돌은 드물지만 발생하면 심각합니다. 랜덤하게 연결이 끊기거나 트래픽이 예상치 못한 곳으로 향하게 됩니다.

<br>

### 스위치 포트 상태

```bash
# Linux: 인터페이스 상태
ip link show
# eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
#       UP: 관리자 활성화
#       LOWER_UP: 물리적 연결됨

# ethtool로 자세한 정보
ethtool eth0
# Link detected: yes
# Speed: 1000Mb/s
# Duplex: Full
```

---

## L3 진단: 네트워크 계층

### ping의 원리

**ICMP Echo Request/Reply**를 사용합니다.

<br>

```
클라이언트                        대상
    │                              │
    │ ── ICMP Echo Request ──────► │
    │                              │
    │ ◄── ICMP Echo Reply ──────── │
    │                              │
```

<br>

```bash
ping 8.8.8.8

# PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
# 64 bytes from 8.8.8.8: icmp_seq=1 ttl=116 time=32.5 ms
# 64 bytes from 8.8.8.8: icmp_seq=2 ttl=116 time=31.8 ms
# ...
#
# --- 8.8.8.8 ping statistics ---
# 5 packets transmitted, 5 received, 0% packet loss, time 4005ms
# rtt min/avg/max/mdev = 31.8/32.1/32.5/0.3 ms
```

<br>

ping의 출력에서 주의 깊게 봐야 할 항목은 네 가지입니다. 단순히 "응답이 오는가"뿐 아니라, RTT의 편차나 패킷 손실률로 네트워크 품질을 판단합니다. TTL 값에서 경유한 라우터 수를 역산할 수도 있습니다(Linux 초기값 64, Windows 초기값 128).

확인할 것:
- **응답 여부**: 대상에 도달 가능한가
- **RTT**: 지연 시간
- **패킷 손실**: 안정성
- **TTL**: 홉 수 추정 (초기값 - TTL)

<br>

### ping이 실패하는 이유

ping 실패 ≠ 연결 불가능

<br>

ping 실패 시 에러 메시지 유형을 구분하면 원인을 좁힐 수 있습니다. "Destination unreachable"은 라우팅 문제, 응답 없음(타임아웃)은 방화벽이나 서버 다운, "Time exceeded"는 TTL 소진으로 라우팅 루프를 의심할 수 있습니다.

가능한 원인:
- **경로 없음**: 라우팅 문제
- **방화벽**: ICMP 차단
- **대상 다운**: 서버 문제
- **TTL 초과**: 라우팅 루프 가능성

<br>

많은 서버가 보안상 ICMP를 차단하기 때문에, ping이 실패해도 HTTP 요청은 정상적으로 처리될 수 있습니다.

<br>

### traceroute / mtr

경로상의 각 홉을 확인합니다.

<br>

```bash
traceroute google.com

# traceroute to google.com (142.250.185.46), 30 hops max
#  1  192.168.1.1 (192.168.1.1)  1.234 ms  1.156 ms  1.089 ms
#  2  10.0.0.1 (10.0.0.1)  5.678 ms  5.432 ms  5.321 ms
#  3  * * *  (응답 없음)
#  4  72.14.198.18 (72.14.198.18)  15.432 ms  15.321 ms  15.210 ms
#  5  142.250.185.46 (142.250.185.46)  20.123 ms  20.012 ms  19.987 ms
```

<br>

원리:
1. TTL=1로 패킷 전송 → 첫 라우터에서 TTL 초과 → ICMP Time Exceeded 응답
2. TTL=2로 패킷 전송 → 두 번째 라우터에서 TTL 초과
3. ...
4. 목적지 도달

<br>

traceroute 결과에서 `* * *`는 해당 홉에서 ICMP Time Exceeded 응답을 받지 못했다는 뜻입니다. 이것이 반드시 문제를 의미하는 것은 아닙니다. 많은 ISP 라우터는 보안상 ICMP 응답을 차단하기 때문에, 중간에 `* * *`가 있어도 최종 목적지에 도달한다면 정상입니다.

`* * *`의 의미:
- ICMP를 차단하는 라우터
- 응답이 느린 라우터
- 단방향 경로 문제

<br>

**mtr**은 traceroute + ping을 결합합니다:

```bash
mtr google.com

# 실시간으로 업데이트되는 통계
# Host                   Loss%   Snt   Last   Avg  Best  Wrst
# 1. 192.168.1.1          0.0%    50    1.2   1.3   1.0   2.1
# 2. 10.0.0.1             0.0%    50    5.4   5.5   5.2   6.1
# 3. (no response)       100.0%   50    0.0   0.0   0.0   0.0
# 4. 72.14.198.18         0.0%    50   15.3  15.4  15.1  16.2
```

<br>

### 라우팅 테이블 확인

```bash
# Linux
ip route show
# 또는
route -n

# default via 192.168.1.1 dev eth0 proto dhcp metric 100
# 192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.10
# 10.0.0.0/8 via 192.168.1.254 dev eth0
```

<br>

확인할 것:
- 기본 게이트웨이(default) 존재 여부
- 목적지로 가는 경로 존재 여부
- 잘못된 경로가 있는지

---

## L4 진단: 전송 계층

### 포트 상태 확인

```bash
# ss (socket statistics) - Linux 권장
ss -tuln
# -t: TCP
# -u: UDP
# -l: listening
# -n: 숫자로 표시

# State    Recv-Q Send-Q Local Address:Port   Peer Address:Port
# LISTEN   0      128    0.0.0.0:22          0.0.0.0:*
# LISTEN   0      128    0.0.0.0:80          0.0.0.0:*
# LISTEN   0      128    [::]:443            [::]:*
```

<br>

```bash
# netstat (전통적)
netstat -tuln
```

<br>

### TCP 연결 상태

```bash
ss -tan
# State      Recv-Q Send-Q Local Address:Port  Peer Address:Port
# LISTEN     0      128    0.0.0.0:80         0.0.0.0:*
# ESTAB      0      0      192.168.1.10:22    192.168.1.100:54321
# TIME-WAIT  0      0      192.168.1.10:80    10.0.0.5:12345
```

<br>

상태 의미:
- **LISTEN**: 연결 대기 중
- **ESTABLISHED**: 연결 수립됨
- **TIME-WAIT**: 연결 종료 후 대기
- **SYN-SENT**: 연결 시도 중
- **CLOSE-WAIT**: 상대가 종료, 내가 종료 대기

<br>

### 포트 도달 가능성 테스트

```bash
# nc (netcat)
nc -zv example.com 80
# Connection to example.com 80 port [tcp/http] succeeded!

nc -zv example.com 443
# Connection to example.com 443 port [tcp/https] succeeded!

# 실패 시:
nc -zv example.com 12345
# nc: connect to example.com port 12345 (tcp) failed: Connection refused
```

<br>

### 방화벽 규칙 확인

```bash
# iptables (Linux)
sudo iptables -L -n -v

# nftables (최신 Linux)
sudo nft list ruleset

# UFW (Ubuntu)
sudo ufw status verbose
```

---

## DNS 진단

### dig

DNS 쿼리를 자세히 보여줍니다.

<br>

```bash
dig example.com

# ;; QUESTION SECTION:
# ;example.com.                   IN      A
#
# ;; ANSWER SECTION:
# example.com.            3600    IN      A       93.184.216.34
#
# ;; Query time: 45 msec
# ;; SERVER: 8.8.8.8#53(8.8.8.8)
# ;; WHEN: Mon Jan 20 22:31:00 KST 2026
```

<br>

유용한 옵션:

```bash
# 특정 DNS 서버 지정
dig @8.8.8.8 example.com

# 특정 레코드 타입
dig example.com MX
dig example.com AAAA
dig example.com NS

# 짧은 출력
dig +short example.com
# 93.184.216.34

# 추적 (재귀적으로 해석)
dig +trace example.com
```

<br>

### nslookup

```bash
nslookup example.com
# Server:         192.168.1.1
# Address:        192.168.1.1#53
#
# Non-authoritative answer:
# Name:   example.com
# Address: 93.184.216.34
```

<br>

### DNS 캐시 문제

```bash
# Linux: systemd-resolved 캐시 확인
systemd-resolve --statistics

# 캐시 플러시
sudo systemd-resolve --flush-caches

# macOS
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

# Windows
ipconfig /flushdns
```

<br>

### 전파 지연

DNS 레코드를 변경하면 전 세계 DNS 서버로 전파되기까지 시간이 소요됩니다.

<br>

```bash
# 여러 DNS 서버에서 확인
dig @8.8.8.8 example.com +short    # Google DNS
dig @1.1.1.1 example.com +short    # Cloudflare DNS
dig @208.67.222.222 example.com +short  # OpenDNS
```

<br>

결과가 서버마다 다르게 나온다면 아직 전파가 진행 중인 상태입니다.

---

## 마무리: 계층을 따라가라

진단 순서 체크리스트:

<br>

1. **물리/L2**
   - [ ] 케이블 연결 확인
   - [ ] 인터페이스 상태 (ip link)
   - [ ] ARP 테이블 (ip neigh)

<br>

2. **L3**
   - [ ] IP 주소 설정 (ip addr)
   - [ ] 로컬 게이트웨이 ping
   - [ ] 인터넷 IP ping (8.8.8.8)
   - [ ] 라우팅 테이블 (ip route)

<br>

3. **DNS**
   - [ ] DNS 쿼리 (dig)
   - [ ] 다른 DNS 서버 시도

<br>

4. **L4**
   - [ ] 포트 열림 확인 (nc)
   - [ ] 방화벽 규칙 확인

<br>

5. **애플리케이션**
   - [ ] curl/wget으로 HTTP 테스트
   - [ ] 애플리케이션 로그 확인

<br>

[Part 2](/dev/network/NetworkDebugging-2/)에서는 패킷 분석 도구를 살펴봅니다.

<br>

---

**관련 글**
- [네트워크 통신의 원리 (1) - 데이터는 어떻게 전달되는가](/dev/network/NetworkCommunication-1/)
- [DNS의 원리와 구조 (1) - DNS의 탄생과 계층 구조](/dev/network/DNS-1/)

**시리즈**
- 네트워크 디버깅 (1) - 계층별 진단 도구 (현재 글)
- [네트워크 디버깅 (2) - 패킷 분석](/dev/network/NetworkDebugging-2/)
