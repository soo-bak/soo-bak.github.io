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

[Part 2](/dev/network/ContainerNetwork-2/)에서 VXLAN과 CNI 플러그인을 통해 멀티호스트 컨테이너 통신이 어떻게 가능한지 살펴보았습니다. 오버레이 네트워크 덕분에 서로 다른 호스트의 컨테이너도 같은 네트워크에 있는 것처럼 통신할 수 있게 되었습니다.

하지만 "연결이 가능하다"는 것과 "운영할 수 있다"는 것은 다른 문제입니다. 초기 컨테이너 오케스트레이션 도구들은 네트워킹을 애플리케이션 개발자에게 맡겼습니다. 컨테이너의 IP를 직접 추적하고, 로드 밸런서를 수동으로 구성하며, 방화벽 규칙도 하나하나 설정해야 했습니다. 컨테이너가 재시작되면 IP가 바뀌고, 여러 컨테이너에 트래픽을 분산해야 하며, 어떤 컨테이너끼리 통신을 허용할지도 결정해야 합니다. 컨테이너가 수십 개일 때는 가능했지만, 수백, 수천 개로 늘어나면서 수동 관리는 한계에 부딪혔습니다.

2014년 Google이 공개한 Kubernetes는 이 문제에 대해 다른 접근을 택했습니다. 네트워크 구성을 명령형(imperative)이 아닌 선언형(declarative)으로 추상화한 것입니다. 저수준 네트워킹 위에 **Service**, **Ingress**, **Network Policy**라는 추상화 계층을 두어, 개발자는 "이런 상태를 원한다"는 선언만으로 서비스 간 통신, 외부 트래픽 라우팅, 접근 제어를 설정할 수 있게 했습니다.

---

## Kubernetes 네트워크 모델

Kubernetes는 컨테이너를 직접 다루지 않고, **Pod**라는 단위로 묶어서 관리합니다. 하나의 Pod에는 하나 이상의 컨테이너가 들어가며, 같은 Pod의 컨테이너들은 네트워크와 스토리지를 공유합니다. Kubernetes에서 IP 주소가 부여되는 최소 단위이기도 합니다.

Kubernetes 네트워크 모델의 목표는 단순합니다. VM 환경처럼 모든 Pod가 하나의 플랫 네트워크에 있는 것과 같은 동작을 보장하여, 기존 애플리케이션을 수정 없이 컨테이너로 옮길 수 있게 하는 것입니다. 이를 위해 CNI 플러그인에게 네 가지 조건을 요구합니다.

<br>

1. **모든 Pod는 고유 IP 주소**를 가진다
2. **모든 Pod는 NAT 없이** 다른 모든 Pod와 통신할 수 있다
3. **모든 노드는 NAT 없이** 모든 Pod와 통신할 수 있다
4. **Pod가 보는 자신의 IP**는 다른 Pod가 보는 IP와 같다

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

이 조건은 Pod 간 직접 통신에 적용됩니다. NAT가 개입하면 출발지 IP가 변환되어 원래 누가 보낸 패킷인지 알기 어려워지는데, Pod 간 통신에 NAT가 없으면 소스 IP 추적, 로깅, 보안 정책 적용이 직관적입니다. 각 Pod가 고유 IP를 가지므로 포트 충돌도 발생하지 않습니다. 다만 뒤에서 다룰 Service는 가상 IP를 Pod IP로 변환하기 위해 DNAT를 사용합니다.

---

## Pod 네트워킹

앞에서 같은 Pod의 컨테이너들은 네트워크를 공유한다고 했습니다. 이 공유는 어떻게 구현될까요?

### pause 컨테이너

모든 Pod에는 사용자가 정의하지 않아도 자동으로 생성되는 **pause 컨테이너**가 있습니다. pause 컨테이너는 네트워크 네임스페이스를 생성한 뒤 아무 작업도 수행하지 않고 대기합니다. 나머지 컨테이너들은 이 네임스페이스에 합류하여 같은 IP와 포트 공간을 공유합니다.

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
│ │ 앱 컨테이너 │  │ 보조         ││ ← 네임스페이스 공유      │
│ │            │  │ 컨테이너     ││                          │
│ └────────────┘  └──────────────┘│                          │
│                                                             │
│  IP: 10.244.1.5                                            │
│  모든 컨테이너가 같은 IP, localhost로 통신                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

<br>

pause 컨테이너가 별도로 존재하는 이유는 안정성 때문입니다. 앱 컨테이너가 비정상 종료되어 재시작되더라도, pause 컨테이너가 네임스페이스를 유지하고 있으므로 Pod의 IP와 네트워크 설정은 그대로 남아 있습니다.

### Pod 내부 통신

같은 Pod의 컨테이너들은 **localhost**로 통신합니다. 단, 포트 공간도 공유하므로 두 컨테이너가 같은 포트를 사용하면 충돌이 발생합니다.

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

다른 Pod와는 **Pod IP**로 직접 통신합니다. [Part 2](/dev/network/ContainerNetwork-2/)에서 다룬 CNI 플러그인이 라우팅을 처리합니다.

```
Pod A (10.244.1.5) → 10.244.2.3:80 → Pod B (10.244.2.3)
```

이 방식은 단순하지만, Pod IP가 영구적이지 않다는 문제가 있습니다. Pod가 재시작되면 새 IP를 받기 때문에, 클라이언트가 Pod IP를 직접 사용하면 상대방이 재시작될 때마다 주소를 다시 알아내야 합니다.

---

## Service 추상화

여기에 부하 분산 문제까지 더해집니다. 같은 역할을 하는 Pod가 여러 개 있을 때, 클라이언트가 모든 Pod IP를 알고 있어야 하고, Pod가 추가되거나 삭제될 때마다 목록을 갱신해야 합니다.

**Service**는 이 문제를 해결합니다. Pod 집합 앞에 고정된 IP와 DNS 이름을 두어, Pod가 재시작되거나 수가 바뀌어도 클라이언트는 Service 주소 하나만 알면 됩니다.

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

### Service 유형

Service는 트래픽을 어디에서 받을 것인지에 따라 유형이 나뉩니다. 클러스터 내부에서만 접근할지, 외부에서도 접근할지를 결정합니다.

#### ClusterIP (기본)

클러스터 **내부에서만** 접근 가능한 가상 IP를 생성합니다. 이 IP는 실제 네트워크 인터페이스에 할당된 것이 아니라, kube-proxy가 iptables/IPVS 규칙으로 구현하는 주소입니다. 마이크로서비스 간 내부 통신에 사용합니다.

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

ClusterIP는 클러스터 내부에서만 접근할 수 있으므로, 외부 트래픽을 받으려면 다른 방법이 필요합니다. NodePort는 ClusterIP를 기반으로 하되, 모든 노드의 **특정 포트**(30000-32767 범위)를 추가로 열어 외부에서 접근할 수 있게 합니다.

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

```
외부 → 노드IP:30080 → Service(ClusterIP) → Pod
```

#### LoadBalancer

NodePort는 외부 접근을 허용하지만, 클라이언트가 노드 IP와 높은 포트 번호를 직접 알아야 합니다. LoadBalancer는 NodePort 위에 클라우드 로드 밸런서(AWS ELB, GCP LB 등)를 자동으로 프로비저닝하여, 고정된 외부 IP 하나로 트래픽을 받을 수 있게 합니다.

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

```
인터넷 → 클라우드 LB → NodePort → Service(ClusterIP) → Pod
```

### 어떤 Service 유형을 선택해야 할까?

앞에서 살펴본 것처럼 세 유형은 ClusterIP → NodePort → LoadBalancer 순서로 쌓이는 계층 구조입니다. 접근 범위가 넓을수록 외부 노출 경로가 늘어나므로, 필요한 만큼만 노출하는 것이 보안상 바람직합니다.

| 사용 사례 | 권장 유형 |
|----------|----------|
| 클러스터 내 마이크로서비스 간 통신 | ClusterIP |
| 개발/테스트 환경에서 외부 접근 | NodePort |
| 프로덕션 비HTTP 외부 노출 (DB, 메시징 등) | LoadBalancer |
| 프로덕션 HTTP/HTTPS 외부 노출 | Ingress + ClusterIP |

일반적인 프로덕션 환경에서는 **내부 서비스에 ClusterIP**, **HTTP 서비스의 외부 노출에는 뒤에서 다루는 Ingress**를 조합합니다.

---

## kube-proxy의 역할

앞에서 ClusterIP가 kube-proxy의 규칙으로 구현된다고 했습니다. 그렇다면 이 가상 IP로 향하는 트래픽은 구체적으로 어떻게 실제 Pod에 도달할까요?

**kube-proxy**는 각 노드에서 실행되면서, Service에 연결된 Pod 목록을 감시하고 그에 맞는 라우팅 규칙을 생성합니다. 구현 방식에 따라 두 가지 모드가 있습니다.

### iptables 모드

기본 모드입니다. kube-proxy가 Service마다 iptables 규칙을 생성하여, Service IP로 가는 트래픽을 DNAT로 Pod IP로 변환합니다. 아래 규칙에서 `--probability`는 3개의 Pod에 트래픽을 균등 분배하는 부분입니다.

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

iptables 모드는 규칙을 순차적으로 탐색하므로 O(n)입니다. Service가 수천 개로 늘어나면 성능이 떨어집니다. IPVS 모드는 해시 테이블을 사용하여 O(1)로 동작하며, round-robin, least-connection 등 다양한 로드 밸런싱 알고리즘도 지원합니다.

```bash
# IPVS 가상 서버
IP Virtual Server version 1.2.1
-> 10.96.0.10:80 rr
  -> 10.244.1.5:8080    Masq    1
  -> 10.244.1.6:8080    Masq    1
  -> 10.244.2.3:8080    Masq    1
```

---

## Ingress

Service는 L4(TCP/UDP)에서 동작하여 IP와 포트 기반으로만 라우팅합니다. 하나의 도메인에서 `/api`는 API 서비스로, `/web`은 프론트엔드 서비스로 보내고 싶다면 어떻게 해야 할까요? URL 경로나 호스트명에 따라 트래픽을 분배하려면 L7(HTTP/HTTPS)에서 동작하는 **Ingress**가 필요합니다.

Ingress는 Service를 대체하는 것이 아니라, Service 앞에서 L7 라우팅을 추가하는 계층입니다.

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

Ingress 리소스는 "이런 라우팅을 원한다"는 선언입니다. 아래 예시는 `example.com/api`로 들어오는 요청은 api-service로, 나머지는 web-service로 보내며, TLS 인증서도 지정합니다.

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

Ingress 리소스가 선언이라면, 이를 실제로 구현하는 것은 **Ingress Controller**입니다. Kubernetes에는 기본 Ingress Controller가 포함되어 있지 않으므로 별도로 설치해야 합니다.

| Controller | 특징 |
|-----------|------|
| **NGINX Ingress** | 가장 널리 사용되며, 범용적인 선택지 |
| **Traefik** | 동적 설정과 자동 인증서 갱신이 강점 |
| **HAProxy Ingress** | 높은 처리량이 필요한 환경에 적합 |
| **ALB Ingress Controller** | AWS 환경에서 클라우드 로드 밸런서와 직접 통합 |

클라우드 환경에서는 해당 클라우드의 네이티브 컨트롤러를 사용하면 로드 밸런서와 자연스럽게 통합됩니다.

---

## Network Policy

지금까지 살펴본 Service와 Ingress는 트래픽을 올바른 Pod로 전달하는 역할을 합니다. 하지만 기본적으로 Kubernetes에서 모든 Pod는 서로 제한 없이 통신할 수 있습니다. 프론트엔드 Pod가 데이터베이스 Pod에 직접 접근하거나, 침해된 Pod 하나가 클러스터 내 모든 서비스에 요청을 보낼 수 있다는 뜻입니다. **Network Policy**는 Pod 간 통신을 세밀하게 제어하여 이 문제를 해결합니다.

아래 예시는 `app: api` Pod의 트래픽을 제한합니다. 여기서 `Ingress`와 `Egress`는 앞서 다룬 Ingress 리소스가 아니라 인바운드/아웃바운드 트래픽 방향을 뜻합니다.

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

이 정책이 적용되면 `app: api` Pod는 인바운드로 `app: web` Pod의 8080 포트만, 아웃바운드로 `app: database` Pod의 5432 포트만 허용됩니다. 그 외의 통신은 모두 차단됩니다.

### 기본 거부 정책

개별 Pod마다 정책을 작성하기 전에, 먼저 모든 트래픽을 기본 차단하는 **Zero Trust** 접근법을 적용할 수 있습니다.

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

이 정책을 먼저 적용하고, 각 서비스에 필요한 통신 경로만 명시적으로 열어줍니다. 서비스 하나가 침해되더라도 다른 서비스로의 접근이 차단되어 피해 범위를 줄일 수 있습니다.

Network Policy는 CNI 플러그인이 지원해야 동작합니다. Flannel은 지원하지 않으므로, 이 기능이 필요하다면 Calico, Cilium 등을 선택해야 합니다.

---

## 서비스 메시 개요

서비스 수가 수십 개를 넘어가면 Service와 Network Policy만으로는 다루기 어려운 요구사항이 생깁니다. 서비스 간 통신을 **mTLS**(서로의 인증서를 검증하는 양방향 TLS)로 암호화해야 하고, 요청이 실패했을 때 어느 서비스에서 문제가 생겼는지 추적해야 하며, **카나리 배포**(새 버전을 일부 트래픽에만 먼저 적용하여 안정성을 확인하는 방식)를 위한 세밀한 트래픽 제어도 필요해집니다.

이런 기능을 각 서비스에 직접 구현하면 비즈니스 로직과 인프라 로직이 뒤섞이게 됩니다. **서비스 메시(Service Mesh)**는 이 인프라 로직을 애플리케이션 밖으로 분리합니다.

<br>

### Sidecar 패턴

서비스 메시는 각 Pod에 **사이드카(Sidecar)** 컨테이너를 주입하여 이를 구현합니다. 사이드카는 앱 컨테이너 옆에서 함께 실행되는 프록시로, Pod의 모든 인바운드/아웃바운드 트래픽을 가로챕니다.

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

앱 컨테이너는 localhost로 통신한다고 생각하지만, 실제로는 사이드카 프록시가 외부 통신을 처리합니다. 앱 코드를 수정하지 않아도 mTLS 암호화, 트래픽 관찰, 라우팅 제어가 가능해집니다.

### 주요 서비스 메시

| | **Istio** | **Linkerd** |
|--|----------|------------|
| 프록시 | Envoy (C++) | 자체 경량 프록시 (Rust) |
| 기능 | mTLS, 트레이싱, 세밀한 라우팅 정책 등 풍부 | 핵심 기능(mTLS, 트레이싱, 로드밸런싱)에 집중 |
| 운영 복잡성 | 높음 (중앙 제어 구성 요소가 많음) | 낮음 (설치 간단, 리소스 사용량 적음) |
| 적합 환경 | 대규모 클러스터, 세밀한 제어 필요 시 | 서비스 메시 첫 도입, 경량 운영 |

---

## 마무리

- Pod는 고유 IP를 가지며, NAT 없이 직접 통신합니다
- Service는 고정 주소로 서비스 디스커버리와 로드 밸런싱을 제공합니다
- Ingress는 Service 앞에서 L7 라우팅을 추가합니다
- Network Policy는 Pod 간 통신을 제어합니다
- 서비스 메시는 사이드카 프록시로 인프라 로직을 애플리케이션 밖에서 처리합니다

이 추상화 계층들은 아래에서 위로 쌓이며, 각 계층이 아래 계층의 복잡성을 숨깁니다.

```
         높음
          │
          │   Service Mesh (mTLS, 트레이싱, 트래픽 제어)
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

이 시리즈에서는 Linux 네트워크 네임스페이스에서 출발하여 오버레이 네트워크를 거쳐 Kubernetes의 추상화 계층까지 살펴봤습니다. 결국 컨테이너 네트워킹은 기존 네트워크 기술을 새로운 방식으로 조합한 것입니다. 각 계층이 어떤 문제를 해결하는지 이해하면, 장애가 발생했을 때 어느 계층에서 문제를 찾아야 할지 판단할 수 있습니다.

<br>

---

**관련 글**
- [로드 밸런싱과 고가용성 (1) - 로드 밸런싱의 원리](/dev/network/LoadBalancing-1/)
- [네트워크 보안의 원리 (2) - TLS와 인증서 체계](/dev/network/NetworkSecurity-2/)

**시리즈**
- [컨테이너 네트워킹 (1) - 컨테이너 네트워크 기초](/dev/network/ContainerNetwork-1/)
- [컨테이너 네트워킹 (2) - 오버레이 네트워크](/dev/network/ContainerNetwork-2/)
- 컨테이너 네트워킹 (3) - Kubernetes 네트워킹 (현재 글)
