---
layout: single
title: "강한 연결 요소(Strongly Connected Components)의 원리와 구현 - soo:bak"
date: "2026-01-03 11:00:00 +0900"
description: 방향 그래프에서 서로 도달 가능한 정점들의 최대 집합인 강한 연결 요소를 찾는 Kosaraju, Tarjan 알고리듬을 다룹니다
---

## 강한 연결 요소란?

**강한 연결 요소(Strongly Connected Components, SCC)**는 방향 그래프에서 **서로 도달 가능한 정점들의 최대 집합**입니다.

SCC 내의 임의의 두 정점 $$u$$, $$v$$에 대해 $$u$$에서 $$v$$로 가는 경로와 $$v$$에서 $$u$$로 가는 경로가 모두 존재합니다.

<br>

### 예시

```
  1 → 2 → 3
  ↑   ↓   ↓
  4 ← 5   6
```

위 그래프에서 정점 `1, 2, 4, 5`는 서로 도달 가능하므로 하나의 SCC를 이룹니다.

정점 `3`과 `6`은 각각 다른 정점으로부터 도달은 가능하지만, 다시 돌아갈 수 없으므로 각각 단독으로 SCC가 됩니다.

SCC: `{1, 2, 4, 5}`, `{3}`, `{6}`

---

## SCC의 성질

<br>

### SCC는 분리됨

서로 다른 SCC 사이에는 양방향 경로가 존재하지 않습니다.

만약 양방향 경로가 있다면, 두 SCC는 하나로 합쳐져야 하기 때문입니다.

<br>

### SCC 압축 그래프는 DAG

각 SCC를 하나의 노드로 압축하면 **방향 비순환 그래프(DAG)**가 됩니다.

사이클이 존재한다면 그 사이클에 포함된 모든 SCC는 하나로 합쳐져야 하므로 모순이 됩니다.

> 참고: [위상 정렬(Topological Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/topological-sort/)

<br>

### 모든 정점은 정확히 하나의 SCC에 속함

SCC들은 그래프의 정점 집합을 분할합니다.

어떤 정점도 두 개 이상의 SCC에 속하지 않으며, 모든 정점은 최소 자기 자신만으로 이루어진 SCC에는 속합니다.

---

## Kosaraju 알고리듬

**두 번의 DFS**로 SCC를 찾는 알고리듬입니다.

구현이 직관적이고 이해하기 쉽습니다.

<br>

### 동작 원리

1. **첫 번째 DFS**: 원본 그래프에서 DFS를 수행하며 종료 순서를 스택에 저장
2. **그래프 역전**: 모든 간선의 방향을 반대로 뒤집음
3. **두 번째 DFS**: 스택에서 꺼내는 순서대로 역방향 그래프에서 DFS 수행

<br>

첫 번째 DFS에서 늦게 종료된 정점일수록 스택의 위쪽에 쌓이게 됩니다.

역방향 그래프에서 이 순서대로 DFS를 수행하면, 같은 SCC에 속한 정점들만 방문하게 됩니다.

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
- **공간**: $$O(V + E)$$ (역방향 그래프 저장)

---

## Tarjan 알고리듬

**한 번의 DFS**로 SCC를 찾는 알고리듬입니다.

역방향 그래프를 만들 필요가 없어 메모리 효율이 좋습니다.

<br>

### 동작 원리

각 정점에 대해 두 가지 값을 관리합니다:

- **발견 시간 (disc)**: DFS에서 해당 정점을 처음 방문한 순서
- **낮은 링크 (low)**: 현재 정점에서 도달 가능한 정점들 중 가장 작은 발견 시간

<br>

DFS를 수행하면서 방문한 정점들을 스택에 쌓습니다.

어떤 정점 $$u$$에서 `low[u] == disc[u]`인 경우, $$u$$는 SCC의 루트입니다.

이때 스택에서 $$u$$까지의 모든 정점을 꺼내면 하나의 SCC가 됩니다.

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

---

## Kosaraju vs Tarjan

두 알고리듬 모두 $$O(V + E)$$ 시간에 동작하지만, 구현 방식과 특성이 다릅니다.

| 특성 | Kosaraju | Tarjan |
|------|----------|--------|
| DFS 횟수 | 2번 | 1번 |
| 역방향 그래프 | 필요 | 불필요 |
| 구현 난이도 | 쉬움 | 중간 |
| 공간 복잡도 | $$O(V + E)$$ | $$O(V)$$ |

<br>

Kosaraju는 이해하기 쉽고 구현이 직관적입니다.

Tarjan은 메모리를 덜 사용하고, 한 번의 DFS로 해결할 수 있어 실전에서 더 자주 사용됩니다.

---

## SCC 활용

<br>

### 2-SAT 문제

논리식 $$(x_1 \lor x_2) \land (\lnot x_1 \lor x_3) \land ...$$ 형태의 만족 가능성을 판별할 때 SCC를 활용합니다.

각 변수와 그 부정을 정점으로, 함의 관계를 간선으로 표현한 그래프에서 SCC를 구합니다.

어떤 변수 $$x$$와 $$\lnot x$$가 같은 SCC에 속하면 만족 불가능, 그렇지 않으면 만족 가능합니다.

<br>

### 그래프 압축 (Condensation)

SCC를 하나의 노드로 압축하여 DAG로 변환하면, 복잡한 방향 그래프 문제를 단순화할 수 있습니다.

```cpp
vector<vector<int>> condensation(int n, vector<vector<int>>& adj,
                                  vector<int>& sccId, int sccCount) {
  vector<set<int>> adjSet(sccCount);

  // SCC 간 간선 추가
  for (int u = 0; u < n; u++) {
    for (int v : adj[u]) {
      int su = sccId[u];
      int sv = sccId[v];
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

### 도달 가능성 분석

같은 SCC 내의 정점들은 서로 도달 가능합니다.

서로 다른 SCC 사이의 도달 가능성은 압축 그래프(DAG)에서 판단할 수 있습니다.

---

## 마무리

강한 연결 요소는 방향 그래프에서 서로 도달 가능한 정점들의 최대 집합입니다.

Kosaraju 알고리듬은 두 번의 DFS로 직관적으로 SCC를 찾고, Tarjan 알고리듬은 한 번의 DFS로 더 효율적으로 찾습니다.

두 알고리듬 모두 $$O(V + E)$$ 시간에 동작하며, 2-SAT, 그래프 압축, 도달 가능성 분석 등 다양한 문제에 활용됩니다.

> 참고: [그래프 탐색: DFS와 BFS - soo:bak](https://soo-bak.github.io/algorithm/theory/graph-traversal-dfs-bfs/)

<br>

**관련 글**:
- [그래프 탐색: DFS와 BFS - soo:bak](https://soo-bak.github.io/algorithm/theory/graph-traversal-dfs-bfs/)
- [위상 정렬(Topological Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/topological-sort/)

<br>

**관련 문제**:
- [[백준 2150] Strongly Connected Component](https://www.acmicpc.net/problem/2150)
- [[백준 4196] 도미노](https://www.acmicpc.net/problem/4196)
- [[백준 11280] 2-SAT - 3](https://www.acmicpc.net/problem/11280)
