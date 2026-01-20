---
layout: single
title: "실시간 통신 (2) - WebRTC 스택 - soo:bak"
date: "2026-01-20 22:31:17 +0900"
description: WebRTC 구성요소, getUserMedia, RTCPeerConnection, 시그널링, SDP, ICE, DTLS-SRTP를 설명합니다.
tags:
  - 네트워크
  - WebRTC
  - P2P
  - SDP
  - ICE
  - SRTP
---

## WebRTC는 브라우저에서 어떻게 P2P 통신하는가

[Part 1](/dev/network/RealTimeCommunication-1/)에서 RTP의 기본을 살펴보았습니다.

**WebRTC**는 브라우저에서 **플러그인 없이** 화상 통화, 음성 통화, 데이터 전송 등의 실시간 통신을 가능하게 합니다.

---

## WebRTC의 탄생

2011년, Google이 GIPS(Global IP Solutions) 인수로 확보한 미디어 엔진을 기반으로 WebRTC 프로젝트를 오픈소스로 공개했습니다.

<br>

목표:
- 플러그인(Flash, Silverlight) 없이 실시간 통신
- 브라우저 네이티브 API
- P2P 연결 (서버 부하 감소)

<br>

2021년에 W3C와 IETF 표준화가 완료되었으며, 현재 모든 주요 브라우저에서 지원됩니다.

---

## WebRTC 구성 요소

```
┌─────────────────────────────────────────────────────────────┐
│                       WebRTC APIs                           │
├────────────────┬────────────────────┬───────────────────────┤
│ getUserMedia   │ RTCPeerConnection  │ RTCDataChannel        │
│ (미디어 캡처) │ (P2P 연결)         │ (데이터 전송)         │
└────────────────┴────────────────────┴───────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     내부 구성요소                           │
├─────────────────┬───────────────────┬───────────────────────┤
│ ICE/STUN/TURN   │ DTLS-SRTP         │ 코덱                  │
│ (연결 설정)     │ (암호화)          │ (VP8, H.264, Opus)   │
└─────────────────┴───────────────────┴───────────────────────┘
```

---

## getUserMedia: 미디어 캡처

사용자의 카메라와 마이크에 접근하는 API입니다.

<br>

```javascript
// 카메라와 마이크 접근
const stream = await navigator.mediaDevices.getUserMedia({
  video: {
    width: { ideal: 1280 },
    height: { ideal: 720 },
    frameRate: { max: 30 }
  },
  audio: {
    echoCancellation: true,
    noiseSuppression: true
  }
});

// 미디어 스트림을 video 엘리먼트에 연결
document.getElementById('localVideo').srcObject = stream;
```

<br>

사용자 권한이 필요하며, 보안상의 이유로 HTTPS 환경에서만 동작합니다 (localhost는 예외).

---

## RTCPeerConnection: P2P 연결

두 브라우저 간의 P2P 연결을 설정하고 관리합니다.

<br>

```javascript
const configuration = {
  iceServers: [
    { urls: 'stun:stun.example.com:3478' },
    {
      urls: 'turn:turn.example.com:3478',
      username: 'user',
      credential: 'password'
    }
  ]
};

const peerConnection = new RTCPeerConnection(configuration);

// 로컬 스트림 추가
stream.getTracks().forEach(track => {
  peerConnection.addTrack(track, stream);
});

// 원격 스트림 수신
peerConnection.ontrack = (event) => {
  document.getElementById('remoteVideo').srcObject = event.streams[0];
};
```

---

## RTCDataChannel: 데이터 전송

P2P 연결을 통해 임의의 데이터를 전송할 수 있습니다.

<br>

```javascript
// 데이터 채널 생성
const dataChannel = peerConnection.createDataChannel('chat', {
  ordered: true,           // 순서 보장
  maxRetransmits: 3        // 최대 재전송 횟수
});

dataChannel.onopen = () => {
  dataChannel.send('Hello!');
};

dataChannel.onmessage = (event) => {
  console.log('Received:', event.data);
};
```

<br>

SCTP(Stream Control Transmission Protocol) 위에서 동작하며, 신뢰성 있는 전송과 비신뢰 전송을 모두 지원합니다.

---

## 시그널링: WebRTC가 정의하지 않는 것

WebRTC는 **시그널링 방법을 정의하지 않습니다**.

시그널링이란 P2P 연결을 설정하기 전에 필요한 메타데이터를 교환하는 과정입니다.

<br>

시그널링에서 교환하는 정보:
- 세션 설정 정보 교환
- SDP(Session Description Protocol) 교환
- ICE 후보 교환

<br>

```
Alice                  시그널링 서버              Bob
  │                         │                      │
  │ ─── SDP Offer ────────► │ ─── SDP Offer ────► │
  │                         │                      │
  │ ◄─── SDP Answer ─────── │ ◄── SDP Answer ──── │
  │                         │                      │
  │ ─── ICE Candidate ────► │ ─── ICE Candidate ─►│
  │ ◄─── ICE Candidate ──── │ ◄── ICE Candidate ──│
  │                         │                      │

시그널링 서버 구현:
- WebSocket
- HTTP 폴링
- 다른 메시지 시스템
```

<br>

따라서 개발자는 WebSocket, HTTP 폴링 등의 방식으로 시그널링 서버를 직접 구현해야 합니다.

---

## SDP (Session Description Protocol)

**SDP**는 미디어 세션의 속성을 설명하는 텍스트 기반 형식입니다.

<br>

```
v=0
o=- 7614219274584779017 2 IN IP4 127.0.0.1
s=-
t=0 0
a=group:BUNDLE 0 1
a=msid-semantic: WMS stream

m=audio 9 UDP/TLS/RTP/SAVPF 111
c=IN IP4 0.0.0.0
a=rtcp:9 IN IP4 0.0.0.0
a=ice-ufrag:abcd
a=ice-pwd:1234567890abcdef
a=fingerprint:sha-256 AB:CD:EF:...
a=setup:actpass
a=mid:0
a=rtpmap:111 opus/48000/2
a=fmtp:111 minptime=10;useinbandfec=1
a=rtcp-fb:111 transport-cc

m=video 9 UDP/TLS/RTP/SAVPF 96
c=IN IP4 0.0.0.0
a=rtcp:9 IN IP4 0.0.0.0
a=mid:1
a=rtpmap:96 VP8/90000
a=rtcp-fb:96 ccm fir
a=rtcp-fb:96 nack
```

<br>

SDP에 포함되는 정보:
- 미디어 타입 (audio, video)
- 코덱 정보 (Opus, VP8 등)
- ICE 인증 정보
- DTLS 핑거프린트
- 대역폭 제한

---

## Offer/Answer 모델

```javascript
// Alice (Offerer)
const offer = await peerConnection.createOffer();
await peerConnection.setLocalDescription(offer);

// Alice → 시그널링 → Bob: offer 전송

// Bob (Answerer)
await peerConnection.setRemoteDescription(offer);
const answer = await peerConnection.createAnswer();
await peerConnection.setLocalDescription(answer);

// Bob → 시그널링 → Alice: answer 전송

// Alice
await peerConnection.setRemoteDescription(answer);
```

<br>

```
상태 전이:
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  stable → have-local-offer → stable                       │
│     │                           ▲                         │
│     │    setLocalDescription    │                         │
│     │    (offer)                │ setRemoteDescription    │
│     │                           │ (answer)                │
│     │                           │                         │
│     ▼                           │                         │
│  have-remote-offer ─────────────┘                         │
│     setLocalDescription(answer)                           │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## ICE와 연결 설정

[NAT 트래버설](/dev/network/NATFirewall-3/)에서 ICE를 설명했듯이, WebRTC는 ICE를 사용하여 최적의 연결 경로를 찾습니다.

<br>

### ICE 후보 수집

```javascript
peerConnection.onicecandidate = (event) => {
  if (event.candidate) {
    // 시그널링 서버를 통해 상대방에게 전송
    signalingServer.send({
      type: 'candidate',
      candidate: event.candidate
    });
  }
};
```

<br>

후보 유형:
- **host**: 로컬 IP
- **srflx**: STUN으로 발견한 공인 IP
- **relay**: TURN 서버 주소

<br>

### Trickle ICE

ICE 후보를 수집하면서 **동시에** 연결을 시도하는 기법입니다.

<br>

```
기존 방식:
모든 후보 수집 완료 → SDP 전송 → 연결 시도

Trickle ICE:
SDP 전송 (일부 후보) → 추가 후보 전송 → 동시에 연결 시도
                                        (더 빠름)
```

---

## DTLS-SRTP: 미디어 암호화

WebRTC는 보안을 위해 **모든 미디어를 암호화**합니다.

<br>

### DTLS (Datagram TLS)

UDP 위에서 동작하는 TLS로, 키 교환에 사용됩니다.

<br>

```
DTLS 핸드셰이크:
┌─────────────┐                    ┌─────────────┐
│   Peer A    │                    │   Peer B    │
└──────┬──────┘                    └──────┬──────┘
       │                                  │
       │ ── ClientHello ───────────────► │
       │                                  │
       │ ◄─ ServerHello, Certificate ─── │
       │                                  │
       │ ── Certificate, KeyExchange ──► │
       │                                  │
       │ ◄─ Finished ─────────────────── │
       │                                  │
```

<br>

SDP의 **fingerprint**로 인증서를 검증하여 중간자 공격을 방지합니다.

<br>

### SRTP (Secure RTP)

DTLS로 교환된 키를 사용하여 RTP 패킷을 암호화합니다.

<br>

```
RTP 패킷                    SRTP 패킷
┌────────────┐             ┌────────────┐
│ RTP 헤더   │             │ RTP 헤더   │
├────────────┤             ├────────────┤
│ 페이로드   │  암호화 →   │ 암호화된   │
│ (평문)     │             │ 페이로드   │
└────────────┘             ├────────────┤
                           │ Auth Tag   │
                           └────────────┘
```

---

## WebRTC 연결 과정 요약

```
┌─────────────────────────────────────────────────────────────┐
│                    WebRTC 연결 단계                         │
│                                                             │
│  1. getUserMedia()로 미디어 캡처                            │
│                      ↓                                      │
│  2. RTCPeerConnection 생성                                  │
│                      ↓                                      │
│  3. createOffer() / setLocalDescription()                  │
│                      ↓                                      │
│  4. 시그널링으로 Offer 전송                                 │
│                      ↓                                      │
│  5. 상대방: setRemoteDescription() / createAnswer()        │
│                      ↓                                      │
│  6. 시그널링으로 Answer 전송                                │
│                      ↓                                      │
│  7. ICE 후보 교환                                           │
│                      ↓                                      │
│  8. DTLS 핸드셰이크                                         │
│                      ↓                                      │
│  9. SRTP 미디어 전송 시작                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 정리: 복잡하지만 강력하다

WebRTC는 많은 기술을 통합합니다:

<br>

- **ICE/STUN/TURN**: NAT 트래버설
- **DTLS**: 키 교환
- **SRTP**: 미디어 암호화
- **RTP/RTCP**: 미디어 전송
- **SDP**: 세션 협상

<br>

이러한 복잡성은 브라우저 API가 추상화하므로, 개발자는 상대적으로 간단한 API만으로 실시간 통신을 구현할 수 있습니다.

<br>

[Part 3](/dev/network/RealTimeCommunication-3/)에서는 네트워크 변화에 어떻게 적응하는지 살펴봅니다.

---

**관련 글**
- [NAT와 방화벽 (3) - NAT 트래버설과 P2P 통신](/dev/network/NATFirewall-3/)
- [실시간 통신 (1) - RTP와 실시간 전송](/dev/network/RealTimeCommunication-1/)
- [실시간 통신 (3) - 품질 관리와 적응](/dev/network/RealTimeCommunication-3/)
- [네트워크 보안의 원리 (2) - TLS와 인증서 체계](/dev/network/NetworkSecurity-2/)
