---
layout: single
title: "컨테이너 네트워킹 (3) - Kubernetes 네트워킹 - soo:bak"
date: "2026-01-20 22:31:12 +0900"
description: Kubernetes 네트워크 모델, Pod 네트워킹, Service 추상화, Ingress, Network Policy, 서비스 메시를 설명합니다.
tags:
  - 네트워크
  - 컨테이너
  - Kubernetes
  - Service
  - Ingress
  - NetworkPolicy
---

## Kubernetes는 네트워킹을 어떻게 추상화하는가

[Part 2](/dev/network/ContainerNetwork-2/)에서 VXLAN과 CNI 플러그인을 통해 멀티호스트 컨테이너 통신이 어떻게 가능한지 살펴보았습니다.

<br>

오버레이 네트워크가 Pod 간 연결을 제공하지만, 실제 운영 환경에서는 더 많은 문제가 남아 있습니다. Pod는 생성과 삭제를 반복하며 IP 주소가 매번 바뀝니다. 클라이언트는 어떤 Pod에 요청을 보내야 할까요?

<br>

Kubernetes는 이런 저수준 기술 위에 **Service**, **Ingress**, **Network Policy**라는 추상화 계층을 제공하여, 개발자가 네트워크 세부사항을 몰라도 애플리케이션을 배포할 수 있게 합니다.

---

## Kubernetes 네트워크 모델

Kubernetes는 CNI 플러그인에게 다음 네 가지 조건을 만족시킬 것을 요구합니다. 이 조건들은 의도적으로 단순합니다. VM 환경처럼 모든 노드가 플랫 네트워크에 있는 것과 동일한 동작을 보장하여, 기존 애플리케이션을 수정 없이 컨테이너로 이전할 수 있게 합니다. NAT가 개입하지 않으므로 소스 IP 추적, 로깅, 보안 정책 적용이 직관적입니다.

<br>

1. **모든 Pod는 고유 IP 주소**를 가진다
2. **모든 Pod는 NAT 없이** 다른 모든 Pod와 통신할 수 있다
3. **모든 노드는 NAT 없이** 모든 Pod와 통신할 수 있다
4. Pod가 보는 자신의 IP는 다른 Pod가 보는 IP와 같다

<br>

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes 클러스터                      │
│                                                             │
│  노드 A (10.0.0.1)              노드 B (10.0.0.2)           │
│  ┌─────────────────┐            ┌─────────────────┐         │
│  │ Pod 1           │            │ Pod 3           │         │
│  │ 10.244.1.5      │◄──────────►│ 10.244.2.3      │         │
│  │                 │   직접     │                 │         │
│  │ Pod 2           │   통신     │ Pod 4           │         │
│  │ 10.244.1.6      │   (NAT X)  │ 10.244.2.4      │         │
│  └─────────────────┘            └─────────────────┘         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

<br>

이 모델은 포트 충돌 걱정 없이 각 Pod가 전체 포트 공간을 사용할 수 있게 하고, 컨테이너에서 VM으로의 이식성을 높이며, 네트워크 정책 설정을 단순하게 만듭니다.

---

## Pod 네트워킹

Pod 내부의 네트워킹은 어떻게 동작할까요? 이를 이해하려면 먼저 pause 컨테이너를 알아야 합니다.

### pause 컨테이너

모든 Pod에는 사용자가 직접 정의하지 않았지만 자동으로 생성되는 숨겨진 **pause 컨테이너**가 있습니다.

<br>

```
Pod
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌───────────────┐                                          │
│  │ pause         │ ← 네트워크 네임스페이스 소유             │
│  │ 컨테이너      │                                          │
│  └───────┬───────┘                                          │
│          │                                                  │
│   ┌──────┴──────────────────────┐                          │
│   │                             │                          │
│ ┌─┴──────────┐  ┌──────────────┐│                          │
│ │ 앱 컨테이너 │  │ 사이드카     ││ ← 네임스페이스 공유      │
│ │            │  │ 컨테이너     ││                          │
│ └────────────┘  └──────────────┘│                          │
│                                                             │
│  IP: 10.244.1.5                                            │
│  모든 컨테이너가 같은 IP, localhost로 통신                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

<br>

pause 컨테이너는 네트워크 네임스페이스를 생성하고 유지하는 역할을 합니다. 앱 컨테이너가 재시작되어도 네트워크가 유지되며, 매우 작아서 실질적으로 아무 작업도 하지 않습니다.

<br>

### Pod 내부 통신

같은 Pod의 컨테이너들은 네트워크 네임스페이스를 공유하므로 **localhost**로 통신할 수 있습니다. 포트만 다르게 사용하면 됩니다.

<br>

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: two-containers
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
  - name: sidecar
    image: busybox
    command: ['wget', '-O-', 'localhost:80']  # localhost로 nginx 접근
```

<br>

### Pod 간 통신

다른 Pod와는 **Pod IP**로 직접 통신합니다. CNI 플러그인이 라우팅을 처리하며, Kubernetes 네트워크 모델에 따라 NAT 없이 직접 통신합니다.

```
Pod A (10.244.1.5) → 10.244.2.3:80 → Pod B (10.244.2.3)
```

---

## Service 추상화

Pod IP를 직접 사용하면 몇 가지 문제가 있습니다. Pod는 일시적이어서 재시작되면 새 IP를 받고, 여러 Pod에 부하를 분산해야 하며, 동적으로 변하는 Pod IP를 하드코딩할 수 없습니다.

<br>

**Service**가 이 문제를 해결합니다. Service는 Pod 집합에 대한 안정적인 엔드포인트(IP와 DNS 이름)를 제공합니다.

<br>

```
┌─────────────────────────────────────────────────────────────┐
│                         Service                             │
│                    (my-service.default)                     │
│                   ClusterIP: 10.96.0.10                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
         ┌────────┐   ┌────────┐   ┌────────┐
         │ Pod 1  │   │ Pod 2  │   │ Pod 3  │
         │10.244  │   │10.244  │   │10.244  │
         │.1.5    │   │.1.6    │   │.2.3    │
         └────────┘   └────────┘   └────────┘
              ▲            ▲            ▲
              │            │            │
         label: app=myapp (셀렉터로 Pod 선택)
```

<br>

### Service 유형

Service는 네 가지 유형이 있으며, 각각 다른 접근 범위와 사용 사례를 가집니다.

#### ClusterIP (기본)

클러스터 **내부에서만** 접근 가능한 가상 IP를 생성합니다. 마이크로서비스 간 내부 통신에 적합합니다.

<br>

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ClusterIP  # 기본값
  selector:
    app: myapp
  ports:
  - port: 80        # Service 포트
    targetPort: 8080 # Pod 포트
```

<br>

#### NodePort

모든 노드의 **특정 포트**(30000-32767 범위)를 열어 외부 접근을 허용합니다. 개발 환경이나 간단한 외부 노출에 적합합니다.

<br>

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080  # 30000-32767 범위
```

<br>

```
외부 → 노드IP:30080 → Service → Pod
```

<br>

#### LoadBalancer

클라우드 환경(AWS, GCP, Azure 등)에서 외부 로드 밸런서를 자동으로 프로비저닝합니다. 프로덕션 환경에서 외부 트래픽을 받을 때 주로 사용합니다.

<br>

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
```

<br>

```
인터넷 → 클라우드 LB → NodePort → Service → Pod
```

<br>

### 어떤 Service 유형을 선택해야 할까?

Service 유형은 접근 범위가 점점 넓어지는 계층 구조를 이루고 있습니다. LoadBalancer는 내부적으로 NodePort를 생성하고, NodePort는 ClusterIP를 포함합니다. 따라서 불필요하게 넓은 접근 범위를 선택하지 않는 것이 보안상 바람직합니다.

<br>

| 사용 사례 | 권장 유형 |
|----------|----------|
| 클러스터 내 마이크로서비스 간 통신 | ClusterIP |
| 개발/테스트 환경에서 외부 접근 | NodePort |
| 프로덕션 환경 외부 노출 (L4) | LoadBalancer |
| HTTP/HTTPS 라우팅이 필요한 경우 | Ingress + ClusterIP |
| 여러 서비스를 하나의 IP로 노출 | Ingress + ClusterIP |

<br>

일반적인 패턴은 **내부 서비스에는 ClusterIP**, **외부 노출이 필요한 HTTP 서비스에는 Ingress**, **비HTTP 서비스(DB, 메시징 등)의 외부 노출에는 LoadBalancer**를 사용하는 것입니다.

---

## kube-proxy의 역할

Service는 가상의 개념이며, 실제 트래픽 라우팅은 **kube-proxy**가 담당합니다. kube-proxy는 각 노드에서 실행되면서 Service의 동작을 구현합니다.

<br>

### iptables 모드

기본 모드로, Service IP로 가는 트래픽을 iptables 규칙으로 Pod로 리다이렉트합니다.

<br>

```bash
# kube-proxy가 생성하는 iptables 규칙 (단순화)
-A KUBE-SERVICES -d 10.96.0.10/32 -p tcp --dport 80 -j KUBE-SVC-XXX
-A KUBE-SVC-XXX -m statistic --mode random --probability 0.333 -j KUBE-SEP-AAA
-A KUBE-SVC-XXX -m statistic --mode random --probability 0.500 -j KUBE-SEP-BBB
-A KUBE-SVC-XXX -j KUBE-SEP-CCC
-A KUBE-SEP-AAA -p tcp -j DNAT --to-destination 10.244.1.5:8080
-A KUBE-SEP-BBB -p tcp -j DNAT --to-destination 10.244.1.6:8080
-A KUBE-SEP-CCC -p tcp -j DNAT --to-destination 10.244.2.3:8080
```

<br>

### IPVS 모드

수천 개의 Service가 있는 대규모 클러스터에서는 IPVS 모드가 더 나은 성능을 제공합니다.

<br>

```bash
# IPVS 가상 서버
IP Virtual Server version 1.2.1
-> 10.96.0.10:80 rr
  -> 10.244.1.5:8080    Masq    1
  -> 10.244.1.6:8080    Masq    1
  -> 10.244.2.3:8080    Masq    1
```

<br>

IPVS는 해시 테이블을 사용하여 O(1) 복잡도로 동작하며(iptables는 O(n)), round-robin, least-connection 등 다양한 로드 밸런싱 알고리즘을 지원합니다.

---

## Ingress

Service는 L4(TCP/UDP)에서 동작하여 IP와 포트 기반으로만 라우팅합니다. 반면 **Ingress**는 L7(HTTP/HTTPS) 라우팅을 제공하여 URL 경로나 호스트명 기반으로 트래픽을 분배할 수 있습니다.

<br>

```
┌─────────────────────────────────────────────────────────────┐
│                        Ingress                              │
│                                                             │
│   /api/*  → api-service                                     │
│   /web/*  → web-service                                     │
│   /*.js   → static-service                                  │
│                                                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │api-service │  │web-service │  │static-svc  │
    └────────────┘  └────────────┘  └────────────┘
```

<br>

### Ingress 리소스

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
  - host: example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
  tls:
  - hosts:
    - example.com
    secretName: tls-secret
```

<br>

### Ingress Controller

Ingress 리소스는 "이런 라우팅을 원한다"는 선언이며, 실제 라우팅은 **Ingress Controller**가 구현합니다. Kubernetes에는 기본 Ingress Controller가 없으므로 별도로 설치해야 합니다.

<br>

Ingress Controller를 선택할 때는 환경(클라우드/온프레미스), 성능 요구, 필요한 기능(WAF, 인증서 자동 관리 등)을 기준으로 판단합니다. 클라우드 환경에서는 해당 클라우드의 네이티브 컨트롤러를 사용하면 로드 밸런서와 자연스럽게 통합됩니다.

<br>

주요 Ingress Controller:
- **NGINX Ingress**: 가장 널리 사용되며 검증됨
- **Traefik**: 동적 설정과 자동 인증서 갱신에 적합
- **HAProxy Ingress**: 고성능이 필요한 환경
- **AWS ALB Ingress Controller**: AWS 환경에서 ALB와 통합

---

## Network Policy

기본적으로 Kubernetes에서 모든 Pod는 서로 제한 없이 통신할 수 있습니다. 보안을 위해 **Network Policy**로 Pod 간 트래픽을 제어할 수 있습니다.

<br>

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: web
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

<br>

이 정책은 `app: api` 레이블이 있는 Pod에 적용되며, 인바운드 트래픽은 `app: web` Pod에서 8080 포트로만, 아웃바운드 트래픽은 `app: database` Pod의 5432 포트로만 허용합니다.

<br>

### 기본 거부 정책

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}  # 모든 Pod
  policyTypes:
  - Ingress
  - Egress
```

<br>

모든 트래픽을 기본 차단하고 필요한 것만 명시적으로 허용하는 **Zero Trust** 접근법입니다. 프로덕션 환경에서는 이 기본 거부 정책을 먼저 적용하고, 각 마이크로서비스에 필요한 통신 경로만 명시적으로 열어주는 방식을 권장합니다. 이렇게 하면 서비스 하나가 침해되더라도 공격자의 횡적 이동(lateral movement)을 제한할 수 있습니다.

<br>

Network Policy는 CNI 플러그인이 지원해야 동작하며, Flannel은 지원하지 않고 Calico, Cilium 등은 지원합니다.

---

## 서비스 메시 개요

마이크로서비스가 많아지면 Service와 Network Policy만으로는 해결하기 어려운 문제들이 생깁니다. 예를 들어, 수십 개의 서비스가 서로 호출하는 환경에서 모든 통신을 mTLS로 암호화하려면 각 서비스에 인증서를 배포하고 갱신하는 과정이 필요합니다. 또한 특정 요청이 실패했을 때 어느 서비스에서 문제가 발생했는지 추적하려면 분산 트레이싱이 필요하고, 카나리 배포를 위해 트래픽의 일부만 새 버전으로 보내는 세밀한 제어도 필요합니다. 이런 기능들을 각 서비스에 직접 구현하면 비즈니스 로직과 인프라 로직이 뒤섞이게 됩니다.

<br>

**서비스 메시**가 이런 문제를 해결합니다.

<br>

### Sidecar 패턴

서비스 메시의 핵심 아이디어는 각 Pod에 **프록시 사이드카**를 주입하는 것입니다.

<br>

```
┌─────────────────────────────────────────────────────────────┐
│                           Pod                               │
│  ┌─────────────┐                     ┌─────────────┐        │
│  │ 앱 컨테이너 │ ◄──── localhost ──► │ 사이드카    │        │
│  │             │                     │ (Envoy)     │        │
│  └─────────────┘                     └──────┬──────┘        │
│                                             │               │
└─────────────────────────────────────────────┼───────────────┘
                                              │
                                         mTLS │
                                              │
┌─────────────────────────────────────────────┼───────────────┐
│                           Pod               │               │
│  ┌─────────────┐                     ┌──────┴──────┐        │
│  │ 앱 컨테이너 │ ◄──── localhost ──► │ 사이드카    │        │
│  └─────────────┘                     │ (Envoy)     │        │
│                                      └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

<br>

앱은 localhost로 통신한다고 생각하지만, 실제로는 사이드카 프록시가 모든 네트워크 처리를 담당합니다. 이를 통해 애플리케이션 코드 수정 없이 mTLS, 관찰성, 트래픽 제어 기능을 추가할 수 있습니다.

<br>

### 주요 서비스 메시

**Istio**는 Google, IBM, Lyft가 개발했으며 Envoy 프록시를 사용합니다. 풍부한 기능을 제공하지만 그만큼 복잡성도 높습니다.

<br>

**Linkerd**는 CNCF 프로젝트로, Rust로 작성된 경량 프록시를 사용합니다. 단순함과 낮은 리소스 사용이 특징입니다.

---

## 마무리

Kubernetes는 여러 계층의 추상화를 통해 컨테이너 네트워킹의 복잡성을 숨깁니다.

<br>

```
         높음
          │
          │   Service Mesh (Istio, Linkerd)
          │        ↓
          │   Ingress (L7 라우팅)
          │        ↓
          │   Service (L4 로드밸런싱, 서비스 디스커버리)
          │        ↓
          │   Network Policy (트래픽 제어)
          │        ↓
          │   Pod 네트워킹 (CNI)
          │        ↓
          │   오버레이 네트워크 (VXLAN 등)
          │        ↓
낮음      │   Linux 네트워킹 (veth, bridge, iptables)
```

<br>

각 계층은 아래 계층의 복잡성을 숨기므로, 애플리케이션 개발자는 Service와 Ingress 수준만 이해하면 됩니다. 반면 플랫폼 엔지니어나 인프라 담당자는 CNI, 오버레이 네트워크 등 하위 계층까지 이해해야 문제를 진단하고 해결할 수 있습니다.

<br>

---

**관련 글**
- [로드 밸런싱과 고가용성 (1) - 로드 밸런싱의 원리](/dev/network/LoadBalancing-1/)
- [네트워크 보안의 원리 (2) - TLS와 인증서 체계](/dev/network/NetworkSecurity-2/)

**시리즈**
- [컨테이너 네트워킹 (1) - 컨테이너 네트워크 기초](/dev/network/ContainerNetwork-1/)
- [컨테이너 네트워킹 (2) - 오버레이 네트워크](/dev/network/ContainerNetwork-2/)
- 컨테이너 네트워킹 (3) - Kubernetes 네트워킹 (현재 글)
