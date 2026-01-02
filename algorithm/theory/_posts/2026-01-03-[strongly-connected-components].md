---
layout: single
title: "강한 연결 요소(Strongly Connected Components)의 원리와 구현 - soo:bak"
date: "2026-01-03 11:00:00 +0900"
description: 방향 그래프에서 서로 도달 가능한 정점들의 최대 집합인 강한 연결 요소를 찾는 Kosaraju, Tarjan 알고리듬을 다룹니다
---

## 강한 연결 요소란?

**강한 연결 요소(Strongly Connected Components, SCC)**는 방향 그래프에서 **서로 도달 가능한 정점들의 최대 집합**입니다.

<br>

SCC 내의 임의의 두 정점 $$u$$, $$v$$에 대해:
- $$u$$에서 $$v$$로 가는 경로가 존재
- $$v$$에서 $$u$$로 가는 경로가 존재

<br>

**예시**

```
  1 → 2 → 3
  ↑   ↓   ↓
  4 ← 5   6
```

SCC: `{1, 2, 4, 5}`, `{3}`, `{6}`

<br>

## SCC의 성질

<br>

**1. SCC는 분리됨**

서로 다른 SCC 사이에는 양방향 경로가 없습니다.

<br>

**2. SCC 압축 그래프는 DAG**

각 SCC를 하나의 노드로 압축하면 **방향 비순환 그래프(DAG)**가 됩니다.

<br>

**3. 모든 정점은 정확히 하나의 SCC에 속함**

SCC들은 그래프의 정점 집합을 분할합니다.

<br>

## Kosaraju 알고리듬

**두 번의 DFS**로 SCC를 찾는 알고리듬입니다.

<br>

### 동작 원리

1. **첫 번째 DFS**: 원본 그래프에서 DFS를 수행하며 종료 순서를 스택에 저장
2. **그래프 역전**: 모든 간선의 방향을 반대로
3. **두 번째 DFS**: 스택 순서대로 역방향 그래프에서 DFS 수행

<br>

### 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

class KosarajuSCC {
private:
  int n;
  vector<vector<int>> adj, radj;  // 원본, 역방향 그래프
  vector<bool> visited;
  stack<int> order;
  vector<int> sccId;
  int sccCount;

  void dfs1(int u) {
    visited[u] = true;
    for (int v : adj[u]) {
      if (!visited[v]) dfs1(v);
    }
    order.push(u);
  }

  void dfs2(int u, int id) {
    sccId[u] = id;
    for (int v : radj[u]) {
      if (sccId[v] == -1) dfs2(v, id);
    }
  }

public:
  KosarajuSCC(int n) : n(n), adj(n), radj(n), visited(n, false),
                        sccId(n, -1), sccCount(0) {}

  void addEdge(int u, int v) {
    adj[u].push_back(v);
    radj[v].push_back(u);
  }

  int findSCCs() {
    // 첫 번째 DFS: 종료 순서 저장
    for (int i = 0; i < n; i++) {
      if (!visited[i]) dfs1(i);
    }

    // 두 번째 DFS: 역방향 그래프에서 SCC 찾기
    while (!order.empty()) {
      int u = order.top();
      order.pop();
      if (sccId[u] == -1) {
        dfs2(u, sccCount++);
      }
    }

    return sccCount;
  }

  int getSccId(int u) { return sccId[u]; }
};

int main() {
  KosarajuSCC scc(8);

  scc.addEdge(0, 1);
  scc.addEdge(1, 2);
  scc.addEdge(2, 0);
  scc.addEdge(2, 3);
  scc.addEdge(3, 4);
  scc.addEdge(4, 5);
  scc.addEdge(5, 3);
  scc.addEdge(6, 5);
  scc.addEdge(6, 7);
  scc.addEdge(7, 6);

  int count = scc.findSCCs();
  cout << "SCC 개수: " << count << "\n";

  for (int i = 0; i < 8; i++) {
    cout << "정점 " << i << ": SCC " << scc.getSccId(i) << "\n";
  }

  return 0;
}
```

<br>

### 시간 복잡도

- **시간**: $$O(V + E)$$
- **공간**: $$O(V + E)$$

<br>

## Tarjan 알고리듬

**한 번의 DFS**로 SCC를 찾는 알고리듬입니다.

<br>

### 핵심 개념

- **발견 시간 (disc)**: DFS 방문 순서
- **낮은 링크 (low)**: 현재 정점에서 도달 가능한 가장 작은 발견 시간
- **스택**: 현재 SCC 후보 정점들 저장

<br>

### 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

class TarjanSCC {
private:
  int n, timer, sccCount;
  vector<vector<int>> adj;
  vector<int> disc, low, sccId;
  vector<bool> onStack;
  stack<int> st;

  void dfs(int u) {
    disc[u] = low[u] = timer++;
    st.push(u);
    onStack[u] = true;

    for (int v : adj[u]) {
      if (disc[v] == -1) {
        dfs(v);
        low[u] = min(low[u], low[v]);
      } else if (onStack[v]) {
        low[u] = min(low[u], disc[v]);
      }
    }

    // SCC의 루트인 경우
    if (low[u] == disc[u]) {
      while (true) {
        int v = st.top();
        st.pop();
        onStack[v] = false;
        sccId[v] = sccCount;
        if (v == u) break;
      }
      sccCount++;
    }
  }

public:
  TarjanSCC(int n) : n(n), adj(n), disc(n, -1), low(n),
                      sccId(n, -1), onStack(n, false),
                      timer(0), sccCount(0) {}

  void addEdge(int u, int v) {
    adj[u].push_back(v);
  }

  int findSCCs() {
    for (int i = 0; i < n; i++) {
      if (disc[i] == -1) dfs(i);
    }
    return sccCount;
  }

  int getSccId(int u) { return sccId[u]; }
};
```

<br>

### 시간 복잡도

- **시간**: $$O(V + E)$$
- **공간**: $$O(V)$$

<br>

## Kosaraju vs Tarjan

<br>

| 특성 | Kosaraju | Tarjan |
|------|----------|--------|
| DFS 횟수 | 2번 | 1번 |
| 역방향 그래프 | 필요 | 불필요 |
| 구현 난이도 | 쉬움 | 중간 |
| 스택 사용 | 종료 순서 | SCC 후보 |

<br>

## SCC 활용

<br>

**1. 2-SAT 문제**

논리식의 만족 가능성을 SCC로 판별합니다.

<br>

**2. 그래프 압축**

SCC를 하나의 노드로 압축하여 DAG로 변환합니다.

```cpp
vector<vector<int>> condensation(int n, TarjanSCC& scc) {
  int sccCount = scc.findSCCs();
  vector<set<int>> adjSet(sccCount);

  // SCC 간 간선 추가
  for (int u = 0; u < n; u++) {
    for (int v : adj[u]) {
      int su = scc.getSccId(u);
      int sv = scc.getSccId(v);
      if (su != sv) {
        adjSet[su].insert(sv);
      }
    }
  }

  // set을 vector로 변환
  vector<vector<int>> dag(sccCount);
  for (int i = 0; i < sccCount; i++) {
    for (int j : adjSet[i]) {
      dag[i].push_back(j);
    }
  }

  return dag;
}
```

<br>

**3. 도달 가능성 분석**

같은 SCC 내의 정점들은 서로 도달 가능합니다.

<br>

## 마무리

강한 연결 요소는 방향 그래프에서 서로 도달 가능한 정점들의 최대 집합입니다.

<br>

**핵심 포인트**
- **정의**: SCC 내 임의의 두 정점은 양방향 도달 가능
- **알고리듬**: Kosaraju (2회 DFS), Tarjan (1회 DFS)
- **시간 복잡도**: $$O(V + E)$$
- **활용**: 2-SAT, 그래프 압축, 도달 가능성

<br>

### 관련 글
- [그래프 탐색: DFS와 BFS - soo:bak](https://soo-bak.github.io/algorithm/theory/graph-traversal-dfs-bfs/)
- [위상 정렬(Topological Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/topological-sort/)

<br>

### 관련 문제
- [[백준 2150] Strongly Connected Component](https://www.acmicpc.net/problem/2150)
- [[백준 4196] 도미노](https://www.acmicpc.net/problem/4196)

