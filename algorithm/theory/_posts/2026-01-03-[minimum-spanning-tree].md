---
layout: single
title: "최소 신장 트리(Minimum Spanning Tree)의 원리와 구현 - soo:bak"
date: "2026-01-03 06:00:00 +0900"
description: 그래프의 모든 정점을 최소 비용으로 연결하는 최소 신장 트리의 개념, Kruskal과 Prim 알고리듬의 원리와 구현을 다룹니다
---

## 최소 신장 트리란?

**최소 신장 트리(Minimum Spanning Tree, MST)**는 가중치가 있는 연결 그래프에서 **모든 정점을 최소 비용으로 연결**하는 트리입니다.

<br>

**신장 트리(Spanning Tree)**란?
- 그래프의 모든 정점을 포함
- 사이클이 없음
- 정점이 $$V$$개면 간선은 $$V-1$$개

<br>

**최소 신장 트리**는 신장 트리 중 **간선 가중치의 합이 최소**인 트리입니다.

<br>

**활용 예시**:
- 도시 간 도로/전선 최소 비용 연결
- 네트워크 설계
- 클러스터링

<br>

## MST의 두 가지 주요 알고리듬

<br>

### 1. Kruskal 알고리듬

**간선 중심** 접근법: 가중치가 작은 간선부터 선택

<br>

### 2. Prim 알고리듬

**정점 중심** 접근법: 연결된 정점에서 가장 가까운 정점 선택

<br>

두 알고리듬 모두 [그리디 알고리듬](https://soo-bak.github.io/algorithm/theory/greedyAlgo/)에 기반합니다.

<br>

## Kruskal 알고리듬

<br>

### 동작 원리

1. 모든 간선을 가중치 순으로 정렬
2. 가중치가 작은 간선부터 선택
3. 선택한 간선이 사이클을 형성하면 건너뛰기
4. $$V-1$$개의 간선을 선택할 때까지 반복

<br>

### 사이클 판별: Union-Find

사이클 판별을 위해 [유니온 파인드(Union-Find)](https://soo-bak.github.io/algorithm/theory/union-find/) 자료구조를 사용합니다.

두 정점이 같은 집합에 속하면 간선을 추가할 경우 사이클이 형성됩니다.

<br>

### Kruskal 구현

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

**출력**: `MST 비용: 19`

<br>

### Kruskal 시간 복잡도

- 간선 정렬: $$O(E \log E)$$
- Union-Find 연산: $$O(E \cdot \alpha(V))$$ (거의 상수)
- **전체**: $$O(E \log E)$$

<br>

## Prim 알고리듬

<br>

### 동작 원리

1. 임의의 정점에서 시작
2. MST에 포함된 정점과 연결된 간선 중 가중치가 최소인 간선 선택
3. 해당 간선으로 연결된 새 정점을 MST에 추가
4. 모든 정점이 MST에 포함될 때까지 반복

<br>

### Prim 구현 (우선순위 큐 사용)

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

**출력**: `MST 비용: 19`

<br>

### Prim 시간 복잡도

- 우선순위 큐 사용: $$O((V + E) \log V)$$
- 인접 행렬 사용: $$O(V^2)$$

<br>

## Kruskal vs Prim

<br>

| 특성 | Kruskal | Prim |
|------|---------|------|
| 접근 방식 | 간선 중심 | 정점 중심 |
| 자료구조 | Union-Find | 우선순위 큐 |
| 시간 복잡도 | $$O(E \log E)$$ | $$O((V+E) \log V)$$ |
| 희소 그래프 | 유리 | - |
| 밀집 그래프 | - | 유리 |
| 간선 리스트 | 적합 | - |
| 인접 리스트 | - | 적합 |

<br>

**선택 기준**:
- 간선이 적은 **희소 그래프**: Kruskal
- 간선이 많은 **밀집 그래프**: Prim

<br>

## MST의 성질

<br>

**1. Cut Property (절단 특성)**

그래프를 두 집합으로 나누는 절단에서, 절단을 가로지르는 최소 가중치 간선은 MST에 포함됩니다.

<br>

**2. Cycle Property (사이클 특성)**

그래프의 임의의 사이클에서 최대 가중치 간선은 MST에 포함되지 않습니다.

<br>

**3. 유일성**

모든 간선의 가중치가 서로 다르면 MST는 유일합니다.

<br>

## 예제: 도시 연결하기

<br>

**문제**: N개의 도시를 모두 연결하는 도로를 건설하려 합니다. 도로 건설 비용을 최소화하세요.

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
  ios::sync_with_stdio(false);
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
    cout << "불가능\n";  // 연결 불가
  }

  return 0;
}
```

<br>

## 마무리

최소 신장 트리는 그래프의 모든 정점을 최소 비용으로 연결하는 핵심 알고리듬입니다.

<br>

**핵심 포인트**
- **MST 정의**: 모든 정점 연결, 사이클 없음, 최소 가중치
- **Kruskal**: 간선 정렬 + Union-Find
- **Prim**: 정점 확장 + 우선순위 큐
- **시간 복잡도**: $$O(E \log E)$$ 또는 $$O((V+E) \log V)$$

<br>

MST는 네트워크 설계, 클러스터링, 근사 알고리듬 등 다양한 분야에서 활용됩니다.

<br>

### 관련 글
- [유니온 파인드(Union-Find)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/union-find/)
- [그리디 알고리듬(Greedy Algorithm)의 원리와 적용 - soo:bak](https://soo-bak.github.io/algorithm/theory/greedyAlgo/)
- [다익스트라 알고리듬의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/Dijkstra/)

<br>

### 관련 문제
- [[백준 1197] 최소 스패닝 트리](https://www.acmicpc.net/problem/1197)
- [[백준 1922] 네트워크 연결](https://www.acmicpc.net/problem/1922)
- [[백준 4386] 별자리 만들기](https://www.acmicpc.net/problem/4386)

