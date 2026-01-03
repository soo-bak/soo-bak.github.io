---
layout: single
title: "최소 신장 트리(Minimum Spanning Tree)의 원리와 구현 - soo:bak"
date: "2026-01-03 06:00:00 +0900"
description: 그래프의 모든 정점을 최소 비용으로 연결하는 최소 신장 트리의 개념, Kruskal과 Prim 알고리듬의 원리와 구현을 다룹니다
tags:
  - 그래프
  - 최소스패닝트리
  - MST
---

## 최소 신장 트리란?

여러 도시를 도로로 연결하려고 합니다.

모든 도시를 연결하되, 도로 건설 비용을 최소화하려면 어떤 도로를 선택해야 할까요?

이런 문제를 해결하는 것이 바로 **최소 신장 트리(Minimum Spanning Tree, MST)** 알고리듬입니다.

<br>

먼저 **신장 트리(Spanning Tree)**의 개념을 살펴보겠습니다.

신장 트리란 그래프의 모든 정점을 포함하면서 사이클이 없는 트리입니다.

정점이 $$V$$개인 그래프의 신장 트리는 정확히 $$V-1$$개의 간선을 가집니다.

<br>

**최소 신장 트리**는 이러한 신장 트리 중에서 간선 가중치의 합이 가장 작은 트리를 말합니다.

---

## 신장 트리의 성질

최소 신장 트리 알고리듬을 이해하기 위해 두 가지 중요한 성질을 알아두면 좋습니다.

<br>

### 절단 특성 (Cut Property)

그래프를 두 집합으로 나누는 절단(cut)을 생각해봅시다.

이 절단을 가로지르는 간선들 중 가중치가 최소인 간선은 반드시 MST에 포함됩니다.

<br>

### 사이클 특성 (Cycle Property)

그래프의 어떤 사이클에서 가중치가 최대인 간선은 MST에 포함되지 않습니다.

<br>

이 두 성질은 Kruskal과 Prim 알고리듬의 정당성을 뒷받침합니다.

---

## Kruskal 알고리듬

Kruskal 알고리듬은 **간선 중심**의 접근법입니다.

가중치가 작은 간선부터 하나씩 선택하면서 MST를 구성합니다.

> 참고: [그리디 알고리듬(Greedy Algorithm)의 원리와 적용 - soo:bak](https://soo-bak.github.io/algorithm/theory/greedyAlgo/)

<br>

### 동작 원리

1. 모든 간선을 가중치 순으로 정렬합니다.
2. 가중치가 작은 간선부터 순서대로 확인합니다.
3. 해당 간선을 추가해도 사이클이 생기지 않으면 MST에 포함시킵니다.
4. $$V-1$$개의 간선을 선택하면 종료합니다.

<br>

### 사이클 판별: Union-Find

간선을 추가할 때 사이클이 생기는지 어떻게 판별할까요?

두 정점이 이미 같은 집합(연결된 컴포넌트)에 속해 있다면, 그 사이에 간선을 추가하면 사이클이 형성됩니다.

이를 효율적으로 확인하기 위해 **유니온 파인드(Union-Find)** 자료구조를 사용합니다.

> 참고: [유니온 파인드(Union-Find)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/union-find/)

<br>

### 단계별 예시

다음과 같은 그래프를 생각해봅시다.

```
정점: 0, 1, 2, 3
간선: (0,1,10), (0,2,6), (0,3,5), (1,3,15), (2,3,4)
      (시작, 끝, 가중치)
```

**정렬 후 간선**: (2,3,4), (0,3,5), (0,2,6), (0,1,10), (1,3,15)

<br>

**1단계**: (2,3,4) 선택 - 2와 3 연결 (MST 비용: 4)

**2단계**: (0,3,5) 선택 - 0과 3 연결 (MST 비용: 9)

**3단계**: (0,2,6) 확인 - 0과 2가 이미 연결됨 (건너뜀)

**4단계**: (0,1,10) 선택 - 0과 1 연결 (MST 비용: 19)

<br>

3개의 간선을 선택했으므로 종료합니다. MST의 총 비용은 19입니다.

<br>

### 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Edge {
  int u, v, weight;
  bool operator<(const Edge& other) const {
    return weight < other.weight;
  }
};

class UnionFind {
private:
  vector<int> parent, rank_;

public:
  UnionFind(int n) : parent(n), rank_(n, 0) {
    for (int i = 0; i < n; i++) {
      parent[i] = i;
    }
  }

  int find(int x) {
    if (parent[x] != x) {
      parent[x] = find(parent[x]);  // 경로 압축
    }
    return parent[x];
  }

  bool unite(int x, int y) {
    int px = find(x), py = find(y);
    if (px == py) return false;  // 이미 같은 집합

    // 랭크 기반 합치기
    if (rank_[px] < rank_[py]) swap(px, py);
    parent[py] = px;
    if (rank_[px] == rank_[py]) rank_[px]++;

    return true;
  }
};

int kruskal(int n, vector<Edge>& edges) {
  sort(edges.begin(), edges.end());

  UnionFind uf(n);
  int mstWeight = 0;
  int edgeCount = 0;

  for (const Edge& e : edges) {
    if (uf.unite(e.u, e.v)) {
      mstWeight += e.weight;
      edgeCount++;
      if (edgeCount == n - 1) break;
    }
  }

  return mstWeight;
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);

  int n = 4;  // 정점 수
  vector<Edge> edges = {
    {0, 1, 10},
    {0, 2, 6},
    {0, 3, 5},
    {1, 3, 15},
    {2, 3, 4}
  };

  cout << "MST 비용: " << kruskal(n, edges) << "\n";

  return 0;
}
```

<br>

### 시간 복잡도

- 간선 정렬: $$O(E \log E)$$
- Union-Find 연산: $$O(E \cdot \alpha(V))$$ (여기서 $$\alpha$$는 아커만 함수의 역함수로, 거의 상수)
- **전체**: $$O(E \log E)$$

---

## Prim 알고리듬

Prim 알고리듬은 **정점 중심**의 접근법입니다.

하나의 정점에서 시작하여 MST를 점점 확장해 나갑니다.

<br>

### 동작 원리

1. 임의의 정점에서 시작합니다.
2. MST에 포함된 정점들과 연결된 간선 중 가중치가 최소인 간선을 선택합니다.
3. 해당 간선으로 연결된 새 정점을 MST에 추가합니다.
4. 모든 정점이 MST에 포함될 때까지 반복합니다.

<br>

### 단계별 예시

같은 그래프에서 정점 0부터 시작해봅시다.

<br>

**초기**: MST = {0}

**1단계**: 0과 연결된 간선 중 최소 - (0,3,5) 선택, MST = {0, 3}

**2단계**: 0,3과 연결된 간선 중 최소 - (2,3,4) 선택, MST = {0, 3, 2}

**3단계**: 0,2,3과 연결된 간선 중 최소 - (0,1,10) 선택, MST = {0, 1, 2, 3}

<br>

모든 정점이 포함되었으므로 종료합니다. MST의 총 비용은 19입니다.

<br>

### 구현 (우선순위 큐 사용)

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef pair<int, int> pii;

int prim(int n, vector<vector<pii>>& adj) {
  vector<bool> inMST(n, false);
  priority_queue<pii, vector<pii>, greater<pii>> pq;

  int mstWeight = 0;
  pq.push({0, 0});  // {가중치, 정점}

  while (!pq.empty()) {
    auto [weight, u] = pq.top();
    pq.pop();

    if (inMST[u]) continue;
    inMST[u] = true;
    mstWeight += weight;

    for (auto [v, w] : adj[u]) {
      if (!inMST[v]) {
        pq.push({w, v});
      }
    }
  }

  return mstWeight;
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);

  int n = 4;  // 정점 수
  vector<vector<pii>> adj(n);

  // 간선 추가 (양방향)
  auto addEdge = [&](int u, int v, int w) {
    adj[u].push_back({v, w});
    adj[v].push_back({u, w});
  };

  addEdge(0, 1, 10);
  addEdge(0, 2, 6);
  addEdge(0, 3, 5);
  addEdge(1, 3, 15);
  addEdge(2, 3, 4);

  cout << "MST 비용: " << prim(n, adj) << "\n";

  return 0;
}
```

<br>

### 시간 복잡도

- 우선순위 큐 사용: $$O((V + E) \log V)$$
- 인접 행렬과 선형 탐색 사용: $$O(V^2)$$

밀집 그래프에서는 인접 행렬 버전이, 희소 그래프에서는 우선순위 큐 버전이 효율적입니다.

---

## Kruskal vs Prim

두 알고리듬 중 어떤 것을 선택해야 할까요?

<br>

**Kruskal 알고리듬**은 간선 리스트 형태로 입력이 주어질 때 적합합니다.

간선의 개수가 적은 희소 그래프에서 효율적입니다.

<br>

**Prim 알고리듬**은 인접 리스트나 인접 행렬 형태로 그래프가 주어질 때 적합합니다.

간선의 개수가 많은 밀집 그래프에서 효율적입니다.

<br>

실전에서는 문제의 입력 형태와 그래프의 특성에 따라 선택하면 됩니다.

두 알고리듬 모두 같은 결과(MST)를 구하므로, 구현이 편한 쪽을 선택해도 무방합니다.

---

## 실전 예제: 도시 연결하기

### 문제

$$N$$개의 도시를 모두 연결하는 도로를 건설하려 합니다.

각 도로 후보와 건설 비용이 주어질 때, 모든 도시를 연결하는 최소 비용을 구하세요.

<br>

### 접근법

전형적인 최소 신장 트리 문제입니다.

도시를 정점으로, 도로를 간선으로 모델링하면 됩니다.

<br>

### 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Edge {
  int u, v, cost;
  bool operator<(const Edge& o) const {
    return cost < o.cost;
  }
};

class UnionFind {
  vector<int> p;
public:
  UnionFind(int n) : p(n) {
    iota(p.begin(), p.end(), 0);
  }
  int find(int x) {
    return p[x] == x ? x : p[x] = find(p[x]);
  }
  bool unite(int x, int y) {
    x = find(x); y = find(y);
    if (x == y) return false;
    p[y] = x;
    return true;
  }
};

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m;  // 도시 수, 도로 후보 수
  cin >> n >> m;

  vector<Edge> edges(m);
  for (int i = 0; i < m; i++) {
    cin >> edges[i].u >> edges[i].v >> edges[i].cost;
    edges[i].u--; edges[i].v--;  // 0-indexed
  }

  sort(edges.begin(), edges.end());

  UnionFind uf(n);
  int totalCost = 0;
  int count = 0;

  for (const Edge& e : edges) {
    if (uf.unite(e.u, e.v)) {
      totalCost += e.cost;
      count++;
      if (count == n - 1) break;
    }
  }

  if (count == n - 1) {
    cout << totalCost << "\n";
  } else {
    cout << -1 << "\n";  // 모든 도시를 연결할 수 없음
  }

  return 0;
}
```

---

## 마무리

최소 신장 트리는 그래프의 모든 정점을 최소 비용으로 연결하는 문제를 해결합니다.

<br>

Kruskal 알고리듬은 간선을 정렬하고 Union-Find를 사용하여 사이클을 판별하며,

Prim 알고리듬은 정점을 하나씩 확장하며 우선순위 큐로 최소 가중치 간선을 선택합니다.

<br>

두 알고리듬 모두 그리디 전략에 기반하며, $$O(E \log E)$$ 또는 $$O((V+E) \log V)$$의 시간 복잡도를 가집니다.

네트워크 설계, 도로 건설, 클러스터링 등 다양한 최적화 문제에서 활용됩니다.

<br>

**관련 글**:
- [유니온 파인드(Union-Find)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/union-find/)
- [그리디 알고리듬(Greedy Algorithm)의 원리와 적용 - soo:bak](https://soo-bak.github.io/algorithm/theory/greedyAlgo/)
- [다익스트라 알고리듬의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/Dijkstra/)

<br>

**관련 문제**:
- [[백준 1197] 최소 스패닝 트리](https://www.acmicpc.net/problem/1197)
- [[백준 1922] 네트워크 연결](https://www.acmicpc.net/problem/1922)
- [[백준 4386] 별자리 만들기](https://www.acmicpc.net/problem/4386)
