---
layout: single
title: "네트워크 성능과 최적화 (3) - 애플리케이션 레벨 최적화 - soo:bak"
date: "2026-01-20 22:31:15 +0900"
description: HTTP 최적화, Connection Pooling, TCP Fast Open, 캐싱, Prefetch, QUIC, 성능 측정을 설명합니다.
tags:
  - 네트워크
  - 성능
  - HTTP
  - QUIC
  - 캐싱
  - 최적화
---

## 애플리케이션에서 네트워크 성능을 어떻게 개선하는가

[Part 1](/dev/network/NetworkPerformance-1/)에서 지연의 구성 요소를,

[Part 2](/dev/network/NetworkPerformance-2/)에서 TCP 혼잡 제어를 살펴보았습니다.

<br>

이제 **애플리케이션 레벨**에서 할 수 있는 최적화를 알아봅니다.

---

## HTTP 최적화

### Keep-Alive (Persistent Connections)

HTTP/1.0은 요청마다 새 TCP 연결을 만들었습니다.

```
HTTP/1.0 (연결 재사용 안 함):
요청 1: TCP 핸드셰이크 + 요청/응답 + 연결 종료
요청 2: TCP 핸드셰이크 + 요청/응답 + 연결 종료
요청 3: TCP 핸드셰이크 + 요청/응답 + 연결 종료
```

<br>

**Keep-Alive**는 연결을 재사용하며, HTTP/1.1에서 기본으로 활성화되어 있습니다.

<br>

```
HTTP/1.1 (Keep-Alive):
TCP 핸드셰이크 (1회)
요청 1 → 응답 1
요청 2 → 응답 2
요청 3 → 응답 3
연결 종료
```

<br>

핸드셰이크 비용 절감:
- TCP 3-way 핸드셰이크: 1 RTT
- TLS 핸드셰이크: 1-2 RTT
- 연결당 2-3 RTT 절약

<br>

### 압축

응답 본문을 압축하여 전송량을 줄입니다.

<br>

```
# 요청 헤더
Accept-Encoding: gzip, deflate, br

# 응답 헤더
Content-Encoding: gzip
```

<br>

주요 압축 방식:
- **gzip**: 가장 널리 지원
- **deflate**: gzip과 유사
- **br (Brotli)**: 더 높은 압축률, 현대 브라우저 지원

<br>

텍스트 콘텐츠(HTML, CSS, JS, JSON)에 효과적:
- 50-80% 크기 감소 가능

<br>

### HTTP/2 다중화

HTTP/1.1의 문제: **Head-of-Line Blocking**

<br>

```
HTTP/1.1:
연결 1: 요청A ──────────► 응답A (느림)
         요청B는 응답A를 기다림

해결책: 병렬 연결 (브라우저는 도메인당 6개)
연결 1: 요청A ──────────► 응답A
연결 2: 요청B ──► 응답B
연결 3: 요청C ──────► 응답C
```

<br>

HTTP/2는 **하나의 연결에서 여러 스트림**을 다중화합니다.

<br>

```
HTTP/2:
하나의 연결:
  스트림 1: 요청A ──────────────► 응답A
  스트림 2: 요청B ──► 응답B
  스트림 3: 요청C ──────► 응답C

프레임 단위로 인터리빙
```

<br>

HTTP/2의 추가 기능:
- **헤더 압축 (HPACK)**: 중복 헤더 제거
- **서버 푸시**: 요청 전에 리소스 전송
- **우선순위**: 중요한 리소스 먼저

<br>

### HTTP/3과 QUIC

HTTP/2도 TCP의 Head-of-Line Blocking 문제가 있어, 패킷 손실 시 모든 스트림이 대기해야 합니다.

<br>

**QUIC**은 UDP 위에 구현된 전송 프로토콜입니다.

<br>

```
┌─────────────────────────────────────────┐
│              HTTP/3                     │
├─────────────────────────────────────────┤
│              QUIC                       │
│   - 다중 스트림 (독립적)                │
│   - 내장 TLS 1.3                        │
│   - 0-RTT 재연결                        │
├─────────────────────────────────────────┤
│              UDP                        │
└─────────────────────────────────────────┘
```

<br>

QUIC의 장점:
- **스트림 독립성**: 한 스트림 손실이 다른 스트림에 영향 없음
- **빠른 연결 설정**: 1-RTT (TLS 포함), 0-RTT 재연결
- **연결 마이그레이션**: IP 변경 시에도 연결 유지

---

## 연결 최적화

### Connection Pooling

애플리케이션 레벨에서 연결을 재사용합니다.

<br>

```
연결 풀:
┌─────────────────────────────────────────┐
│  연결 1: 유휴 (사용 가능)              │
│  연결 2: 사용 중                        │
│  연결 3: 유휴 (사용 가능)              │
│  연결 4: 사용 중                        │
└─────────────────────────────────────────┘

요청 → 풀에서 유휴 연결 획득 → 사용 → 반환
```

<br>

데이터베이스, HTTP 클라이언트에서 흔히 사용합니다.

<br>

### TCP Fast Open (TFO)

첫 번째 SYN 패킷에 데이터를 포함합니다.

<br>

```
일반 TCP:
SYN ────────────►
◄──────── SYN-ACK
ACK + 데이터 ───►  (3번째 패킷에서야 데이터)

TCP Fast Open:
SYN + 쿠키 + 데이터 ──►  (첫 패킷에 데이터!)
◄───────── SYN-ACK + 응답
ACK ────────────►
```

<br>

이미 쿠키가 있는 경우 1 RTT를 절약할 수 있습니다.

<br>

### 0-RTT 재연결

TLS 1.3과 QUIC에서 지원합니다.

<br>

이전 연결의 키를 사용하여 첫 패킷부터 암호화된 데이터를 전송합니다.

<br>

주의: **재전송 공격** 가능성

0-RTT 데이터는 멱등성 있는 요청에만 사용해야 합니다.

---

## 캐싱 전략

### 브라우저 캐시

```
# 응답 헤더
Cache-Control: max-age=3600  # 1시간 캐시
Cache-Control: no-cache      # 매번 검증
Cache-Control: no-store      # 캐시 안 함

ETag: "abc123"               # 리소스 식별자
Last-Modified: Wed, 21 Oct 2015 07:28:00 GMT
```

<br>

**조건부 요청**:

```
# 클라이언트 요청
If-None-Match: "abc123"
If-Modified-Since: Wed, 21 Oct 2015 07:28:00 GMT

# 서버 응답 (변경 없음)
304 Not Modified
(본문 없음, 대역폭 절약)
```

<br>

### CDN 캐시

전 세계 에지 서버에 콘텐츠를 캐시합니다.

<br>

```
사용자 (서울) ──► CDN 에지 (서울) ──► 원본 서버 (미국)
                     │
                캐시 있으면
                여기서 응답
                (RTT 감소)
```

<br>

### 캐시 무효화 전략

**버전/해시 기반 URL**:

```
# 파일 변경 시 URL 변경
/static/app.abc123.js  (max-age=1년)
/static/app.def456.js  (새 버전)
```

<br>

긴 캐시 시간 + URL 변경 = 즉시 갱신 가능

---

## 프리페칭과 프리커넥트

### DNS Prefetch

다음에 필요할 도메인의 DNS를 미리 조회합니다.

<br>

```html
<link rel="dns-prefetch" href="//api.example.com">
```

<br>

### Preconnect

TCP + TLS 연결을 미리 수립합니다.

<br>

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
```

<br>

### Prefetch

다음 페이지에 필요한 리소스를 미리 가져옵니다.

<br>

```html
<link rel="prefetch" href="/next-page.html">
```

<br>

### Preload

현재 페이지에 필요한 리소스를 높은 우선순위로 가져옵니다.

<br>

```html
<link rel="preload" href="/critical.css" as="style">
<link rel="preload" href="/hero.jpg" as="image">
```

---

## 프로토콜 선택

### TCP vs UDP

| 특성 | TCP | UDP |
|-----|-----|-----|
| 신뢰성 | 보장 | 없음 |
| 순서 | 보장 | 없음 |
| 연결 | 필요 | 불필요 |
| 오버헤드 | 높음 | 낮음 |
| 사용 사례 | 웹, 이메일 | 스트리밍, 게임, DNS |

<br>

### QUIC의 장점

- TCP의 신뢰성 + UDP의 유연성
- 빠른 연결 설정
- 모바일 로밍에 유리
- HTTP/3의 기반

<br>

### gRPC

HTTP/2 기반의 RPC 프레임워크로, 다음과 같은 특징이 있습니다.

<br>

- Protocol Buffers (효율적인 직렬화)
- 양방향 스트리밍
- 강타입 인터페이스

<br>

이러한 특징으로 마이크로서비스 간 통신에 적합합니다.

<br>

### WebSocket

HTTP 연결을 업그레이드하여 **양방향 통신**을 제공합니다.

<br>

```
클라이언트                 서버
    │                        │
    │ ── HTTP Upgrade ─────► │
    │ ◄── 101 Switching ─── │
    │                        │
    │ ◄────── 데이터 ──────► │
    │ ◄────── 데이터 ──────► │
    │   (양방향, 실시간)     │
```

<br>

채팅이나 알림 같은 실시간 애플리케이션에 적합합니다.

---

## 측정과 모니터링

### 핵심 지표

**TTFB (Time To First Byte)**:
- 요청 시작부터 첫 바이트 수신까지
- 서버 응답 시간 지표

<br>

**LCP (Largest Contentful Paint)**:
- 가장 큰 콘텐츠가 렌더링된 시간
- 사용자 인지 로딩 완료

<br>

**FCP (First Contentful Paint)**:
- 첫 번째 콘텐츠 렌더링 시간

<br>

**CLS (Cumulative Layout Shift)**:
- 레이아웃 이동 정도
- 시각적 안정성

<br>

### 실제 사용자 모니터링 (RUM)

실제 사용자 환경에서의 성능 데이터를 수집합니다.

<br>

```javascript
// Performance API
const timing = performance.getEntriesByType('navigation')[0];
console.log('TTFB:', timing.responseStart - timing.requestStart);
console.log('DOM Content Loaded:', timing.domContentLoadedEventEnd);
```

<br>

### 합성 모니터링

시뮬레이션된 사용자를 통해 정기적으로 성능을 측정합니다.

<br>

대표적인 도구로 Lighthouse, WebPageTest, Pingdom 등이 있습니다.

---

## 정리: 측정 없이 최적화 없다

애플리케이션 레벨 최적화 체크리스트:

<br>

**연결 최적화**:
- [ ] HTTP/2 또는 HTTP/3 사용
- [ ] Keep-Alive 활성화
- [ ] Connection Pooling

<br>

**전송 최적화**:
- [ ] 압축 (gzip, Brotli)
- [ ] 캐싱 전략 수립
- [ ] CDN 활용

<br>

**로딩 최적화**:
- [ ] Critical CSS 인라인
- [ ] JavaScript 지연 로딩
- [ ] 이미지 최적화/지연 로딩
- [ ] Preconnect/Prefetch

<br>

**측정**:
- [ ] Core Web Vitals 모니터링
- [ ] RUM 설정
- [ ] 목표 설정 및 추적

<br>

```
"측정하지 않으면 개선할 수 없다."
                - Peter Drucker
```

---

**관련 글**
- [네트워크 성능과 최적화 (1) - 지연 시간의 구성 요소](/dev/network/NetworkPerformance-1/)
- [네트워크 성능과 최적화 (2) - TCP 혼잡 제어 심화](/dev/network/NetworkPerformance-2/)
- [HTTP의 발전 (1) - HTTP/0.9에서 HTTP/2까지](/dev/network/HTTPEvolution-1/)
- [HTTP의 발전 (2) - HTTP/3과 QUIC](/dev/network/HTTPEvolution-2/)
