---
layout: single
title: "네트워크 디버깅 (2) - 패킷 분석 - soo:bak"
date: "2026-01-20 22:31:20 +0900"
description: 패킷 캡처 원리, tcpdump, Wireshark, TCP 문제 분석, TLS 트래픽 분석, 실제 사례를 설명합니다.
tags:
  - 네트워크
  - 디버깅
  - tcpdump
  - Wireshark
  - 패킷분석
  - TLS
---

## 패킷 레벨에서 무엇을 볼 수 있는가

[Part 1](/dev/network/NetworkDebugging-1/)에서 계층별 진단 도구를 살펴보았습니다.

<br>

더 깊은 분석이 필요할 때, **패킷 캡처**를 사용합니다.

이를 통해 실제로 네트워크를 지나는 데이터를 직접 확인할 수 있습니다.

---

## 패킷 캡처의 원리

### Promiscuous 모드

일반적으로 NIC는 자신에게 온 패킷만 받습니다.

**Promiscuous 모드**에서는 네트워크의 모든 패킷을 받습니다.

<br>

```
일반 모드:
NIC → 내 MAC 주소인가? → 예 → 처리
                        → 아니오 → 폐기

Promiscuous 모드:
NIC → 모든 패킷 처리 (캡처)
```

<br>

스위치 환경에서는 자신에게 오는 패킷만 보이므로, 모든 트래픽을 캡처하려면 **포트 미러링** 설정이 필요합니다.

<br>

### BPF (Berkeley Packet Filter)

커널에서 효율적으로 패킷을 필터링합니다.

<br>

```
                     ┌─────────────────┐
                     │   사용자 공간   │
                     │   (tcpdump)     │
                     └────────┬────────┘
                              │
                              │ 필터된 패킷만
                              │
                     ┌────────┴────────┐
                     │      BPF        │ ← 커널에서 필터링
                     │   (필터 실행)   │
                     └────────┬────────┘
                              │
                              │ 모든 패킷
                              │
                     ┌────────┴────────┐
                     │      NIC        │
                     └─────────────────┘
```

<br>

불필요한 패킷이 사용자 공간까지 올라가지 않아 효율적입니다.

<br>

### 캡처 위치의 중요성

```
클라이언트 ─────── 방화벽 ─────── 서버

클라이언트에서 캡처: 나가는 패킷 O, 방화벽에서 차단되면 응답 X
서버에서 캡처: 방화벽 통과한 패킷만 보임
방화벽에서 캡처: 차단된 패킷도 볼 수 있음
```

<br>

어디서 캡처하느냐에 따라 보이는 것이 다릅니다.

---

## tcpdump 활용

### 기본 사용법

```bash
# 기본 캡처 (모든 패킷)
sudo tcpdump -i eth0

# 패킷 내용까지 (hex + ASCII)
sudo tcpdump -i eth0 -X

# 파일로 저장
sudo tcpdump -i eth0 -w capture.pcap

# 저장된 파일 읽기
tcpdump -r capture.pcap
```

<br>

### 필터 문법

```bash
# 호스트 필터
tcpdump host 192.168.1.10
tcpdump src host 192.168.1.10
tcpdump dst host 192.168.1.10

# 네트워크 필터
tcpdump net 192.168.1.0/24

# 포트 필터
tcpdump port 80
tcpdump port 80 or port 443
tcpdump portrange 8000-8080

# 프로토콜 필터
tcpdump tcp
tcpdump udp
tcpdump icmp

# 조합
tcpdump "host 192.168.1.10 and port 80"
tcpdump "src host 192.168.1.10 and dst port 443"
```

<br>

### 자주 쓰는 필터

```bash
# HTTP 트래픽
tcpdump -i eth0 "tcp port 80"

# HTTPS 트래픽
tcpdump -i eth0 "tcp port 443"

# DNS 쿼리
tcpdump -i eth0 "udp port 53"

# TCP SYN 패킷만 (연결 시도)
tcpdump -i eth0 "tcp[tcpflags] & tcp-syn != 0"

# TCP RST 패킷만 (연결 거부/리셋)
tcpdump -i eth0 "tcp[tcpflags] & tcp-rst != 0"

# ICMP (ping)
tcpdump -i eth0 icmp
```

<br>

### 출력 해석

```bash
tcpdump -i eth0 -n port 80

# 22:31:01.123456 IP 192.168.1.10.54321 > 93.184.216.34.80: Flags [S], seq 123456789, win 65535, options [mss 1460,sackOK,TS val 123 ecr 0,nop,wscale 7], length 0
```

<br>

해석:
- `22:31:01.123456`: 타임스탬프
- `192.168.1.10.54321`: 출발지 IP:포트
- `93.184.216.34.80`: 목적지 IP:포트
- `Flags [S]`: TCP 플래그 (S=SYN)
- `seq`: 시퀀스 번호
- `win`: 윈도우 크기
- `length`: 페이로드 길이

<br>

TCP 플래그:
- `S`: SYN
- `F`: FIN
- `R`: RST
- `P`: PSH
- `.`: ACK (플래그 없음 표시)
- `[S.]`: SYN+ACK

---

## Wireshark 활용

### GUI 기반 분석

Wireshark는 그래픽 기반의 패킷 분석 도구입니다.

<br>

장점:
- 프로토콜 디코딩 (HTTP, DNS, TLS 등을 해석)
- 대화별 필터링
- 통계 및 그래프
- Follow Stream (대화 전체 보기)

<br>

### 캡처 필터 vs 디스플레이 필터

**캡처 필터** (tcpdump와 같은 BPF 문법):
- 캡처할 때 적용
- 필터에 맞는 패킷만 저장
- 예: `host 192.168.1.10 and port 80`

<br>

**디스플레이 필터** (Wireshark 고유):
- 이미 캡처된 패킷을 필터링
- 더 강력한 필터 문법
- 예: `http.request.method == "GET"`

<br>

### 유용한 디스플레이 필터

```
# IP 주소
ip.addr == 192.168.1.10
ip.src == 192.168.1.10
ip.dst == 192.168.1.10

# 포트
tcp.port == 80
tcp.srcport == 443

# HTTP
http
http.request
http.response
http.request.method == "POST"
http.response.code == 404

# DNS
dns
dns.qry.name == "example.com"

# TLS
tls
tls.handshake
tls.handshake.type == 1  # Client Hello

# TCP 문제
tcp.analysis.retransmission
tcp.analysis.duplicate_ack
tcp.analysis.zero_window
tcp.flags.reset == 1

# 특정 대화
tcp.stream eq 5
```

<br>

### Follow Stream

TCP 연결의 전체 대화를 볼 수 있습니다.

```
Right-click → Follow → TCP Stream

HTTP 요청/응답이 읽기 쉽게 표시됨:
GET /index.html HTTP/1.1
Host: example.com
...

HTTP/1.1 200 OK
Content-Type: text/html
...
```

---

## TCP 문제 분석

### 재전송 패턴

```
패킷 흐름:
1. [TCP] seq=1, len=1000  →  (전송)
2. [TCP] seq=1001, len=1000  →  (전송)
3. [TCP] seq=1, len=1000  →  (재전송! 1번 손실됨)
```

<br>

Wireshark에서:
- `[TCP Retransmission]`으로 표시
- 검정/빨강 배경색

<br>

재전송이 자주 발생하면 네트워크 혼잡이나 패킷 손실을 의심해야 합니다.

<br>

### 윈도우 스케일링

```
# TCP 옵션에서 확인
Options: ... Window scale: 7 (multiply by 128)

실제 윈도우 = 헤더의 윈도우 값 × 스케일 팩터
```

<br>

윈도우 스케일이 없으면 최대 64KB로 제한되어 고대역폭 환경에서 성능 저하의 원인이 됩니다.

<br>

### RST 원인 분석

TCP RST는 연결을 강제 종료합니다.

<br>

원인 분석:
- **닫힌 포트**: 대상에서 해당 포트를 listen하지 않음
- **방화벽**: 연결 차단 시 RST 응답
- **애플리케이션**: 비정상 종료
- **타임아웃**: 오래된 연결 정리

<br>

```
RST 패킷 전후 맥락 확인:
- SYN → RST: 포트 닫힘 또는 방화벽
- 데이터 → RST: 애플리케이션 문제
```

---

## TLS 트래픽 분석

### 핸드셰이크 확인

TLS 내용은 암호화되어 볼 수 없지만, 핸드셰이크는 볼 수 있습니다.

<br>

```
1. Client Hello
   - 지원 TLS 버전
   - 지원 암호 스위트
   - SNI (Server Name Indication)

2. Server Hello
   - 선택된 TLS 버전
   - 선택된 암호 스위트

3. Certificate
   - 서버 인증서

4. Key Exchange
   - 키 교환 데이터

5. Finished
   - 핸드셰이크 완료
```

<br>

### 인증서 문제 확인

```
Wireshark → TLS → Certificate

인증서 체인:
1. 서버 인증서
2. 중간 CA
3. 루트 CA (보통 미포함)

문제 확인:
- 만료된 인증서
- 잘못된 호스트명
- 체인 불완전
```

<br>

### SSLKEYLOGFILE

**복호화된 TLS 트래픽**을 보려면 키가 필요합니다.

<br>

```bash
# 환경 변수 설정
export SSLKEYLOGFILE=/tmp/keys.log

# 브라우저 또는 curl 실행
curl https://example.com

# Wireshark에서:
# Edit → Preferences → Protocols → TLS
# (Pre)-Master-Secret log filename: /tmp/keys.log
```

<br>

개발 및 디버깅 환경에서만 사용해야 하며, 프로덕션 환경에서는 심각한 보안 위험이 될 수 있습니다.

---

## 실제 사례

### 연결 실패

증상: curl이 타임아웃

<br>

```bash
tcpdump -i eth0 "host example.com and port 80"

# 결과:
# SYN →
# SYN →  (재전송)
# SYN →  (재전송)
# (응답 없음)
```

<br>

분석: SYN에 응답이 없음

원인 후보:
- 방화벽 차단
- 서버 다운
- 잘못된 라우팅

<br>

### 느린 응답

증상: 웹 페이지 로딩이 느림

<br>

```
Wireshark로 분석:
1. DNS 응답: 빠름 (10ms)
2. TCP 핸드셰이크: 빠름 (30ms)
3. TLS 핸드셰이크: 빠름 (100ms)
4. HTTP 요청 전송: 즉시
5. HTTP 응답 시작: 3초 후!  ← 문제

서버 처리 시간이 느림 (TTFB 문제)
```

<br>

### 간헐적 문제

증상: 가끔 연결이 끊김

<br>

```
장시간 캡처 후 분석:
- 정상 연결들...
- 22:30:45: [TCP RST]
- 22:45:12: [TCP RST]

RST 전후 패킷 분석:
- 일정 시간(900초) 유휴 후 RST
- 방화벽/NAT 타임아웃 의심

해결: Keep-alive 간격 조정
```

---

## 정리: 패킷은 거짓말하지 않는다

패킷 분석의 핵심:

<br>

1. **적절한 위치**에서 캡처
2. **필터**로 관련 트래픽만 추출
3. **시간순**으로 흐름 따라가기
4. **프로토콜 지식**으로 해석
5. **비정상 패턴** 식별

<br>

```
"When in doubt, packet capture."

의심스러우면 패킷을 캡처하라.
```

<br>

애플리케이션 로그는 이미 해석된 정보지만, 패킷은 **실제로 일어난 일** 그 자체입니다.

---

**관련 글**
- [네트워크 디버깅 (1) - 계층별 진단 도구](/dev/network/NetworkDebugging-1/)
- [소켓과 전송 계층 (2) - TCP의 연결 관리와 신뢰성](/dev/network/SocketTransport-2/)
- [네트워크 보안의 원리 (2) - TLS와 인증서 체계](/dev/network/NetworkSecurity-2/)
