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

[Part 1](/dev/network/RealTimeCommunication-1/)에서 RTP가 실시간 미디어를 전송하는 원리를 살펴보았습니다.

RTP는 미디어 전송에 특화된 프로토콜이지만, 이것만으로는 실시간 통신 애플리케이션을 만들 수 없습니다.

두 사용자가 어떻게 서로를 찾고, 방화벽 뒤의 상대방과 어떻게 직접 연결하며, 미디어 스트림은 어떻게 암호화할 것인지 — 실제 애플리케이션에는 RTP 외에도 여러 프로토콜이 더 필요합니다.

**WebRTC(Web Real-Time Communication)**는 이 프로토콜들과 브라우저 API를 하나로 묶은 표준입니다. 플러그인 없이 브라우저만으로 실시간 통신을 구현할 수 있게 합니다.

---

## WebRTC의 탄생

2011년, Google이 GIPS(Global IP Solutions) 인수로 확보한 미디어 엔진을 기반으로 WebRTC 프로젝트를 오픈소스로 공개했습니다. 당시 브라우저에서 실시간 통신을 하려면 Flash나 Silverlight 같은 플러그인이 필수였습니다. 이는 보안 취약점과 성능 문제를 수반했고, 모바일 환경에서는 아예 동작하지 않는 경우도 많았습니다.

Google은 이 문제를 브라우저 자체의 네이티브 기능으로 해결하고자 했습니다. 목표는 플러그인 없이 브라우저 API만으로 P2P 실시간 통신을 구현하는 것이었으며, 2021년에 W3C와 IETF 표준화가 완료되었습니다. 현재 모든 주요 브라우저에서 지원됩니다.

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
│                     내부 프로토콜                            │
├──────────────┬────────────┬────────────┬────────────────────┤
│ ICE/STUN/TURN│ DTLS-SRTP  │ RTP/RTCP   │ SCTP              │
│ (연결 설정)  │ (암호화)   │ (미디어)   │ (데이터 채널)     │
├──────────────┴────────────┴────────────┴────────────────────┤
│              코덱: VP8, H.264, Opus                         │
└─────────────────────────────────────────────────────────────┘
```

---

## getUserMedia: 미디어 캡처

앞에서 WebRTC의 탄생 배경과 구성 요소를 살펴봤습니다. 이제 각 API가 어떻게 동작하는지 구체적으로 살펴보겠습니다. WebRTC로 화상 통화를 하려면 먼저 내 카메라와 마이크의 데이터를 가져와야 합니다. getUserMedia는 사용자의 카메라와 마이크에 접근하는 API입니다.

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

이 코드를 실행하면 브라우저가 사용자에게 카메라와 마이크 접근 권한을 요청하고, 승인 시 MediaStream 객체를 반환합니다.

반환된 스트림을 video 엘리먼트에 연결하면 로컬 화면에 자신의 모습이 표시됩니다. 사용자 권한이 필요하며, 보안상의 이유로 HTTPS 환경에서만 동작합니다 (localhost는 예외).

이는 악의적인 웹사이트가 무단으로 사용자의 카메라나 마이크에 접근하는 것을 방지하기 위한 브라우저의 보안 정책입니다.

---

## RTCPeerConnection: P2P 연결

getUserMedia로 미디어를 캡처했다면, 이제 상대방에게 전송해야 합니다. RTCPeerConnection은 두 브라우저 간의 P2P 연결을 설정하고 관리합니다.

<br>

다음 코드는 RTCPeerConnection 객체를 생성하고, 로컬 미디어 스트림을 추가하며, 상대방으로부터 수신한 스트림을 화면에 표시하는 과정을 보여줍니다.

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

<br>

configuration 객체에서 STUN/TURN 서버를 지정하면, RTCPeerConnection은 이를 사용하여 NAT 뒤의 상대방과도 연결할 수 있습니다. ontrack 이벤트 핸들러는 상대방의 미디어 스트림이 도착할 때 자동으로 호출되어 화면에 표시합니다.

---

## RTCDataChannel: 데이터 전송

WebRTC는 미디어뿐 아니라 일반 데이터도 전송할 수 있습니다. 화상 회의 중 채팅 메시지를 보내거나, 파일을 공유하거나, 게임 상태를 동기화할 때 RTCDataChannel을 사용합니다. P2P 연결을 통해 임의의 데이터를 전송할 수 있습니다.

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

이 코드는 채팅 메시지를 주고받을 수 있는 데이터 채널을 생성합니다. 채널이 열리면 'Hello!' 메시지를 전송하고, 상대방이 보낸 메시지는 onmessage 핸들러로 수신합니다.

<br>

내부적으로는 SCTP(Stream Control Transmission Protocol) 위에서 동작합니다. TCP는 바이트 스트림이므로 보낸 데이터가 합쳐져 도착할 수 있고, 어디서 끊어야 할지 애플리케이션이 직접 판단해야 합니다. 반면 UDP는 보낸 메시지 단위를 그대로 보존하지만, 손실 시 재전송하지 않습니다.

SCTP는 양쪽의 장점을 결합하여 TCP처럼 손실 시 재전송하면서도, UDP처럼 메시지 단위를 그대로 보존하여 전달합니다.

RTCDataChannel은 이를 활용하여 신뢰성 있는 순서 보장 전송(ordered: true)과 빠른 비신뢰 전송(ordered: false) 중 선택할 수 있습니다.

---

## 시그널링: WebRTC가 정의하지 않는 것

앞에서 미디어 캡처와 P2P 연결, 데이터 전송 API를 살펴봤습니다. 두 브라우저가 P2P로 연결되려면, 서로의 미디어 능력(코덱, 해상도 등)과 네트워크 주소를 먼저 알아야 합니다. 이 메타데이터를 교환하는 과정이 **시그널링**입니다.

WebRTC는 시그널링을 의도적으로 표준화하지 않았습니다. 애플리케이션마다 요구사항이 다르기 때문입니다. 채팅 앱은 WebSocket을, IoT 기기는 MQTT를, 게임은 커스텀 프로토콜을 사용할 수 있습니다. 시그널링에서 교환하는 핵심 정보는 SDP(Session Description Protocol)와 ICE 후보입니다.

<br>

```
A                      시그널링 서버              B
  │                         │                      │
  │ ─── SDP Offer ────────► │ ─── SDP Offer ────► │
  │                         │                      │
  │ ◄─── SDP Answer ─────── │ ◄── SDP Answer ──── │
  │                         │                      │
  │ ─── ICE Candidate ────► │ ─── ICE Candidate ─►│
  │ ◄─── ICE Candidate ──── │ ◄── ICE Candidate ──│
```

개발자는 시그널링 서버를 직접 구현해야 합니다. 시그널링은 초기 연결 설정에만 사용되며, P2P 연결이 수립되면 이후 미디어는 시그널링 서버를 거치지 않고 직접 전송됩니다.

---

## SDP (Session Description Protocol)

시그널링 과정에서 교환되는 핵심 정보가 SDP입니다. SDP는 미디어 세션의 속성을 텍스트로 기술하는 형식입니다. 실제 SDP의 주요 필드를 보면 어떤 정보가 오가는지 알 수 있습니다.

```
m=audio 9 UDP/TLS/RTP/SAVPF 111   ← 오디오 미디어, 페이로드 타입 111
a=rtpmap:111 opus/48000/2          ← 코덱: Opus, 48kHz, 스테레오
a=ice-ufrag:abcd                   ← ICE 인증 정보
a=fingerprint:sha-256 AB:CD:EF:...  ← DTLS 인증서 해시

m=video 9 UDP/TLS/RTP/SAVPF 96    ← 비디오 미디어, 페이로드 타입 96
a=rtpmap:96 VP8/90000              ← 코덱: VP8, 90kHz 클럭
a=rtcp-fb:96 nack                  ← 패킷 손실 시 재전송 요청 지원
```

Offer 측이 자신이 지원하는 코덱과 설정을 SDP에 나열하면, Answer 측이 그중 자신도 지원하는 항목을 선택하여 응답합니다.

---

## Offer/Answer 모델

SDP가 미디어 세션 정보를 담는 형식이라면, Offer/Answer는 이를 교환하는 절차입니다. 두 브라우저가 서로 다른 코덱을 지원하거나, 네트워크 환경이 다를 수 있습니다. Offer/Answer 모델은 이러한 차이를 협상하여 양쪽이 모두 지원하는 설정을 찾습니다.

다음은 A와 B가 Offer와 Answer를 교환하여 P2P 연결을 협상하는 코드 흐름입니다.

<br>

```javascript
// A (Offerer)
const offer = await peerConnection.createOffer();
await peerConnection.setLocalDescription(offer);

// A → 시그널링 → B: offer 전송

// B (Answerer)
await peerConnection.setRemoteDescription(offer);
const answer = await peerConnection.createAnswer();
await peerConnection.setLocalDescription(answer);

// B → 시그널링 → A: answer 전송

// A
await peerConnection.setRemoteDescription(answer);
```

이 과정을 거치면 양쪽의 PeerConnection 객체가 상대방의 미디어 능력과 네트워크 설정을 알게 되고, ICE 후보 교환을 통해 실제 연결이 수립됩니다.

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

Offer/Answer로 미디어 협상은 끝났지만, 실제로 어떤 네트워크 경로로 연결할지는 아직 정해지지 않았습니다. 대부분의 사용자는 NAT나 방화벽 뒤에 있어 공인 IP를 직접 노출하지 않습니다.

WebRTC는 **ICE(Interactive Connectivity Establishment)**를 사용하여 이 문제를 해결합니다([NAT와 방화벽 (3)](/dev/network/NATFirewall-3/)에서 ICE의 원리를 다룬 바 있습니다). ICE는 가능한 모든 네트워크 경로를 후보(candidate)로 수집한 뒤, 우선순위에 따라 연결을 시도합니다.

### ICE 후보 수집

RTCPeerConnection은 ICE 후보를 발견할 때마다 onicecandidate 이벤트를 발생시킵니다. 이 후보들을 시그널링 서버를 통해 상대방에게 전달해야 합니다.

<br>

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

새로운 후보가 발견될 때마다 이벤트 핸들러가 호출되고, 모든 후보 수집이 끝나면 event.candidate가 null이 됩니다. 상대방은 받은 후보를 addIceCandidate()로 자신의 PeerConnection에 추가합니다.

ICE가 수집하는 후보는 세 종류입니다.

| 후보 유형 | 조건 | 경로 |
|---|---|---|
| host | 직접 연결 가능 | 로컬 IP |
| srflx | NAT 뒤 | STUN으로 발견한 공인 IP |
| relay | 직접 연결 모두 실패 | TURN 서버 중계 |

ICE는 host → srflx → relay 순서로 시도하여, 가능한 한 직접 연결을 우선합니다.

### Trickle ICE

기존 ICE는 모든 후보를 수집한 뒤에야 연결을 시도했기 때문에, 연결 설정에 수 초가 걸렸습니다. Trickle ICE는 이 대기 시간을 줄이기 위해 후보를 수집하면서 동시에 연결을 시도하는 기법입니다. 일부 후보만 있어도 SDP를 먼저 전송하고, 나머지 후보는 발견되는 즉시 추가로 전달하여 연결 시간을 단축합니다.

```
시간 ──────────────────────────────────────►

기존 ICE:
[후보 수집 ···············] → [SDP 전송] → [연결 시도]

Trickle ICE:
[SDP 전송] → [연결 시도 ···············]
[후보 수집 ·········]  ↗ (발견 즉시 추가)
```

---

## DTLS-SRTP: 미디어 암호화

ICE를 통해 P2P 연결이 수립되었지만, 미디어를 전송하기 전에 암호화가 필요합니다. 인터넷을 통해 전송되는 패킷은 중간에 도청될 수 있으므로, WebRTC는 **미디어를 암호화한 뒤 전송**합니다.

### DTLS (Datagram TLS)

암호화에는 키 교환이 필요합니다. 기존 TLS는 TCP 전용이므로, WebRTC는 UDP 위에서 동작하는 DTLS(Datagram TLS)를 사용합니다. DTLS는 TLS와 동일한 암호화 강도를 제공하면서, UDP 환경에서 발생하는 패킷 손실과 재정렬을 처리합니다.

```
┌─────────────┐                    ┌─────────────┐
│   Peer A    │                    │   Peer B    │
└──────┬──────┘                    └──────┬──────┘
       │ ── ClientHello ───────────────► │
       │ ◄─ ServerHello, Certificate ─── │
       │ ── Certificate, KeyExchange ──► │
       │ ◄─────────────── Finished ───── │
       │ ── Finished ───────────────────►│
       │         (암호화 키 공유 완료)     │
```

양쪽이 Finished를 교환하면 키 공유가 완료됩니다. 이때 SDP에 포함된 fingerprint(DTLS 인증서의 해시 값)로 인증서를 검증합니다. fingerprint는 시그널링 과정에서 미리 교환되므로, 공격자가 인증서를 위조하더라도 해시 불일치로 탐지됩니다.

### SRTP (Secure RTP)

DTLS는 키 교환에만 사용됩니다. 키 교환이 완료되면, 이후 RTP 패킷은 SRTP(Secure RTP)로 암호화하여 전송합니다. SRTP는 페이로드를 암호화하고, 헤더와 암호화된 페이로드 전체에 대한 인증 태그(Auth Tag)를 추가합니다. 헤더는 평문이지만 인증 태그가 헤더까지 포함하므로, 헤더가 변조되면 수신 측에서 탐지할 수 있습니다.

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
애플리케이션 (API)              네트워크

1. getUserMedia()
         ↓
2. RTCPeerConnection 생성
         ↓
3. createOffer()
   setLocalDescription()
         ↓
4. 시그널링으로 Offer 전송 ──────► ICE 후보 수집/교환 시작
         ↓                         (Trickle ICE: 병렬 진행)
5. 상대방: setRemoteDescription()
           createAnswer()
         ↓
6. 시그널링으로 Answer 전송
                                   ICE 연결 확립
                                        ↓
                                   DTLS 핸드셰이크
                                        ↓
                                   SRTP 미디어 전송 시작
```

---

## 마무리

이 글에서 살펴본 내용을 정리하면:

- SDP로 미디어 능력을 협상하고, ICE/STUN/TURN으로 NAT 뒤의 상대방과 연결 경로를 확보합니다.
- DTLS로 키를 교환한 뒤, SRTP로 RTP 패킷을 암호화하여 전송합니다.
- getUserMedia, RTCPeerConnection, RTCDataChannel 세 API가 이 과정을 브라우저에서 다룰 수 있게 합니다.

WebRTC는 단일 프로토콜이 아니라, 시그널링부터 암호화까지 여러 프로토콜과 API를 묶은 표준입니다. 개발자는 시그널링 서버를 직접 구현해야 하지만, 나머지 연결 설정과 미디어 전송은 브라우저가 처리합니다.

네트워크는 고정된 환경이 아닙니다. 사용자가 WiFi에서 LTE로 전환하거나, 대역폭이 갑자기 줄어들 수 있습니다. WebRTC 연결이 수립된 후에도 이러한 변화에 지속적으로 적응해야 합니다.

[Part 3](/dev/network/RealTimeCommunication-3/)에서는 네트워크 변화에 적응하는 품질 관리 메커니즘을 살펴봅니다.

<br>

---

**관련 글**
- [NAT와 방화벽 (3) - NAT 트래버설과 P2P 통신](/dev/network/NATFirewall-3/)
- [네트워크 보안의 원리 (2) - TLS와 인증서 체계](/dev/network/NetworkSecurity-2/)

**시리즈**
- [실시간 통신 (1) - RTP와 실시간 전송](/dev/network/RealTimeCommunication-1/)
- 실시간 통신 (2) - WebRTC 스택 (현재 글)
- [실시간 통신 (3) - 품질 관리와 적응](/dev/network/RealTimeCommunication-3/)
