---
layout: single
title: "위상 정렬(Topological Sort)의 원리와 구현 - soo:bak"
date: "2026-01-03 07:00:00 +0900"
description: 방향 비순환 그래프(DAG)의 정점들을 선행 관계에 따라 정렬하는 위상 정렬의 원리, DFS와 BFS(Kahn) 구현 방법을 다룹니다
---

## 위상 정렬이란?

**위상 정렬(Topological Sort)**은 **방향 비순환 그래프(DAG, Directed Acyclic Graph)**에서 정점들을 **선행 관계에 따라 정렬**하는 알고리듬입니다.

<br>

간선 `A → B`가 있으면, 정렬 결과에서 `A`는 반드시 `B`보다 앞에 위치합니다.

<br>

**예시: 과목 수강 순서**

```
미적분 → 확률
미적분 → 선형대수
확률 → 통계
선형대수 → 통계
```

위상 정렬 결과: `미적분 → 확률 → 선형대수 → 통계` 또는 `미적분 → 선형대수 → 확률 → 통계`

<br>

**활용 예시**:
- 작업 스케줄링
- 빌드 시스템 (의존성 해결)
- 컴파일러 (심볼 해석)
- 교과과정 설계

<br>

## 위상 정렬의 조건

<br>

**필수 조건: 사이클이 없어야 함**

사이클이 있으면 위상 정렬이 불가능합니다.

```
A → B → C → A  (사이클)
```

이 경우 A가 C보다 앞이고, C가 B보다 앞이고, B가 A보다 앞이어야 하므로 모순입니다.

<br>

## 두 가지 구현 방법

<br>

### 1. DFS 기반

깊이 우선 탐색을 수행하면서, 탐색이 끝난 정점을 스택에 넣습니다.

<br>

### 2. BFS 기반 (Kahn's Algorithm)

진입 차수(in-degree)가 0인 정점부터 처리합니다.

<br>

## DFS 기반 위상 정렬

<br>

### 동작 원리

1. 모든 정점에 대해 DFS 수행
2. DFS가 끝난 정점을 스택에 push
3. 스택을 역순으로 출력하면 위상 정렬 결과

<br>

### 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

class TopologicalSortDFS {
private:
  int n;
  vector<vector<int>> adj;
  vector<bool> visited;
  stack<int> result;

  void dfs(int u) {
    visited[u] = true;

    for (int v : adj[u]) {
      if (!visited[v]) {
        dfs(v);
      }
    }

    result.push(u);  // 탐색 완료 후 스택에 추가
  }

public:
  TopologicalSortDFS(int n) : n(n), adj(n), visited(n, false) {}

  void addEdge(int u, int v) {
    adj[u].push_back(v);
  }

  vector<int> sort() {
    for (int i = 0; i < n; i++) {
      if (!visited[i]) {
        dfs(i);
      }
    }

    vector<int> order;
    while (!result.empty()) {
      order.push_back(result.top());
      result.pop();
    }

    return order;
  }
};

int main() {
  TopologicalSortDFS ts(6);

  // 간선 추가 (예: 과목 의존성)
  ts.addEdge(5, 2);
  ts.addEdge(5, 0);
  ts.addEdge(4, 0);
  ts.addEdge(4, 1);
  ts.addEdge(2, 3);
  ts.addEdge(3, 1);

  vector<int> order = ts.sort();

  cout << "위상 정렬 결과: ";
  for (int v : order) {
    cout << v << " ";
  }
  cout << "\n";

  return 0;
}
```

**출력**: `위상 정렬 결과: 5 4 2 3 1 0`

<br>

### DFS 시간 복잡도

- **시간**: $$O(V + E)$$
- **공간**: $$O(V)$$ (방문 배열, 스택)

<br>

## BFS 기반 위상 정렬 (Kahn's Algorithm)

<br>

### 동작 원리

1. 모든 정점의 진입 차수(in-degree) 계산
2. 진입 차수가 0인 정점을 큐에 삽입
3. 큐에서 정점을 꺼내 결과에 추가
4. 해당 정점에서 나가는 간선을 제거 (연결된 정점의 진입 차수 감소)
5. 진입 차수가 0이 된 정점을 큐에 삽입
6. 큐가 빌 때까지 반복

<br>

### 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

class TopologicalSortBFS {
private:
  int n;
  vector<vector<int>> adj;
  vector<int> inDegree;

public:
  TopologicalSortBFS(int n) : n(n), adj(n), inDegree(n, 0) {}

  void addEdge(int u, int v) {
    adj[u].push_back(v);
    inDegree[v]++;
  }

  vector<int> sort() {
    queue<int> q;
    vector<int> order;

    // 진입 차수가 0인 정점 찾기
    for (int i = 0; i < n; i++) {
      if (inDegree[i] == 0) {
        q.push(i);
      }
    }

    while (!q.empty()) {
      int u = q.front();
      q.pop();
      order.push_back(u);

      for (int v : adj[u]) {
        inDegree[v]--;
        if (inDegree[v] == 0) {
          q.push(v);
        }
      }
    }

    // 모든 정점이 포함되지 않으면 사이클 존재
    if (order.size() != n) {
      return {};  // 사이클 존재
    }

    return order;
  }
};

int main() {
  TopologicalSortBFS ts(6);

  ts.addEdge(5, 2);
  ts.addEdge(5, 0);
  ts.addEdge(4, 0);
  ts.addEdge(4, 1);
  ts.addEdge(2, 3);
  ts.addEdge(3, 1);

  vector<int> order = ts.sort();

  if (order.empty()) {
    cout << "사이클이 존재합니다.\n";
  } else {
    cout << "위상 정렬 결과: ";
    for (int v : order) {
      cout << v << " ";
    }
    cout << "\n";
  }

  return 0;
}
```

**출력**: `위상 정렬 결과: 4 5 0 2 3 1`

<br>

### BFS 시간 복잡도

- **시간**: $$O(V + E)$$
- **공간**: $$O(V)$$ (진입 차수 배열, 큐)

<br>

## DFS vs BFS 방식 비교

<br>

| 특성 | DFS 방식 | BFS 방식 (Kahn) |
|------|----------|-----------------|
| 사이클 탐지 | 별도 처리 필요 | 자동 탐지 |
| 구현 복잡도 | 간단 | 간단 |
| 결과 순서 | 역순 스택 | 순차 큐 |
| 메모리 | 재귀 스택 | 큐 |

<br>

**BFS 방식의 장점**: 사이클을 자동으로 감지할 수 있습니다.

결과의 크기가 정점 수와 다르면 사이클이 존재합니다.

<br>

## 사이클 탐지 (DFS)

DFS 기반에서 사이클을 탐지하려면 방문 상태를 세 가지로 구분합니다:

```cpp
enum State { UNVISITED, VISITING, VISITED };

class TopologicalSortWithCycleDetection {
private:
  int n;
  vector<vector<int>> adj;
  vector<State> state;
  stack<int> result;
  bool hasCycle;

  void dfs(int u) {
    state[u] = VISITING;

    for (int v : adj[u]) {
      if (state[v] == VISITING) {
        hasCycle = true;  // 사이클 발견
        return;
      }
      if (state[v] == UNVISITED) {
        dfs(v);
        if (hasCycle) return;
      }
    }

    state[u] = VISITED;
    result.push(u);
  }

public:
  TopologicalSortWithCycleDetection(int n)
    : n(n), adj(n), state(n, UNVISITED), hasCycle(false) {}

  void addEdge(int u, int v) {
    adj[u].push_back(v);
  }

  vector<int> sort() {
    for (int i = 0; i < n; i++) {
      if (state[i] == UNVISITED) {
        dfs(i);
        if (hasCycle) return {};
      }
    }

    vector<int> order;
    while (!result.empty()) {
      order.push_back(result.top());
      result.pop();
    }
    return order;
  }
};
```

<br>

## 실전 예제: 작업 순서 정하기

<br>

**문제**: N개의 작업이 있고, 일부 작업은 다른 작업이 먼저 완료되어야 합니다. 가능한 작업 순서를 구하세요.

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m;  // 작업 수, 선행 조건 수
  cin >> n >> m;

  vector<vector<int>> adj(n + 1);
  vector<int> inDegree(n + 1, 0);

  for (int i = 0; i < m; i++) {
    int a, b;  // a를 먼저 해야 b를 할 수 있음
    cin >> a >> b;
    adj[a].push_back(b);
    inDegree[b]++;
  }

  queue<int> q;
  for (int i = 1; i <= n; i++) {
    if (inDegree[i] == 0) {
      q.push(i);
    }
  }

  vector<int> order;
  while (!q.empty()) {
    int u = q.front();
    q.pop();
    order.push_back(u);

    for (int v : adj[u]) {
      inDegree[v]--;
      if (inDegree[v] == 0) {
        q.push(v);
      }
    }
  }

  if (order.size() != n) {
    cout << "순서를 정할 수 없습니다.\n";
  } else {
    for (int v : order) {
      cout << v << " ";
    }
    cout << "\n";
  }

  return 0;
}
```

<br>

## 위상 정렬과 최장 경로

DAG에서 최장 경로는 위상 정렬을 이용해 $$O(V + E)$$에 구할 수 있습니다:

```cpp
vector<int> longestPath(int n, vector<vector<pair<int, int>>>& adj) {
  vector<int> inDegree(n, 0);
  vector<int> dist(n, 0);

  for (int u = 0; u < n; u++) {
    for (auto [v, w] : adj[u]) {
      inDegree[v]++;
    }
  }

  queue<int> q;
  for (int i = 0; i < n; i++) {
    if (inDegree[i] == 0) q.push(i);
  }

  while (!q.empty()) {
    int u = q.front();
    q.pop();

    for (auto [v, w] : adj[u]) {
      dist[v] = max(dist[v], dist[u] + w);
      if (--inDegree[v] == 0) {
        q.push(v);
      }
    }
  }

  return dist;
}
```

<br>

## 마무리

위상 정렬은 DAG에서 정점들의 선행 관계를 고려한 순서를 구하는 알고리듬입니다.

<br>

**핵심 포인트**
- **조건**: 방향 비순환 그래프(DAG)에서만 가능
- **두 가지 방법**: DFS (후위 순회) 또는 BFS (Kahn's Algorithm)
- **시간 복잡도**: $$O(V + E)$$
- **사이클 탐지**: BFS는 자동, DFS는 별도 처리

<br>

위상 정렬은 의존성 관리, 스케줄링, 컴파일러 설계 등 다양한 분야에서 필수적으로 활용됩니다.

<br>

### 관련 글
- [그래프 탐색: DFS와 BFS - soo:bak](https://soo-bak.github.io/algorithm/theory/graph-traversal-dfs-bfs/)
- [동적 계획법(Dynamic Programming)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/dynamic-programming/)

<br>

### 관련 문제
- [[백준 2252] 줄 세우기](https://www.acmicpc.net/problem/2252)
- [[백준 1766] 문제집](https://www.acmicpc.net/problem/1766)
- [[백준 1005] ACM Craft](https://www.acmicpc.net/problem/1005)

