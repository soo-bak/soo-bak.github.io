---
layout: single
title: "네트워크 보안의 원리 (2) - TLS와 인증서 체계 - soo:bak"
date: "2026-01-19 23:12:02 +0900"
description: TLS 핸드셰이크, PKI, X.509 인증서, 인증서 검증 과정을 설명합니다.
tags:
  - 네트워크
  - 보안
  - TLS
  - HTTPS
  - 인증서
---

## 안전한 연결이 필요한 이유

[Part 1](/dev/network/NetworkSecurity-1/)에서 암호화의 수학적 기초를 살펴보았습니다.

대칭키 암호, 비대칭키 암호, 해시 함수.

이것들을 어떻게 조합하여 실제 안전한 통신을 만들까요?

<br>

인터넷에서 가장 널리 사용되는 보안 프로토콜이 **TLS(Transport Layer Security)**입니다.

HTTPS의 "S"가 바로 TLS입니다.

<br>

TLS가 해결해야 하는 문제:

1. **키 교환**: 처음 만난 두 당사자가 어떻게 공유 비밀을 만드는가
2. **서버 인증**: 내가 접속한 서버가 진짜 그 서버인지 어떻게 확인하는가
3. **데이터 보호**: 교환된 키로 어떻게 데이터를 암호화하고 무결성을 보장하는가

---

## TLS의 역사

**SSL(Secure Sockets Layer)**은 1994년 Netscape가 개발했습니다.

SSL 2.0이 최초의 공개 버전이었지만 심각한 취약점이 있었습니다.

SSL 3.0(1996)이 널리 사용되었습니다.

<br>

1999년, IETF가 SSL 3.0을 기반으로 **TLS 1.0**을 표준화했습니다.

- TLS 1.0 (1999): SSL 3.0과 거의 동일
- TLS 1.1 (2006): CBC 공격 완화
- TLS 1.2 (2008): SHA-256, AEAD 지원
- TLS 1.3 (2018): 대폭 개선, 레거시 제거

<br>

현재 TLS 1.2와 1.3만 안전한 것으로 간주됩니다.

TLS 1.0/1.1과 SSL은 사용하면 안 됩니다.

---

## TLS 1.2 핸드셰이크

TLS 연결은 **핸드셰이크**로 시작합니다.

암호화 파라미터를 협상하고 키를 교환합니다.

<br>

```
Client                                 Server
   │                                      │
   │ ──────── ClientHello ──────────────► │
   │                                      │
   │ ◄─────── ServerHello ─────────────── │
   │ ◄─────── Certificate ─────────────── │
   │ ◄─────── ServerKeyExchange ───────── │
   │ ◄─────── ServerHelloDone ─────────── │
   │                                      │
   │ ──────── ClientKeyExchange ────────► │
   │ ──────── ChangeCipherSpec ─────────► │
   │ ──────── Finished ─────────────────► │
   │                                      │
   │ ◄─────── ChangeCipherSpec ────────── │
   │ ◄─────── Finished ────────────────── │
   │                                      │
   │ ════════ 암호화된 통신 ════════════ │
```

<br>

**1. ClientHello**

클라이언트가 지원하는 것들을 알려줍니다:
- TLS 버전
- 지원하는 암호 스위트 목록
- 무작위 값 (client random)
- 지원하는 압축 방법

<br>

**2. ServerHello**

서버가 선택한 것들을 알려줍니다:
- 사용할 TLS 버전
- 선택한 암호 스위트
- 무작위 값 (server random)

<br>

**3. Certificate**

서버의 인증서를 전송합니다.

인증서에는 서버의 공개키가 포함되어 있습니다.

<br>

**4. ServerKeyExchange**

키 교환에 필요한 추가 파라미터를 전송합니다.

DHE나 ECDHE 사용 시 서버의 임시 공개키가 여기에 포함됩니다.

<br>

**5. ClientKeyExchange**

클라이언트의 키 교환 데이터입니다.

ECDHE의 경우 클라이언트의 임시 공개키입니다.

<br>

**6. Pre-Master Secret → Master Secret → 세션 키**

양쪽이 공유한 정보로 세션 키를 파생합니다:

```
Pre-Master Secret (키 교환으로 얻음)
       │
       ▼
Master Secret = PRF(Pre-Master Secret,
                    "master secret",
                    client random + server random)
       │
       ▼
세션 키들 = PRF(Master Secret,
                "key expansion",
                server random + client random)
```

<br>

세션 키들:
- client_write_key: 클라이언트 → 서버 암호화
- server_write_key: 서버 → 클라이언트 암호화
- client_write_MAC_key: 클라이언트 → 서버 MAC
- server_write_MAC_key: 서버 → 클라이언트 MAC

<br>

**7. Finished**

지금까지의 모든 핸드셰이크 메시지의 해시를 암호화하여 전송합니다.

상대방도 같은 값을 계산하여 비교합니다.

일치하면 키 교환이 성공한 것입니다.

---

## TLS 1.2의 문제점

TLS 1.2 핸드셰이크는 **2-RTT(Round Trip Time)**가 필요합니다.

ClientHello → ServerHello...Finished → ClientFinished → 데이터

<br>

100ms 지연의 네트워크에서 핸드셰이크만 200ms.

모바일 네트워크에서는 더 오래 걸립니다.

<br>

또한 여러 레거시 알고리즘이 여전히 허용되었습니다:
- RSA 키 교환 (전방향 비밀성 없음)
- CBC 모드 (패딩 오라클 공격 가능)
- 약한 해시 함수 (SHA-1)

---

## TLS 1.3: 단순화와 강화

2018년에 발표된 TLS 1.3은 대폭 개선되었습니다.

<br>

**핸드셰이크가 1-RTT로 단축**

```
Client                                 Server
   │                                      │
   │ ──────── ClientHello ──────────────► │
   │          + KeyShare                  │
   │                                      │
   │ ◄─────── ServerHello ─────────────── │
   │          + KeyShare                  │
   │ ◄─────── {EncryptedExtensions} ───── │
   │ ◄─────── {Certificate} ───────────── │
   │ ◄─────── {CertificateVerify} ─────── │
   │ ◄─────── {Finished} ───────────────── │
   │                                      │
   │ ──────── {Finished} ─────────────► │
   │                                      │
   │ ════════ 암호화된 통신 ════════════ │
```

{ } = 암호화된 메시지

<br>

클라이언트가 첫 메시지에 KeyShare(임시 공개키)를 포함합니다.

서버가 응답할 때 이미 암호화된 데이터를 보낼 수 있습니다.

<br>

**0-RTT 재개**

이전에 연결했던 서버라면 0-RTT로 데이터를 보낼 수 있습니다.

첫 메시지에 암호화된 애플리케이션 데이터를 포함합니다.

<br>

단, 리플레이 공격 위험이 있어 주의가 필요합니다.

GET 요청처럼 멱등성(idempotent)이 있는 요청에만 사용해야 합니다.

<br>

**레거시 제거**

TLS 1.3에서 제거된 것들:
- RSA 키 교환 (전방향 비밀성 없음)
- CBC 모드 (패딩 오라클 공격)
- RC4, DES, 3DES
- SHA-1
- 압축 (CRIME 공격)
- 재협상

<br>

남은 암호 스위트:
- TLS_AES_128_GCM_SHA256
- TLS_AES_256_GCM_SHA384
- TLS_CHACHA20_POLY1305_SHA256

<br>

모두 AEAD(인증된 암호화)를 사용합니다.

전방향 비밀성은 필수입니다 (ECDHE 또는 DHE).

---

## 인증서: 신뢰의 기반

TLS에서 서버의 공개키를 어떻게 믿을 수 있을까요?

<br>

**중간자 공격(Man-in-the-Middle, MITM)**

공격자가 클라이언트와 서버 사이에서 양쪽을 속입니다.

```
Client ◄──► Attacker ◄──► Server

Client는 Attacker가 Server인 줄 암
Server는 Attacker가 Client인 줄 암
```

<br>

공격자가 자신의 공개키를 서버의 것이라고 속이면?

클라이언트는 공격자의 키로 암호화합니다.

공격자가 복호화하고, 진짜 서버의 키로 다시 암호화해서 전달합니다.

<br>

이를 방지하려면 서버의 공개키가 **진짜 그 서버의 것**임을 확인해야 합니다.

---

## PKI: 공개키 기반 구조

**PKI(Public Key Infrastructure)**는 공개키의 소유권을 증명하는 체계입니다.

<br>

핵심 아이디어:

신뢰할 수 있는 제3자(**인증 기관, CA**)가 "이 공개키는 이 주체의 것"이라고 서명합니다.

<br>

```
웹사이트 운영자:
  1. 키 쌍 생성 (공개키, 개인키)
  2. 인증 요청서(CSR) 생성
  3. CA에 제출

CA:
  1. 신원 확인
  2. 인증서 발급 (공개키 + 신원 정보 + CA의 서명)

사용자:
  1. 웹사이트의 인증서 수신
  2. CA의 공개키로 서명 검증
  3. 유효하면 웹사이트의 공개키를 신뢰
```

---

## X.509 인증서 구조

인증서의 표준 형식은 **X.509**입니다.

<br>

주요 필드:

```
Version: 3 (현재 버전)
Serial Number: 인증서 고유 번호
Signature Algorithm: CA가 서명에 사용한 알고리즘
Issuer: 발급자 (CA) 정보
Validity:
  Not Before: 유효 시작일
  Not After: 유효 종료일
Subject: 인증서 주체 정보
Subject Public Key Info:
  Algorithm: 공개키 알고리즘
  Public Key: 실제 공개키
Extensions:
  Subject Alternative Name: 대체 도메인 이름
  Key Usage: 키 용도
  ...
Signature: CA의 서명
```

<br>

**Subject Alternative Name(SAN)**이 중요합니다.

하나의 인증서가 여러 도메인을 커버할 수 있습니다.

```
example.com
www.example.com
api.example.com
```

---

## 인증서 체인

CA의 공개키는 어떻게 믿을까요?

상위 CA가 서명합니다.

<br>

**인증서 체인(Certificate Chain)**:

```
루트 CA 인증서
     │ (서명)
     ▼
중간 CA 인증서
     │ (서명)
     ▼
서버 인증서 (End-Entity)
```

<br>

- **루트 CA**: 자기 자신을 서명 (자체 서명, self-signed)
- **중간 CA**: 루트 CA가 서명
- **서버 인증서**: 중간 CA가 서명

<br>

루트 CA 인증서는 어떻게 신뢰할까요?

운영체제와 브라우저에 **미리 설치**되어 있습니다.

이것이 **신뢰 저장소(Trust Store)**입니다.

<br>

Windows, macOS, iOS, Android, Firefox 등 각각 자체 신뢰 저장소를 관리합니다.

약 100~200개의 루트 CA가 포함되어 있습니다.

---

## 인증서 검증 과정

브라우저가 인증서를 검증하는 과정:

<br>

**1. 체인 구축**

서버가 보낸 인증서들로 루트까지 체인을 만듭니다.

<br>

**2. 서명 검증**

각 인증서의 서명이 상위 인증서의 공개키로 유효한지 확인합니다.

<br>

**3. 유효 기간 확인**

현재 시간이 Not Before와 Not After 사이인지 확인합니다.

<br>

**4. 폐기 여부 확인**

인증서가 폐기되지 않았는지 확인합니다.
- **CRL(Certificate Revocation List)**: CA가 발행하는 폐기 목록
- **OCSP(Online Certificate Status Protocol)**: 실시간 상태 확인

<br>

**5. 도메인 일치 확인**

인증서의 Subject 또는 SAN이 접속하려는 도메인과 일치하는지 확인합니다.

<br>

**6. 신뢰 루트 확인**

체인의 최상위가 신뢰 저장소에 있는 루트 CA인지 확인합니다.

---

## 인증서 투명성 (Certificate Transparency)

CA가 악의적이거나 실수로 잘못된 인증서를 발급하면?

<br>

2011년, DigiNotar CA가 해킹당했습니다.

공격자가 google.com에 대한 인증서를 발급받았습니다.

이란에서 Gmail 사용자를 대상으로 MITM 공격에 사용되었습니다.

<br>

**Certificate Transparency(CT)**는 이를 방지하기 위한 시스템입니다.

<br>

모든 인증서 발급을 공개 로그에 기록합니다.

누구나 로그를 모니터링할 수 있습니다.

도메인 소유자는 자신의 도메인에 대한 모든 인증서를 확인할 수 있습니다.

<br>

```
CA가 인증서 발급
     │
     ▼
CT 로그에 제출
     │
     ▼
SCT(Signed Certificate Timestamp) 반환
     │
     ▼
인증서에 SCT 포함
```

<br>

Chrome은 2018년부터 CT가 없는 인증서를 신뢰하지 않습니다.

---

## Let's Encrypt: 무료 자동화 인증서

전통적으로 인증서는:
- 비쌈 (연간 수십~수백 달러)
- 수동 발급 (서류 제출, 이메일 검증)
- 1~2년 유효

<br>

**Let's Encrypt**는 2016년에 시작된 무료 CA입니다.

<br>

특징:
- **무료**: 비용 없음
- **자동화**: ACME 프로토콜로 자동 발급/갱신
- **짧은 유효 기간**: 90일 (자동 갱신 권장)
- **DV 인증서만**: 도메인 소유권만 확인

<br>

**ACME(Automated Certificate Management Environment)**

도메인 소유권을 자동으로 증명합니다.

```
1. 클라이언트가 Let's Encrypt에 도메인 인증 요청
2. Let's Encrypt가 챌린지 제시 (HTTP 또는 DNS)
3. 클라이언트가 챌린지 완료 (특정 파일 배치 또는 DNS 레코드 생성)
4. Let's Encrypt가 검증
5. 인증서 발급
```

<br>

Let's Encrypt 덕분에 HTTPS 도입 비용이 크게 낮아졌습니다.

---

## 인증서의 종류

**DV(Domain Validation)**

- 도메인 소유권만 확인
- 가장 저렴하고 빠름
- Let's Encrypt가 제공하는 것

<br>

**OV(Organization Validation)**

- 조직의 실제 존재 확인
- 회사 등록 서류 검토
- 인증서에 조직 이름 포함

<br>

**EV(Extended Validation)**

- 가장 엄격한 검증
- 법적 실체, 물리적 존재, 운영 상태 확인
- 예전에는 브라우저에서 녹색 주소창으로 표시 (현재는 대부분 폐지)

<br>

기술적 보안 수준은 모두 동일합니다.

차이는 "누가 이 도메인을 운영하는가"에 대한 신뢰 수준입니다.

---

## HSTS: 다운그레이드 방지

사용자가 `http://example.com`으로 접속하면?

서버가 `https://`로 리다이렉트합니다.

<br>

하지만 첫 번째 HTTP 요청은 암호화되지 않았습니다.

공격자가 리다이렉트를 가로채고 HTTP로 유지할 수 있습니다.

이것이 **SSL Stripping** 공격입니다.

<br>

**HSTS(HTTP Strict Transport Security)**는 이를 방지합니다.

<br>

서버가 응답 헤더에 포함:
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

<br>

브라우저는 이 도메인에 대해:
- 지정된 기간 동안 HTTP 요청을 자동으로 HTTPS로 변환
- 인증서 오류 시 연결 거부 (예외 허용 안 함)

<br>

**HSTS Preload**는 더 강력합니다.

브라우저에 미리 HSTS 도메인 목록을 포함합니다.

첫 방문부터 HTTPS를 강제합니다.

---

## TLS가 보호하는 것과 보호하지 않는 것

**TLS가 보호하는 것:**
- 데이터의 기밀성 (도청 방지)
- 데이터의 무결성 (변조 방지)
- 서버 인증 (가짜 서버 방지)

<br>

**TLS가 보호하지 않는 것:**
- 메타데이터 (접속한 IP, 시간, 데이터 크기)
- SNI(Server Name Indication) - 어떤 도메인에 접속하는지 노출
- 클라이언트가 누구인지 (기본적으로)

<br>

SNI는 여러 도메인이 같은 IP를 공유할 때 필요합니다.

클라이언트가 "나는 example.com에 접속하려 한다"고 평문으로 알려줍니다.

서버가 올바른 인증서를 선택할 수 있습니다.

<br>

**Encrypted Client Hello(ECH)**는 SNI도 암호화하려는 시도입니다.

TLS 1.3의 확장으로 개발 중입니다.

<br>

[Part 3](/dev/network/NetworkSecurity-3/)에서는 네트워크 계층별 공격과 방어 메커니즘을 살펴봅니다.

---

**관련 글**
- [네트워크 보안의 원리 (1) - 암호화의 수학적 기초](/dev/network/NetworkSecurity-1/)
- [네트워크 보안의 원리 (3) - 네트워크 공격과 방어](/dev/network/NetworkSecurity-3/)
- [네트워크 통신의 원리 (3) - 프로토콜 스택과 데이터 흐름](/dev/network/NetworkCommunication-3/)
