---
layout: single
title: "네트워크 성능과 최적화 (2) - TCP 혼잡 제어 심화 - soo:bak"
date: "2026-01-20 22:31:14 +0900"
description: 혼잡 붕괴, Slow Start, AIMD, Reno, CUBIC, Vegas, BBR, 혼잡 제어 알고리즘 비교를 설명합니다.
tags:
  - 네트워크
  - TCP
  - 혼잡제어
  - CUBIC
  - BBR
  - 성능
---

## 혼잡 제어 알고리즘은 어떻게 발전했는가

[Part 1](/dev/network/NetworkPerformance-1/)에서 지연의 구성 요소를 살펴보았습니다.

큐잉 지연은 네트워크 혼잡 시 급격히 증가하며, TCP의 **혼잡 제어(Congestion Control)**가 이 문제를 다룹니다.

---

## 혼잡 붕괴 (Congestion Collapse)

### 1986년 인터넷 위기

1986년, 인터넷에 심각한 문제가 발생했습니다.

<br>

LBL(Lawrence Berkeley Laboratory)과 UC Berkeley 사이의 링크:
- 용량: 32 Kbps
- 실제 처리량: **40 bps** (1000배 감소!)

<br>

원인: **혼잡 붕괴(Congestion Collapse)**

<br>

```
혼잡 붕괴의 악순환:
1. 네트워크 혼잡 → 패킷 손실
2. 패킷 손실 → 재전송
3. 재전송 → 더 많은 트래픽
4. 더 많은 트래픽 → 더 심한 혼잡
5. 반복...
```

<br>

### Jacobson의 해결책

Van Jacobson이 1988년 혼잡 제어 알고리즘을 발표했습니다.

"Congestion Avoidance and Control" 논문.

<br>

이 알고리즘이 현대 TCP 혼잡 제어의 토대입니다.

---

## 전통적 혼잡 제어

### Slow Start

연결 시작 시 네트워크 용량을 **탐색**합니다.

<br>

```
cwnd: 혼잡 윈도우 (Congestion Window)

시작: cwnd = 1 MSS (Maximum Segment Size)
ACK 수신마다: cwnd = cwnd + 1 MSS

RTT 1: 1 패킷 전송 → 1 ACK → cwnd = 2
RTT 2: 2 패킷 전송 → 2 ACK → cwnd = 4
RTT 3: 4 패킷 전송 → 4 ACK → cwnd = 8
...
```

<br>

**지수적 증가**입니다.

"Slow" Start라는 이름이지만 실제로는 빠르게 증가합니다.

<br>

```
cwnd
 │              ssthresh
 │                 │
 │                 │    ┌─ Congestion Avoidance
 │                 │   /   (선형 증가)
 │                 │  /
 │                 │ /
 │            ┌───┼/
 │           /    │
 │          /     │
 │         /      │
 │        / Slow Start
 │       /  (지수적 증가)
 │______/
 └────────────────────── 시간
```

<br>

**ssthresh(Slow Start Threshold)**에 도달하면 Congestion Avoidance로 전환합니다.

<br>

### Congestion Avoidance

ssthresh 이후에는 **선형 증가**합니다.

<br>

```
RTT마다: cwnd = cwnd + 1/cwnd (약 1 MSS/RTT)
```

<br>

천천히 증가하면서 혼잡을 조심합니다.

<br>

### AIMD (Additive Increase, Multiplicative Decrease)

- **Additive Increase**: 혼잡이 없으면 선형 증가
- **Multiplicative Decrease**: 패킷 손실 시 절반으로 감소

<br>

```
cwnd
 │
 │    /\        /\        /\
 │   /  \      /  \      /  \
 │  /    \    /    \    /    \
 │ /      \  /      \  /      \
 │/        \/        \/        \
 └─────────────────────────────── 시간
          손실    손실    손실
```

<br>

톱니 모양의 패턴이 특징입니다.

---

## 손실 기반 알고리즘

### TCP Reno

가장 전통적인 혼잡 제어입니다.

<br>

**Fast Retransmit**:
- 3개의 중복 ACK 수신 시 즉시 재전송
- 타임아웃을 기다리지 않음

<br>

**Fast Recovery**:
- 3 중복 ACK: cwnd = cwnd/2, ssthresh = cwnd
- Slow Start로 돌아가지 않고 Congestion Avoidance 유지

<br>

### TCP NewReno

Reno의 개선 버전으로, 여러 패킷 손실 시 더 나은 복구 성능을 보여줍니다.

<br>

### CUBIC (Linux 기본)

Linux의 기본 혼잡 제어 알고리즘입니다.

<br>

CUBIC의 아이디어:
- 윈도우 크기를 **3차 함수(cubic function)**로 조절
- 손실 직전 윈도우 크기를 목표로

<br>

```
W(t) = C(t - K)³ + Wmax

Wmax: 손실 직전 윈도우
K: 원점으로부터의 시간
C: 상수
```

<br>

```
cwnd
 │            Wmax
 │         ──────────────
 │        /              \
 │       /                \
 │      /                  \
 │     │                    │
 │     │                    │
 │    /                      \
 │   │                        │
 │  /                          \
 │_/                            \_
 └────────────────────────────────── 시간
             손실 발생
```

<br>

특징:
- 손실 전 윈도우에 빠르게 접근
- 그 근처에서 천천히 탐색
- 고대역폭 환경에 적합

---

## 손실 기반의 한계

**"손실 = 혼잡"** 가정의 문제:

<br>

1. **버퍼가 가득 찬 후에야** 손실 발생
   - 이미 큰 지연이 발생한 상태

<br>

2. **무선 환경**에서 손실은 혼잡 때문이 아닐 수 있음
   - 전파 간섭, 신호 감쇠
   - 불필요한 속도 감소

<br>

3. **버퍼블로트**
   - 큰 버퍼 = 늦은 손실 감지 = 큰 지연

---

## 지연 기반 알고리즘

### TCP Vegas

RTT 변화를 혼잡의 신호로 사용합니다.

<br>

아이디어:
- 혼잡이 없으면 RTT가 일정 (BaseRTT)
- 큐잉이 시작되면 RTT 증가
- **RTT 증가 = 혼잡 시작** (손실 전에 감지!)

<br>

```
Expected = cwnd / BaseRTT
Actual = cwnd / RTT

Diff = Expected - Actual

Diff > β: cwnd 감소
Diff < α: cwnd 증가
α < Diff < β: 유지
```

<br>

### Vegas의 문제

손실 기반 알고리즘과 **공존하기 어렵습니다**.

<br>

```
Vegas vs CUBIC 경쟁:
- Vegas: RTT 증가 감지 → 속도 줄임
- CUBIC: 아직 손실 없음 → 속도 유지/증가
- 결과: CUBIC이 대역폭 대부분 차지
```

<br>

보수적인 Vegas가 손해를 봅니다.

---

## BBR (Bottleneck Bandwidth and RTT)

Google이 2016년에 발표한 혼잡 제어 알고리즘입니다.

<br>

### BBR의 접근

손실에 반응하지 않고, 대신 **병목 대역폭**과 **최소 RTT**를 직접 측정합니다.

<br>

```
목표: BDP에 맞는 전송률 유지

Delivery Rate = 전송된 데이터 / ACK 간격
BtlBw = max(Delivery Rate)  # 병목 대역폭
RTprop = min(RTT)           # 최소 RTT (전파 지연)

최적 cwnd ≈ BtlBw × RTprop
```

<br>

### BBR의 동작 단계

```
┌─────────────────────────────────────────────────────────────┐
│                        BBR 상태 기계                        │
│                                                             │
│   ┌──────────┐      ┌──────────┐      ┌──────────┐         │
│   │ STARTUP  │ ───► │  DRAIN   │ ───► │ PROBE_BW │         │
│   │ (탐색)   │      │ (배수)   │      │ (유지)   │         │
│   └──────────┘      └──────────┘      └──────────┘         │
│                                              │              │
│                                              ▼              │
│                                        ┌──────────┐         │
│                                        │PROBE_RTT │         │
│                                        │(RTT 측정)│         │
│                                        └──────────┘         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

<br>

1. **STARTUP**: 대역폭 빠르게 탐색 (지수 증가)
2. **DRAIN**: 쌓인 큐 비우기
3. **PROBE_BW**: 대역폭 유지하며 작은 변동으로 탐색
4. **PROBE_RTT**: 주기적으로 RTT 재측정

<br>

### BBR의 장단점

**장점**:
- 버퍼블로트 방지 (큐를 채우지 않음)
- 손실에 덜 민감
- 위성/장거리 링크에서 우수한 성능

<br>

**단점**:
- CUBIC과 공존 시 불공정할 수 있음
- 얕은 버퍼에서 문제 가능
- 아직 발전 중 (BBRv2, BBRv3)

---

## 혼잡 제어 선택

### 시나리오별 추천

**데이터센터 내부**:
- 낮은 RTT, 낮은 손실
- CUBIC 또는 DCTCP

<br>

**장거리/위성**:
- 높은 RTT, 큰 BDP
- BBR 또는 Hybla

<br>

**모바일/무선**:
- 가변 손실, 가변 대역폭
- BBR (손실에 덜 민감)

<br>

**일반 인터넷**:
- CUBIC (기본값으로 무난)
- BBR (실험적)

<br>

### Linux에서 확인/변경

```bash
# 현재 알고리즘 확인
cat /proc/sys/net/ipv4/tcp_congestion_control
# cubic

# 사용 가능한 알고리즘
cat /proc/sys/net/ipv4/tcp_available_congestion_control
# reno cubic

# BBR 활성화
sudo modprobe tcp_bbr
echo "bbr" | sudo tee /proc/sys/net/ipv4/tcp_congestion_control
```

---

## 정리: 완벽한 알고리즘은 없다

혼잡 제어의 발전:

<br>

| 세대 | 알고리즘 | 접근 방식 | 특징 |
|-----|---------|----------|-----|
| 1세대 | Tahoe, Reno | 손실 기반 | 단순, 느린 복구 |
| 2세대 | NewReno, CUBIC | 개선된 손실 기반 | 빠른 복구, 고대역폭 |
| 3세대 | Vegas | 지연 기반 | 버퍼블로트 방지, 공존 문제 |
| 4세대 | BBR | 모델 기반 | 대역폭/RTT 측정, 실험적 |

<br>

각 알고리즘은 특정 가정과 트레이드오프를 갖고 있으며, 모든 상황에 완벽한 알고리즘은 없습니다.

<br>

[Part 3](/dev/network/NetworkPerformance-3/)에서는 애플리케이션 레벨에서의 네트워크 최적화를 다룹니다.

---

**관련 글**
- [소켓과 전송 계층 (2) - TCP의 연결 관리와 신뢰성](/dev/network/SocketTransport-2/)
- [네트워크 성능과 최적화 (1) - 지연 시간의 구성 요소](/dev/network/NetworkPerformance-1/)
- [네트워크 성능과 최적화 (3) - 애플리케이션 레벨 최적화](/dev/network/NetworkPerformance-3/)
