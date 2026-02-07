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

[Part 1](/dev/network/RealTimeCommunication-1/)에서 RTP가 실시간 미디어를 전송하는 원리를 살펴보았습니다. RTP는 미디어 전송에 특화된 프로토콜이지만, 이것만으로는 실시간 통신 애플리케이션을 만들 수 없습니다. 두 사용자가 어떻게 서로를 찾고, 방화벽 뒤의 상대방과 어떻게 직접 연결하며, 미디어 스트림은 어떻게 암호화할 것인지 — 실제 애플리케이션에는 RTP 위에 여러 계층의 프로토콜이 더 필요합니다. **WebRTC(Web Real-Time Communication)**는 이 모든 것을 브라우저에서 **플러그인 없이** 해결합니다.

---

## WebRTC의 탄생

2011년, Google이 GIPS(Global IP Solutions) 인수로 확보한 미디어 엔진을 기반으로 WebRTC 프로젝트를 오픈소스로 공개했습니다. 당시 브라우저에서 실시간 통신을 하려면 Flash나 Silverlight 같은 플러그인이 필수였습니다. 이는 보안 취약점과 성능 문제를 수반했고, 모바일 환경에서는 아예 동작하지 않는 경우도 많았습니다. Google은 이 문제를 브라우저 자체의 네이티브 기능으로 해결하고자 했습니다. 목표는 플러그인 없이 브라우저 API만으로 P2P 실시간 통신을 구현하는 것이었으며, 2021년에 W3C와 IETF 표준화가 완료되었습니다. 현재 모든 주요 브라우저에서 지원됩니다.

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

이 코드를 실행하면 브라우저가 사용자에게 카메라와 마이크 접근 권한을 요청하고, 승인 시 MediaStream 객체를 반환합니다. 반환된 스트림을 video 엘리먼트에 연결하면 로컬 화면에 자신의 모습이 표시됩니다. 사용자 권한이 필요하며, 보안상의 이유로 HTTPS 환경에서만 동작합니다 (localhost는 예외). 이는 악의적인 웹사이트가 무단으로 사용자의 카메라나 마이크에 접근하는 것을 방지하기 위한 브라우저의 보안 정책입니다.

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

내부적으로는 SCTP(Stream Control Transmission Protocol) 위에서 동작합니다. SCTP는 TCP처럼 신뢰성을 보장하면서도 UDP처럼 메시지 경계를 유지하는 전송 프로토콜입니다. RTCDataChannel은 이를 활용하여 신뢰성 있는 전송(ordered: true)과 빠른 비신뢰 전송(ordered: false) 중 선택할 수 있습니다.

---

## 시그널링: WebRTC가 정의하지 않는 것

앞에서 미디어 캡처와 P2P 연결, 데이터 전송 API를 살펴봤습니다. 그런데 WebRTC는 한 가지를 의도적으로 표준화하지 않았습니다. 바로 **시그널링**입니다. 시그널링은 P2P 연결을 설정하기 전에 필요한 메타데이터를 교환하는 과정입니다. 두 브라우저가 P2P로 연결되려면, 서로의 미디어 능력(코덱, 해상도 등)과 네트워크 주소를 먼저 알아야 합니다. WebRTC가 시그널링을 표준화하지 않은 이유는, 애플리케이션마다 요구사항이 다르기 때문입니다. 채팅 앱은 WebSocket을, IoT 기기는 MQTT를, 게임은 커스텀 프로토콜을 사용할 수 있습니다.

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

따라서 개발자는 WebSocket, HTTP 폴링 등의 방식으로 시그널링 서버를 직접 구현해야 합니다. 시그널링은 초기 연결 설정에만 사용되며, 일단 P2P 연결이 수립되면 이후 미디어 스트림은 시그널링 서버를 거치지 않고 직접 전송됩니다.

---

## SDP (Session Description Protocol)

시그널링 과정에서 교환되는 핵심 정보가 바로 SDP입니다. SDP는 미디어 세션의 속성을 설명하는 텍스트 기반 형식입니다.

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

SDP는 사람이 읽을 수 있는 텍스트 형식이지만, 실제로는 기계가 파싱하여 미디어 세션의 파라미터를 협상하는 데 사용됩니다. Offer 측이 자신이 지원하는 코덱과 설정을 나열하면, Answer 측이 그중 자신도 지원하는 항목을 선택하여 응답합니다. SDP에는 미디어 타입 (audio, video), 코덱 정보 (Opus, VP8 등), ICE 인증 정보, DTLS 핑거프린트, 대역폭 제한 등이 포함됩니다.

---

## Offer/Answer 모델

SDP가 미디어 세션 정보를 담는 형식이라면, Offer/Answer는 이를 교환하는 절차입니다. 두 브라우저가 서로 다른 코덱을 지원하거나, 네트워크 환경이 다를 수 있습니다. Offer/Answer 모델은 이러한 차이를 협상하여 양쪽이 모두 지원하는 설정을 찾습니다. 다음은 Alice와 Bob이 Offer와 Answer를 교환하여 P2P 연결을 협상하는 코드 흐름입니다.

<br>

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

Offer/Answer로 미디어 협상은 끝났지만, 실제로 어떤 네트워크 경로로 연결할지는 아직 정해지지 않았습니다. 대부분의 사용자는 NAT나 방화벽 뒤에 있어 직접 연결이 불가능하므로, [NAT 트래버설](/dev/network/NATFirewall-3/)에서 ICE를 설명했듯이, WebRTC는 ICE(Interactive Connectivity Establishment)를 사용하여 최적의 연결 경로를 찾습니다. ICE는 가능한 모든 네트워크 경로를 후보(candidate)로 수집한 뒤, 우선순위에 따라 연결을 시도합니다.

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

이벤트 핸들러는 새로운 후보가 발견될 때마다 호출되며, 모든 후보 수집이 끝나면 event.candidate가 null이 됩니다. 상대방은 받은 후보를 addIceCandidate() 메서드로 자신의 PeerConnection에 추가합니다. 직접 연결이 가능하면 host 후보(로컬 IP)를, NAT 뒤에 있으면 STUN으로 발견한 srflx 후보(공인 IP)를, 모두 실패하면 TURN 서버를 통한 relay 후보를 사용합니다.

### Trickle ICE

기존 ICE는 모든 후보를 수집한 뒤에야 연결을 시도했기 때문에, 연결 설정에 수 초가 걸렸습니다. Trickle ICE는 이 대기 시간을 줄이기 위해 후보를 수집하면서 동시에 연결을 시도하는 기법입니다. 일부 후보만 있어도 SDP를 먼저 전송하고, 나머지 후보는 발견되는 즉시 추가로 전달하여 연결 시간을 단축합니다.

```
기존 방식:
모든 후보 수집 완료 → SDP 전송 → 연결 시도

Trickle ICE:
SDP 전송 (일부 후보) → 추가 후보 전송 → 동시에 연결 시도
                                        (더 빠름)
```

---

## DTLS-SRTP: 미디어 암호화

ICE를 통해 P2P 연결이 수립되었습니다. 하지만 바로 미디어를 전송하면 안 됩니다. 인터넷을 통해 전송되는 모든 패킷은 중간에 도청될 수 있으므로, WebRTC는 보안을 위해 **모든 미디어를 암호화**합니다.

### DTLS (Datagram TLS)

WebRTC는 UDP를 사용하지만, 암호화를 위해서는 키 교환이 필요합니다. 기존 TLS는 TCP 전용이므로, UDP 위에서 동작하는 DTLS(Datagram TLS)를 사용하여 키를 안전하게 교환합니다. DTLS는 TLS와 동일한 암호화 강도를 제공하면서도 UDP의 특성에 맞게 패킷 손실과 재정렬을 처리합니다.

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

SDP에 포함된 fingerprint 값으로 인증서를 검증하여 중간자 공격을 방지합니다. fingerprint는 DTLS 인증서의 해시 값으로, 시그널링 과정에서 미리 교환되므로 공격자가 인증서를 위조하더라도 해시 불일치로 탐지됩니다.

### SRTP (Secure RTP)

DTLS로 키 교환이 완료되면, 이 키를 사용하여 실제 미디어 스트림을 암호화합니다. DTLS는 키 교환에만 사용되고, 이후 모든 RTP 패킷은 SRTP(Secure RTP)로 암호화됩니다. SRTP는 RTP 페이로드를 암호화하고 인증 태그를 추가하여 변조를 탐지합니다.

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

## 마무리

WebRTC는 많은 기술을 통합하여 브라우저에서의 실시간 통신을 가능하게 합니다:
- **ICE/STUN/TURN**: NAT 트래버설로 방화벽 뒤의 사용자와도 연결
- **DTLS**: UDP 위에서 안전한 키 교환
- **SRTP**: 미디어 암호화로 도청 방지
- **RTP/RTCP**: 실시간 미디어 전송과 품질 모니터링
- **SDP**: 미디어 능력 협상

브라우저 API가 이러한 복잡성을 추상화하므로, 개발자는 간단한 API만으로 실시간 통신을 구현할 수 있습니다. getUserMedia로 미디어를 캡처하고, RTCPeerConnection으로 P2P 연결을 설정하는 몇 줄의 코드만으로 화상 회의 애플리케이션을 만들 수 있습니다.

하지만 네트워크는 고정된 환경이 아닙니다. 사용자가 WiFi에서 LTE로 전환하거나, 대역폭이 갑자기 줄어들 수 있습니다. WebRTC는 이러한 변화에 어떻게 대응할까요?

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
