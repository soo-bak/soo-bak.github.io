---
layout: single
title: "HTTP의 진화 (1) - HTTP/1.0에서 HTTP/2까지 - soo:bak"
date: "2026-01-19 23:13:01 +0900"
description: HTTP/1.0, HTTP/1.1의 특성, Head-of-Line Blocking, HTTP/2의 다중화와 HPACK을 설명합니다.
tags:
  - 네트워크
  - HTTP
  - 웹
  - HTTP2
---

## 웹의 언어

[네트워크 통신의 원리 (3)](/dev/network/NetworkCommunication-3/)에서 HTTP의 기본 구조를 살펴보았습니다.

HTTP(HyperText Transfer Protocol)는 웹의 애플리케이션 계층 프로토콜입니다.

<br>

1991년 팀 버너스리(Tim Berners-Lee)가 월드 와이드 웹과 함께 HTTP를 설계했으며, 처음에는 단순한 문서 전송만을 위한 프로토콜이었습니다.

<br>

30년이 지난 지금, 웹은 복잡한 애플리케이션 플랫폼이 되었고, HTTP도 이에 맞춰 함께 진화해왔습니다.

어떤 문제들을 어떻게 해결해왔는지 살펴보겠습니다.

---

## HTTP/0.9: 시작

최초의 HTTP는 매우 단순했습니다.

<br>

```
요청:
GET /index.html

응답:
<html>
...페이지 내용...
</html>
```

<br>

특징:
- GET 메서드만 존재
- 헤더 없음
- HTML 파일만 전송
- 연결당 하나의 요청

---

## HTTP/1.0: 확장

1996년 RFC 1945로 문서화되었습니다.

<br>

```
요청:
GET /page.html HTTP/1.0
Host: example.com
User-Agent: Mozilla/5.0

응답:
HTTP/1.0 200 OK
Content-Type: text/html
Content-Length: 1234

<html>...
```

<br>

추가된 기능:
- HTTP 버전 표시
- 헤더 필드 (Host, Content-Type, 등)
- POST, HEAD 메서드
- 상태 코드 (200, 404, 500 등)
- 이미지, 비디오 등 다양한 콘텐츠

<br>

**HTTP/1.0의 문제: 연결당 하나의 요청**

```
요청 1 ──[TCP 연결]──► 응답 1 ──[연결 종료]

요청 2 ──[TCP 연결]──► 응답 2 ──[연결 종료]

요청 3 ──[TCP 연결]──► 응답 3 ──[연결 종료]
```

<br>

웹페이지 하나를 표시하려면 HTML, CSS, JavaScript, 이미지 등 수십 개의 리소스가 필요한데, 각 리소스마다 TCP 연결을 새로 맺어야 했습니다.

<br>

TCP 연결 비용:
- 3-way 핸드셰이크: 1 RTT
- TLS 핸드셰이크: 1-2 RTT 추가
- 슬로우 스타트: 처음에는 느리게 시작

<br>

리소스 50개면 50번의 연결 설정 오버헤드입니다.

---

## HTTP/1.1: 지속 연결

1997년 RFC 2068, 1999년 RFC 2616으로 표준화되었습니다.

<br>

**Keep-Alive (지속 연결)**

```
──[TCP 연결]──────────────────────────────────────────►
   요청1 → 응답1   요청2 → 응답2   요청3 → 응답3 ...
```

<br>

하나의 TCP 연결을 여러 요청에 재사용하는 방식으로, HTTP/1.1에서는 이것이 기본 동작이 되었습니다.

덕분에 연결 설정 오버헤드가 크게 줄었습니다.

<br>

**파이프라이닝(Pipelining)**

이론적으로, 응답을 기다리지 않고 여러 요청을 보낼 수 있습니다.

```
요청1 → 요청2 → 요청3 →

                      ← 응답1 ← 응답2 ← 응답3
```

<br>

하지만 파이프라이닝은 **실패**했습니다.

이유는 **Head-of-Line(HOL) Blocking** 때문입니다.

HTTP/1.1에서 응답은 반드시 요청 순서대로 와야 합니다.

따라서 요청 1의 응답이 늦어지면, 이미 준비된 요청 2, 3의 응답도 함께 대기해야 합니다.

```
요청1 → 요청2 → 요청3 →

       [응답1 지연...]
                      ← 응답1 ← 응답2 ← 응답3

       요청2, 3의 응답이 준비되어도 대기
```

<br>

결과적으로 대부분의 브라우저는 파이프라이닝을 비활성화했습니다.

---

## HTTP/1.1의 한계

**병렬 연결로 우회**

HOL Blocking 문제를 완전히 해결할 수 없었기에, 브라우저는 우회 전략을 택했습니다.

도메인당 4~8개의 병렬 연결을 열어 각 연결에서 순차적으로 요청과 응답을 처리하는 방식입니다.

<br>

```
연결1: 요청1 → 응답1   요청5 → 응답5
연결2: 요청2 → 응답2   요청6 → 응답6
연결3: 요청3 → 응답3   ...
연결4: 요청4 → 응답4   ...
```

<br>

문제:
- 연결 수 제한 (동시 연결이 너무 많으면 서버에 부담)
- 각 연결마다 TCP/TLS 오버헤드
- 여전히 연결 내에서는 HOL Blocking

<br>

**도메인 샤딩(Domain Sharding)**

브라우저의 도메인당 연결 제한을 우회합니다.

```
메인 페이지: example.com
이미지: images.example.com
스크립트: scripts.example.com
스타일: styles.example.com
```

<br>

각 도메인에 6개씩 연결하면 총 24개까지 연결을 확보할 수 있습니다.

하지만 이 방식은 DNS 조회와 연결 설정 비용이 추가되는 단점이 있습니다.

<br>

**헤더 중복**

모든 요청에 같은 헤더가 반복됩니다.

```
GET /page1.html HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...
Accept: text/html,application/xhtml+xml,...
Accept-Language: en-US,en;q=0.9,ko;q=0.8
Accept-Encoding: gzip, deflate, br
Cookie: session=abc123; preferences=...

GET /page2.html HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...  ← 같음
Accept: text/html,application/xhtml+xml,...                ← 같음
Accept-Language: en-US,en;q=0.9,ko;q=0.8                  ← 같음
Accept-Encoding: gzip, deflate, br                         ← 같음
Cookie: session=abc123; preferences=...                    ← 같음
```

<br>

이처럼 수백에서 수천 바이트에 달하는 헤더가 매 요청마다 반복되며, 텍스트 기반이라 압축하기도 어렵습니다.

---

## HTTP/2: 근본적 재설계

HTTP/1.1의 근본적인 한계를 극복하기 위해 HTTP/2가 등장했습니다.

Google의 SPDY 프로토콜에서 발전한 HTTP/2는 2015년 RFC 7540으로 표준화되었습니다.

<br>

**핵심 변화: 이진 프레이밍 계층**

HTTP/1.x가 텍스트 기반이었던 것과 달리, HTTP/2는 이진(binary) 프레이밍을 사용합니다.

<br>

```
HTTP/1.x:
GET /index.html HTTP/1.1\r\n
Host: example.com\r\n
\r\n

HTTP/2:
[프레임 헤더: 9바이트]
  Length(24비트) | Type(8비트) | Flags(8비트)
  Stream ID(31비트)
[프레임 페이로드]
```

<br>

왜 이진인가?

- 파싱이 빠름 (텍스트 파싱은 느림)
- 크기가 작음
- 오류 가능성 낮음

---

## HTTP/2 스트림과 다중화

**스트림(Stream)**은 하나의 요청-응답 쌍을 의미하며, 각 스트림은 고유한 ID를 가집니다.

<br>

**다중화(Multiplexing)**

하나의 TCP 연결에서 여러 스트림이 **동시에** 전송됩니다.

```
         ┌──────────────────────────────────────┐
TCP 연결 │  [S1][S2][S1][S3][S2][S1][S3][S2]... │
         └──────────────────────────────────────┘

S1: 스트림 1 (HTML 요청/응답)
S2: 스트림 2 (CSS 요청/응답)
S3: 스트림 3 (이미지 요청/응답)
```

<br>

각 스트림의 프레임이 인터리빙(interleaving)되어 전송되므로, 응답 순서와 상관없이 완료된 것부터 클라이언트에 전달됩니다.

<br>

**HTTP/1.1과 비교:**

```
HTTP/1.1 (순차적):
요청1 → 응답1 → 요청2 → 응답2 → 요청3 → 응답3

HTTP/2 (다중화):
요청1, 요청2, 요청3 →
← 응답2의 일부
← 응답1의 일부
← 응답3
← 응답2의 나머지
← 응답1의 나머지
```

<br>

큰 파일이 작은 파일을 막지 않습니다.

---

## HTTP/2 프레임 유형

```
타입              설명
─────────────────────────────────────
HEADERS          요청/응답 헤더
DATA             바디 데이터
PRIORITY         스트림 우선순위
RST_STREAM       스트림 취소
SETTINGS         연결 설정
PUSH_PROMISE     서버 푸시 알림
PING             연결 상태 확인
GOAWAY           연결 종료 알림
WINDOW_UPDATE    흐름 제어
CONTINUATION     HEADERS 연속
```

<br>

**스트림 우선순위(PRIORITY)**

브라우저가 중요한 리소스에 높은 우선순위를 부여합니다.

```
HTML: 우선순위 높음
CSS: 우선순위 높음
JavaScript: 중간
이미지: 낮음
```

<br>

서버는 우선순위에 따라 대역폭을 분배합니다.

---

## HPACK: 헤더 압축

HTTP/2는 **HPACK**으로 헤더를 압축합니다.

<br>

**정적 테이블**

자주 사용되는 61개의 헤더를 미리 정의합니다.

```
인덱스  헤더                     값
─────────────────────────────────────
1      :authority
2      :method                 GET
3      :method                 POST
4      :path                   /
5      :path                   /index.html
...
61     www-authenticate
```

<br>

따라서 인덱스만 전송하면 되어, ":method: GET"을 보내는 대신 "2"만 전송해도 됩니다.

<br>

**동적 테이블**

연결 중에 새 헤더가 나오면 동적 테이블에 추가하고, 이후 같은 헤더가 나타나면 인덱스로 참조합니다.

<br>

```
첫 번째 요청:
Cookie: session=abc123...  → 전체 전송, 동적 테이블에 저장 (인덱스 62)

두 번째 요청:
Cookie: session=abc123...  → "62"만 전송
```

<br>

**허프만 인코딩**

테이블에 없는 문자열은 허프만 코딩으로 압축하는데, 자주 사용되는 문자에 짧은 코드를 할당하는 방식입니다.

<br>

이러한 기법들을 통해 헤더 크기가 85~90%까지 감소합니다.

---

## 서버 푸시

서버가 클라이언트의 요청 **전에** 리소스를 보낼 수 있습니다.

<br>

```
클라이언트: GET /index.html

서버:
  PUSH_PROMISE (나는 /style.css도 보낼 거야)
  PUSH_PROMISE (나는 /script.js도 보낼 거야)
  HEADERS (응답: /index.html)
  DATA (/index.html 내용)
  HEADERS (응답: /style.css)
  DATA (/style.css 내용)
  HEADERS (응답: /script.js)
  DATA (/script.js 내용)
```

<br>

HTML을 파싱하고 CSS/JS를 요청하는 시간을 절약합니다.

<br>

하지만 실제로는 문제가 있습니다:

- 클라이언트가 이미 캐시에 가지고 있을 수 있음 (대역폭 낭비)
- 푸시할 리소스 결정이 어려움
- 브라우저 지원과 구현의 차이

<br>

결과적으로 서버 푸시는 실제로 잘 사용되지 않으며, HTTP/3에서도 지원은 하지만 권장하지 않습니다.

---

## HTTP/2의 HOL Blocking 문제

HTTP/2는 HTTP 레벨의 HOL Blocking을 해결하여, 하나의 스트림이 느려도 다른 스트림은 진행될 수 있게 되었습니다.

<br>

하지만 **TCP 레벨의 HOL Blocking**이 남아있습니다.

<br>

TCP는 순서를 보장하는 프로토콜이므로, 패킷 하나가 손실되면 재전송을 기다려야 합니다.

<br>

```
TCP 패킷 흐름:
[패킷1] [패킷2] [패킷3 손실] [패킷4] [패킷5]

TCP 수신 버퍼:
[패킷1] [패킷2] [      ?      ] [패킷4] [패킷5]

패킷 4, 5는 도착했지만 애플리케이션에 전달 불가
패킷 3 재전송 대기 중...
```

<br>

HTTP/2에서 이것이 문제가 되는 이유:

여러 스트림이 하나의 TCP 연결을 공유하기 때문에, 패킷 3이 스트림 1의 것이라도 스트림 2, 3도 모두 대기해야 합니다.

<br>

```
[S1-P1] [S2-P1] [S1-P2 손실] [S3-P1] [S2-P2]

스트림 2, 3의 패킷이 도착했지만
스트림 1의 패킷 재전송까지 모두 대기
```

<br>

이것이 HTTP/3에서 TCP를 버리고 QUIC를 사용하는 이유입니다.

[Part 2](/dev/network/HTTPEvolution-2/)에서 살펴봅니다.

---

## HTTP/2 도입 시 고려사항

**TLS 필수화**

표준상 HTTP/2는 TLS 없이도 동작합니다 (h2c).

하지만 모든 주요 브라우저는 TLS 위에서만 HTTP/2를 지원합니다 (h2).

사실상 HTTP/2 = HTTPS입니다.

<br>

**ALPN(Application-Layer Protocol Negotiation)**

TLS 핸드셰이크 중에 HTTP 버전을 협상합니다.

추가 RTT 없이 HTTP/2 사용 가능 여부를 결정합니다.

<br>

**기존 최적화 재고**

HTTP/1.1을 위한 최적화가 HTTP/2에서는 오히려 해로울 수 있습니다:

- 도메인 샤딩: 불필요 (연결 하나로 충분)
- 이미지 스프라이트: 불필요 (다중화로 개별 요청해도 됨)
- 인라인 CSS/JS: 푸시로 대체 가능
- 연결 수 최소화: 이미 하나로 충분

---

## HTTP/1.1에서 HTTP/2로

HTTP/2는 HTTP/1.1과 의미적으로(semantically) 호환됩니다.

- 같은 메서드 (GET, POST, PUT, DELETE...)
- 같은 상태 코드 (200, 404, 500...)
- 같은 헤더 필드 (대부분)

<br>

차이는 **전송 방식(framing)**입니다.

```
HTTP/1.1:
텍스트 기반, 개행 구분, 순차적

HTTP/2:
이진 프레임, 길이 지정, 다중화
```

<br>

따라서 애플리케이션 코드는 대부분 수정 없이 동작하며, 서버와 클라이언트 라이브러리가 전송 계층을 처리합니다.

---

**관련 글**
- [네트워크 통신의 원리 (3) - 프로토콜 스택과 데이터 흐름](/dev/network/NetworkCommunication-3/)
- [HTTP의 진화 (2) - HTTP/3과 WebSocket](/dev/network/HTTPEvolution-2/)
- [네트워크 보안의 원리 (2) - TLS와 인증서 체계](/dev/network/NetworkSecurity-2/)
