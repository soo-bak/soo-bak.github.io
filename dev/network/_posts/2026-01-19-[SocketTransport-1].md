---
layout: single
title: "소켓과 전송 계층 (1) - 소켓의 탄생과 추상화 - soo:bak"
date: "2026-01-19 23:14:01 +0900"
description: Berkeley Sockets의 역사, 소켓의 본질, 5-tuple 식별, 소켓 API의 설계 철학을 설명합니다.
tags:
  - 네트워크
  - 소켓
  - TCP/IP
  - 운영체제
---

## 프로세스 간 통신의 역사

1970년대 Unix 운영체제에서 프로세스들은 서로 통신해야 했습니다.

같은 컴퓨터에서 실행되는 프로세스끼리 데이터를 주고받는 것을 **IPC(Inter-Process Communication)**라고 합니다.

<br>

Unix는 여러 IPC 메커니즘을 제공했습니다.

**파이프(Pipe)**는 한 프로세스의 출력을 다른 프로세스의 입력으로 연결합니다.

```
프로세스 A → [파이프] → 프로세스 B

ls | grep ".txt"  ← ls의 출력이 grep의 입력으로
```

파이프는 단방향이고, 부모-자식 관계의 프로세스 사이에서만 작동합니다.

<br>

**메시지 큐**, **공유 메모리**, **세마포어** 같은 더 복잡한 메커니즘도 있었습니다.

하지만 이것들은 모두 **같은 컴퓨터** 안에서만 작동했습니다.

<br>

1970년대 후반, ARPANET이 성장하면서 새로운 요구가 생겼습니다.

**다른 컴퓨터에 있는 프로세스와 통신하려면 어떻게 해야 하는가?**

기존 IPC는 네트워크를 고려하지 않았습니다.

네트워크 통신을 위한 새로운 추상화가 필요했습니다.

---

## Berkeley Sockets의 등장

1983년, UC Berkeley의 BSD 4.2가 발표되었습니다.

Bill Joy가 이끄는 팀이 DARPA의 지원을 받아 개발한 이 운영체제에는 혁신적인 네트워크 API가 포함되어 있었습니다.

**Berkeley Sockets**입니다.

<br>

Berkeley Sockets의 핵심 철학은 이것이었습니다.

**"네트워크 통신도 파일처럼 다루자."**

<br>

Unix에서 모든 것은 파일입니다.

하드디스크, 프린터, 키보드도 파일처럼 열고(open), 읽고(read), 쓰고(write), 닫습니다(close).

네트워크 연결도 마찬가지로 다룰 수 있다면, 기존 프로그래밍 모델을 그대로 사용할 수 있습니다.

<br>

```
파일:     open()  →  read()/write()  →  close()

소켓:     socket() → connect() → read()/write() → close()
```

이 설계 덕분에 프로그래머는 네트워크의 복잡한 세부사항을 알 필요가 없었습니다.

이미 익숙한 파일 I/O 개념으로 네트워크 프로그래밍을 할 수 있었습니다.

<br>

Berkeley Sockets는 빠르게 표준이 되었습니다.

BSD Unix뿐 아니라 System V Unix, Linux, Windows(Winsock), macOS 등 거의 모든 운영체제가 이 API를 채택했습니다.

40년이 지난 지금도 네트워크 프로그래밍의 기본 인터페이스입니다.

---

## 소켓이란 무엇인가

"소켓"이라는 용어는 혼란을 일으키기 쉽습니다.

많은 사람들이 소켓을 "IP 주소와 포트의 조합"이라고 이해합니다.

```
192.168.1.100:8080  ← 이것이 소켓?
```

**이것은 정확하지 않습니다.**

IP:포트는 소켓의 일부일 뿐, 소켓 자체가 아닙니다.

<br>

소켓의 본질을 이해하려면 커널 내부를 봐야 합니다.

**소켓은 커널이 관리하는 데이터 구조입니다.**

<br>

애플리케이션이 `socket()` 함수를 호출하면, 커널은 내부에 데이터 구조를 생성합니다.

이 구조에는 통신에 필요한 모든 정보가 담깁니다.

```
커널 내 소켓 구조 (단순화)
┌─────────────────────────────────┐
│  프로토콜 정보 (TCP/UDP)         │
│  로컬 IP 주소                    │
│  로컬 포트 번호                  │
│  원격 IP 주소                    │
│  원격 포트 번호                  │
│  연결 상태 (LISTEN, ESTABLISHED) │
│  송신 버퍼                       │
│  수신 버퍼                       │
│  타이머, 시퀀스 번호, 옵션...     │
└─────────────────────────────────┘
```

<br>

`socket()` 함수는 이 구조에 대한 **파일 디스크립터(File Descriptor)**를 반환합니다.

```c
int sockfd = socket(AF_INET, SOCK_STREAM, 0);
// sockfd = 3 (예: 파일 디스크립터 번호)
```

이 숫자(3)는 커널 내 소켓 구조를 가리키는 핸들입니다.

이후 모든 작업은 이 번호를 통해 수행됩니다.

```c
write(sockfd, data, len);   // 소켓으로 데이터 전송
read(sockfd, buffer, len);  // 소켓에서 데이터 수신
close(sockfd);              // 소켓 닫기
```

<br>

**소켓은 통신 끝점(Endpoint)의 추상화입니다.**

네트워크 연결의 한쪽 끝을 나타내는 커널 객체이며, 애플리케이션은 파일 디스크립터를 통해 이 객체와 상호작용합니다.

---

## 5-Tuple: 연결의 고유 식별

TCP 연결은 어떻게 식별될까요?

같은 서버에 여러 클라이언트가 연결하면 어떻게 구분할까요?

<br>

답은 **5-tuple**입니다.

```
(프로토콜, 로컬 IP, 로컬 포트, 원격 IP, 원격 포트)
```

<br>

이 다섯 가지 값의 조합이 하나의 연결을 고유하게 식별합니다.

```
연결 1: (TCP, 192.168.1.100, 8080, 10.0.0.1, 52001)
연결 2: (TCP, 192.168.1.100, 8080, 10.0.0.1, 52002)
연결 3: (TCP, 192.168.1.100, 8080, 10.0.0.2, 52001)
```

세 연결 모두 같은 서버(192.168.1.100:8080)에 대한 것이지만, 클라이언트 정보가 다르므로 별개의 연결입니다.

<br>

**왜 5개가 필요한가?**

4개로는 부족합니다.

```
프로토콜이 없다면:
  TCP와 UDP가 같은 포트를 쓸 때 구분 불가

원격 IP가 없다면:
  어느 클라이언트의 연결인지 구분 불가

원격 포트가 없다면:
  같은 클라이언트의 여러 연결 구분 불가
```

5-tuple은 연결을 식별하는 **최소한의 완전한 집합**입니다.

<br>

**하나의 서버 포트, 수천 개의 연결**

이제 웹 서버가 어떻게 수천 개의 동시 연결을 처리하는지 이해할 수 있습니다.

```
웹 서버: 192.168.1.100:80 (LISTEN 상태의 소켓)

연결된 클라이언트들:
┌────────────────────────────────────────────────────┐
│ (TCP, 192.168.1.100, 80, 203.0.113.1, 50001)      │ ← 클라이언트 A
│ (TCP, 192.168.1.100, 80, 203.0.113.1, 50002)      │ ← 클라이언트 A (2번째)
│ (TCP, 192.168.1.100, 80, 198.51.100.5, 49000)     │ ← 클라이언트 B
│ (TCP, 192.168.1.100, 80, 192.0.2.10, 55555)       │ ← 클라이언트 C
│ ...                                                │
└────────────────────────────────────────────────────┘
```

서버의 로컬 주소(192.168.1.100:80)는 모두 같습니다.

하지만 각 연결의 5-tuple은 다릅니다.

커널은 들어오는 패킷의 5-tuple을 확인하여 어느 소켓으로 전달할지 결정합니다.

<br>

클라이언트 포트는 보통 운영체제가 자동으로 할당합니다.

이를 **임시 포트(Ephemeral Port)**라고 하며, 보통 49152 ~ 65535 범위입니다.

---

## 소켓 API의 설계

Berkeley Sockets API의 주요 함수들을 살펴봅시다.

각 함수가 하는 일의 본질을 이해하는 것이 중요합니다.

<br>

### socket(): 소켓 생성

```c
int socket(int domain, int type, int protocol);

// 예시
int sockfd = socket(AF_INET, SOCK_STREAM, 0);
```

`socket()`은 커널에 소켓 데이터 구조를 생성하고, 파일 디스크립터를 반환합니다.

이 시점에서 소켓은 아직 어떤 주소에도 바인딩되지 않았고, 어디에도 연결되지 않았습니다.

**빈 통신 끝점**이 생성된 것입니다.

<br>

`AF_INET`은 IPv4를 의미합니다.

`SOCK_STREAM`은 바이트 스트림(TCP)을, `SOCK_DGRAM`은 데이터그램(UDP)을 의미합니다.

<br>

### bind(): 주소 할당

```c
int bind(int sockfd, struct sockaddr *addr, socklen_t addrlen);

// 예시: 모든 인터페이스의 8080 포트에 바인딩
struct sockaddr_in addr;
addr.sin_family = AF_INET;
addr.sin_addr.s_addr = INADDR_ANY;  // 0.0.0.0
addr.sin_port = htons(8080);
bind(sockfd, (struct sockaddr*)&addr, sizeof(addr));
```

`bind()`는 소켓에 로컬 주소(IP와 포트)를 할당합니다.

서버는 클라이언트가 연결할 주소를 알려야 하므로 `bind()`가 필수입니다.

<br>

클라이언트는 보통 `bind()`를 호출하지 않습니다.

`connect()` 시 커널이 자동으로 적절한 로컬 주소를 할당합니다.

<br>

### listen(): 연결 대기

```c
int listen(int sockfd, int backlog);

// 예시: 최대 128개의 대기 연결 허용
listen(sockfd, 128);
```

`listen()`은 소켓을 **수동 모드(Passive Mode)**로 전환합니다.

이 소켓은 이제 직접 통신하지 않고, 들어오는 연결 요청을 기다립니다.

<br>

`backlog`는 **연결 대기열의 크기**입니다.

클라이언트의 SYN이 도착했지만 아직 `accept()`되지 않은 연결이 여기에 대기합니다.

대기열이 가득 차면 새로운 연결 요청이 거부됩니다.

<br>

```
                         ┌─────────────────┐
클라이언트 SYN 도착 ──→   │   연결 대기열    │
                         │  (backlog 크기) │
                         └────────┬────────┘
                                  │
                         accept() 호출
                                  ↓
                         새 연결 소켓 생성
```

<br>

### accept(): 연결 수락

```c
int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);

// 예시
struct sockaddr_in client_addr;
socklen_t len = sizeof(client_addr);
int conn_fd = accept(listen_fd, (struct sockaddr*)&client_addr, &len);
```

`accept()`는 대기열에서 완료된 연결을 꺼내고, **새로운 소켓**을 생성합니다.

<br>

이것이 핵심입니다.

`listen()` 상태의 소켓은 연결을 받기만 합니다.

실제 데이터 통신은 `accept()`가 반환한 **새 소켓**에서 일어납니다.

```
listen_fd: 계속 새 연결을 받음 (포트 8080)
     │
     ├── accept() → conn_fd_1: 클라이언트 A와 통신
     │
     ├── accept() → conn_fd_2: 클라이언트 B와 통신
     │
     └── accept() → conn_fd_3: 클라이언트 C와 통신
```

<br>

### connect(): 연결 시작 (클라이언트)

```c
int connect(int sockfd, struct sockaddr *addr, socklen_t addrlen);

// 예시: 서버에 연결
struct sockaddr_in server_addr;
server_addr.sin_family = AF_INET;
server_addr.sin_addr.s_addr = inet_addr("192.168.1.100");
server_addr.sin_port = htons(8080);
connect(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr));
```

`connect()`는 클라이언트 측에서 서버로 연결을 시작합니다.

TCP의 경우, 이 함수가 3-Way Handshake를 수행합니다.

<br>

### 전체 흐름

서버와 클라이언트의 소켓 API 사용 흐름입니다.

```
서버                                클라이언트
  │                                    │
socket()                            socket()
  │                                    │
bind()                                 │
  │                                    │
listen()                               │
  │                                    │
  │←─────────── SYN ──────────── connect() 시작
  │                                    │
  │──────── SYN+ACK ────────────→      │
  │                                    │
  │←─────────── ACK ──────────── connect() 완료
  │                                    │
accept() ─→ 새 소켓 생성               │
  │                                    │
read()/write() ←────────────→ read()/write()
  │                                    │
close()                            close()
```

---

## 왜 이 추상화가 중요한가

Berkeley Sockets가 40년간 표준으로 유지된 이유가 있습니다.

<br>

**첫째, 복잡성을 숨깁니다.**

애플리케이션 개발자는 TCP의 상태 기계, 패킷 재조립, 흐름 제어, 혼잡 제어를 몰라도 됩니다.

`read()`와 `write()`만 호출하면 커널이 모든 것을 처리합니다.

<br>

**둘째, 프로토콜 독립적입니다.**

같은 API로 TCP, UDP, Unix 도메인 소켓, 심지어 새로운 프로토콜도 사용할 수 있습니다.

`socket()` 호출 시 타입만 바꾸면 됩니다.

<br>

**셋째, 운영체제 독립적입니다.**

Linux, Windows, macOS에서 거의 동일한 코드가 동작합니다.

이것이 인터넷 애플리케이션의 이식성을 가능하게 했습니다.

<br>

**넷째, 파일 I/O와 통합됩니다.**

`select()`, `poll()`, `epoll()` 같은 I/O 다중화 메커니즘은 파일 디스크립터를 사용합니다.

소켓도 파일 디스크립터이므로, 파일, 파이프, 소켓을 하나의 이벤트 루프에서 처리할 수 있습니다.

```c
// select()로 파일과 소켓을 동시에 감시
fd_set readfds;
FD_SET(file_fd, &readfds);
FD_SET(socket_fd, &readfds);
select(max_fd + 1, &readfds, NULL, NULL, NULL);
```

<br>

---

[Part 2](/dev/network/SocketTransport-2/)에서는 TCP 연결의 상태 기계를 살펴봅니다.

`connect()`와 `accept()` 뒤에서 어떤 일이 일어나는지, TCP의 11가지 상태가 무엇을 의미하는지, TIME_WAIT가 왜 필요한지 알아봅니다.

<br>

---

**관련 글**
- [네트워크 통신의 원리 (1) - 전자기파와 신호 전송](/dev/network/NetworkCommunication-1/)
- [네트워크 통신의 원리 (2) - 디지털 신호와 정보 전달](/dev/network/NetworkCommunication-2/)
- [네트워크 통신의 원리 (3) - 프로토콜 스택과 데이터 흐름](/dev/network/NetworkCommunication-3/)

**시리즈**
- 소켓과 전송 계층 (1) - 소켓의 탄생과 추상화 (현재 글)
- [소켓과 전송 계층 (2) - TCP 연결의 상태 기계](/dev/network/SocketTransport-2/)
- [소켓과 전송 계층 (3) - 멀티플렉싱과 패킷 흐름](/dev/network/SocketTransport-3/)

