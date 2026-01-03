---
layout: single
title: "위상 정렬(Topological Sort)의 원리와 구현 - soo:bak"
date: "2026-01-03 07:00:00 +0900"
description: 방향 비순환 그래프(DAG)의 정점들을 선행 관계에 따라 정렬하는 위상 정렬의 원리, DFS와 BFS(Kahn) 구현 방법을 다룹니다
tags:
  - 그래프
  - 위상정렬
---

## 위상 정렬이란?

어떤 대학교의 교과과정을 생각해보겠습니다.

`통계학`을 수강하려면 먼저 `확률론`과 `선형대수`를 이수해야 하고, `확률론`을 듣기 위해서는 `미적분학`이 선행되어야 합니다.

이처럼 **선후 관계가 있는 작업들을 올바른 순서로 나열**하는 것이 바로 **위상 정렬(Topological Sort)**입니다.

<br>

**위상 정렬**은 **방향 비순환 그래프(DAG, Directed Acyclic Graph)**에서 정점들을 선행 관계에 따라 정렬하는 알고리듬입니다.

간선 `A → B`가 있으면, 정렬 결과에서 `A`는 반드시 `B`보다 앞에 위치합니다.

<br>

위 과목 예시를 그래프로 표현하면 다음과 같습니다:

```
미적분학 → 확률론
미적분학 → 선형대수
확률론 → 통계학
선형대수 → 통계학
```

가능한 위상 정렬 결과: `미적분학 → 확률론 → 선형대수 → 통계학` 또는 `미적분학 → 선형대수 → 확률론 → 통계학`

<br>

위상 정렬은 작업 스케줄링, 빌드 시스템의 의존성 해결, 컴파일러의 심볼 해석 등 다양한 분야에서 활용됩니다.

---

## 위상 정렬의 조건

위상 정렬이 가능하려면 그래프에 **사이클이 없어야** 합니다.

<br>

예를 들어 다음과 같은 상황을 생각해보겠습니다:

```
A → B → C → A  (사이클)
```

`A`를 처리하려면 `C`가 먼저 끝나야 하고, `C`를 처리하려면 `B`가 먼저 끝나야 하며, `B`를 처리하려면 `A`가 먼저 끝나야 합니다.

이 경우 어떤 정점도 먼저 처리할 수 없으므로, 위상 정렬이 불가능합니다.

---

## 구현 방법

위상 정렬을 구현하는 방법은 크게 두 가지입니다.

<br>

**DFS 기반**: 깊이 우선 탐색을 수행하면서, 탐색이 끝난 정점을 스택에 넣습니다. 스택을 역순으로 출력하면 위상 정렬 결과가 됩니다.

**BFS 기반 (Kahn's Algorithm)**: 진입 차수(in-degree)가 `0`인 정점부터 차례로 처리합니다.

---

## DFS 기반 위상 정렬

### 동작 원리

1. 모든 정점에 대해 DFS 수행
2. DFS가 끝난 정점을 스택에 push
3. 스택을 역순으로 출력하면 위상 정렬 결과

<br>

DFS가 끝났다는 것은 해당 정점에서 갈 수 있는 모든 정점을 이미 방문했다는 의미입니다.

따라서 스택에서 꺼내는 순서대로 나열하면, 선행 정점이 항상 앞에 오게 됩니다.

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

**시간 복잡도**: $$O(V + E)$$

모든 정점과 간선을 한 번씩 방문합니다.

**공간 복잡도**: $$O(V)$$

방문 배열과 스택에 정점 수만큼의 공간이 필요합니다.

---

## BFS 기반 위상 정렬 (Kahn's Algorithm)

### 동작 원리

1. 모든 정점의 진입 차수(in-degree) 계산
2. 진입 차수가 `0`인 정점을 큐에 삽입
3. 큐에서 정점을 꺼내 결과에 추가
4. 해당 정점에서 나가는 간선을 제거 (연결된 정점의 진입 차수 감소)
5. 진입 차수가 `0`이 된 정점을 큐에 삽입
6. 큐가 빌 때까지 반복

<br>

진입 차수가 `0`이라는 것은 해당 정점에 선행 조건이 없다는 의미입니다.

따라서 바로 처리할 수 있고, 처리 후에는 후속 정점들의 선행 조건 수가 하나씩 줄어듭니다.

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

**시간 복잡도**: $$O(V + E)$$

**공간 복잡도**: $$O(V)$$

---

## DFS와 BFS 방식의 차이

두 방식 모두 $$O(V + E)$$의 시간 복잡도를 가지며, 올바른 위상 정렬 결과를 제공합니다.

<br>

**BFS 방식(Kahn's Algorithm)**의 장점은 사이클을 자동으로 감지할 수 있다는 점입니다.

알고리듬이 종료된 후 결과에 포함된 정점 수가 전체 정점 수와 다르면, 그래프에 사이클이 존재한다는 의미입니다.

<br>

반면 **DFS 방식**에서 사이클을 탐지하려면 방문 상태를 세 가지로 구분해야 합니다:

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

`VISITING` 상태의 정점을 다시 방문한다면, 현재 탐색 경로 상에 사이클이 존재한다는 의미입니다.

---

## 실전 예제: 작업 순서 정하기

$$N$$개의 작업이 있고, 일부 작업은 다른 작업이 먼저 완료되어야 합니다.

가능한 작업 순서를 구하는 문제입니다.

<br>

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

---

## 위상 정렬과 최장 경로

DAG에서 최장 경로는 위상 정렬을 이용해 $$O(V + E)$$에 구할 수 있습니다.

<br>

위상 정렬 순서대로 각 정점을 방문하면서, 해당 정점까지의 최장 거리를 갱신합니다.

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

위상 정렬 순서대로 처리하면, 어떤 정점을 방문할 때 그 정점으로 들어오는 모든 간선의 출발점은 이미 처리가 완료된 상태입니다.

따라서 한 번의 순회만으로 최장 경로를 구할 수 있습니다.

---

## 마무리

위상 정렬은 DAG에서 정점들의 선행 관계를 고려한 순서를 구하는 알고리듬입니다.

<br>

DFS 방식은 탐색이 끝난 정점을 스택에 넣고 역순으로 출력하는 방식이고, BFS 방식(Kahn's Algorithm)은 진입 차수가 `0`인 정점부터 차례로 처리하는 방식입니다.

두 방식 모두 $$O(V + E)$$의 시간 복잡도를 가지며, BFS 방식은 사이클 탐지가 자연스럽게 이루어진다는 장점이 있습니다.

<br>

위상 정렬은 의존성 관리, 스케줄링, 컴파일러 설계 등 선행 관계가 있는 작업을 다루는 다양한 문제에서 활용됩니다.

<br>

**관련 글**:
- [그래프 탐색: DFS와 BFS - soo:bak](https://soo-bak.github.io/algorithm/theory/graph-traversal-dfs-bfs/)
- [동적 계획법(Dynamic Programming)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/dynamic-programming/)

<br>

**관련 문제**:
- [[백준 2252] 줄 세우기](https://www.acmicpc.net/problem/2252)
- [[백준 1766] 문제집](https://www.acmicpc.net/problem/1766)
- [[백준 1005] ACM Craft](https://www.acmicpc.net/problem/1005)
