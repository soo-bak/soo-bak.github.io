---
layout: single
title: "유니온-파인드 - 분리 집합의 효율적 관리 - soo:bak"
date: "2025-12-27 02:30:00 +0900"
description: 유니온-파인드(서로소 집합)의 원리와 경로 압축, 랭크 기반 합치기 최적화를 통한 효율적인 구현을 설명합니다.
---

## 유니온-파인드란?

SNS에서 "A와 B는 친구이고, B와 C는 친구이다"라는 관계가 주어졌다고 가정해보겠습니다. A와 C는 직접 연결되어 있지 않지만, B를 통해 연결되어 있으므로 같은 친구 그룹입니다. 이처럼 "두 사람이 같은 그룹인지"를 빠르게 판별하는 것이 유니온-파인드의 핵심입니다.

<br>

**유니온-파인드(Union-Find)** 는 이처럼 **서로소 집합(Disjoint Set)** 을 효율적으로 관리하는 자료구조입니다. "서로소"란 공통 원소가 없다는 의미로, 각 원소는 정확히 하나의 집합에만 속합니다.

<br>

유니온-파인드는 두 가지 핵심 연산을 지원합니다:
- **Find**: 원소가 속한 집합의 대표(루트) 찾기
- **Union**: 두 집합을 하나로 합치기

<br>

친구 관계, 네트워크 연결, 그래프의 연결 요소 판별 등 다양한 문제에서 활용됩니다.

<br>

---

## 기본 아이디어

각 집합을 **트리**로 표현합니다. 트리의 **루트**가 집합의 **대표**가 됩니다. 같은 루트를 가진 원소들은 같은 집합에 속합니다.

<br>

### 예시

5명의 사람 {1, 2, 3, 4, 5}가 있고, 처음에는 각자 별개의 집합입니다.

```
초기 상태: {1}, {2}, {3}, {4}, {5}

Union(1, 2) 후: {1, 2}, {3}, {4}, {5}
  1
  |
  2

Union(3, 4) 후: {1, 2}, {3, 4}, {5}
  1     3
  |     |
  2     4

Union(1, 3) 후: {1, 2, 3, 4}, {5}
    1
   /|\
  2 3 ...
    |
    4
```

<br>

이제 Find(4)를 호출하면 루트인 1이 반환됩니다. Find(2)도 1이 반환됩니다. 즉, 2와 4는 같은 집합입니다.

<br>

---

## 기본 구현

### 배열을 이용한 표현

`parent[i]` = 노드 i의 부모 노드

루트 노드는 자기 자신을 부모로 가집니다 (`parent[root] = root`).

<br>

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAX_N = 100001;
int parent[MAX_N];

// 초기화: 모든 노드가 자기 자신을 부모로 (각자 별개의 집합)
void init(int n) {
  for (int i = 1; i <= n; i++)
    parent[i] = i;
}

// Find: 루트 찾기
int find(int x) {
  if (parent[x] == x)
    return x;  // 루트 발견
  return find(parent[x]);  // 부모를 따라 올라감
}

// Union: 두 집합 합치기
void unite(int x, int y) {
  int rootX = find(x);
  int rootY = find(y);
  if (rootX != rootY)
    parent[rootX] = rootY;  // x의 루트를 y의 루트에 연결
}

// 같은 집합인지 확인
bool isSameSet(int x, int y) {
  return find(x) == find(y);
}
```

<br>

### 시간 복잡도 (최적화 전)

문제는 트리가 **한쪽으로 치우칠 수 있다**는 것입니다.

```
Union(1, 2), Union(2, 3), Union(3, 4), Union(4, 5) 순서로 실행하면:

  5
  |
  4
  |
  3
  |
  2
  |
  1
```

이 경우 Find(1)은 모든 노드를 거쳐야 하므로 **O(n)** 이 걸립니다.

<br>

---

## 최적화 1: 경로 압축 (Path Compression)

Find 연산 시 **방문한 모든 노드를 루트에 직접 연결**합니다. 다음 번 Find가 훨씬 빨라집니다.

<br>

```cpp
int find(int x) {
  if (parent[x] == x)
    return x;
  return parent[x] = find(parent[x]);  // 경로 압축: 루트를 직접 저장
}
```

<br>

### 동작 과정

Find(1)을 호출하면:

```
변경 전:          변경 후:
    5                 5
    |              /||\
    4             4 3 2 1
    |
    3
    |
    2
    |
    1
```

<br>

모든 노드가 루트에 직접 연결되어, 다음 번 Find는 O(1)에 완료됩니다.

<br>

---

## 최적화 2: 랭크 기반 합치기 (Union by Rank)

Union 시 항상 **작은(낮은) 트리를 큰(높은) 트리에** 붙입니다. 트리의 높이가 급격히 증가하는 것을 방지합니다.

<br>

`rank[i]` = 노드 i를 루트로 하는 트리의 높이 (근사값)

<br>

```cpp
int parent[MAX_N];
int rank_[MAX_N];  // rank는 C++ 예약어이므로 rank_ 사용

void init(int n) {
  for (int i = 1; i <= n; i++) {
    parent[i] = i;
    rank_[i] = 0;  // 초기 높이는 0
  }
}

void unite(int x, int y) {
  int rootX = find(x);
  int rootY = find(y);

  if (rootX == rootY)
    return;  // 이미 같은 집합

  // 랭크가 작은 트리를 큰 트리에 붙이기
  if (rank_[rootX] < rank_[rootY]) {
    parent[rootX] = rootY;
  } else if (rank_[rootX] > rank_[rootY]) {
    parent[rootY] = rootX;
  } else {
    // 랭크가 같으면 아무나 붙이고, 붙인 쪽의 랭크 증가
    parent[rootY] = rootX;
    rank_[rootX]++;
  }
}
```

<br>

---

## 최적화된 시간 복잡도

경로 압축과 랭크 기반 합치기를 **모두** 적용하면:

- **Find**: O(α(n))
- **Union**: O(α(n))

<br>

α(n)은 **애커만 함수의 역함수**로, 실질적으로 **상수**입니다. n이 우주의 원자 수(약 10⁸⁰)보다 커도 α(n) < 5입니다. 따라서 모든 연산이 **거의 O(1)** 에 수행된다고 볼 수 있습니다.

<br>

---

## 전체 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAX_N = 100001;
int parent[MAX_N];
int rank_[MAX_N];

void init(int n) {
  for (int i = 0; i <= n; i++) {
    parent[i] = i;
    rank_[i] = 0;
  }
}

// Find with path compression
int find(int x) {
  if (parent[x] != x)
    parent[x] = find(parent[x]);
  return parent[x];
}

// Union by rank
void unite(int x, int y) {
  int rootX = find(x);
  int rootY = find(y);

  if (rootX == rootY)
    return;

  if (rank_[rootX] < rank_[rootY])
    swap(rootX, rootY);

  parent[rootY] = rootX;
  if (rank_[rootX] == rank_[rootY])
    rank_[rootX]++;
}

bool isSameSet(int x, int y) {
  return find(x) == find(y);
}
```

<br>

---

## 유니온-파인드 활용

### 연결 요소 개수 세기

각 집합의 루트는 자기 자신을 부모로 가집니다. 이를 이용해 집합의 개수를 셀 수 있습니다.

```cpp
int countSets(int n) {
  int count = 0;
  for (int i = 1; i <= n; i++) {
    if (parent[i] == i)
      count++;
  }
  return count;
}
```

<br>

### 집합의 크기 관리

각 집합에 몇 개의 원소가 있는지 추적할 수 있습니다.

```cpp
int size_[MAX_N];

void init(int n) {
  for (int i = 0; i <= n; i++) {
    parent[i] = i;
    size_[i] = 1;  // 초기에 각 집합의 크기는 1
  }
}

void unite(int x, int y) {
  int rootX = find(x);
  int rootY = find(y);

  if (rootX == rootY)
    return;

  // 작은 집합을 큰 집합에 합치기
  if (size_[rootX] < size_[rootY])
    swap(rootX, rootY);

  parent[rootY] = rootX;
  size_[rootX] += size_[rootY];  // 크기 합산
}

int getSize(int x) {
  return size_[find(x)];
}
```

<br>

---

## 크루스칼 알고리즘과 유니온-파인드

**최소 스패닝 트리(MST)** 를 구하는 **크루스칼 알고리즘**에서 유니온-파인드가 핵심적으로 사용됩니다.

<br>

크루스칼 알고리즘의 아이디어:
1. 모든 간선을 가중치 순으로 정렬
2. 가중치가 작은 간선부터 선택
3. **사이클이 생기지 않으면** 트리에 추가
4. n-1개의 간선을 선택하면 종료

<br>

"사이클이 생기는지"는 **두 정점이 이미 같은 집합인지**로 판별합니다.

```cpp
struct Edge {
  int u, v, cost;
  bool operator<(const Edge& o) const {
    return cost < o.cost;
  }
};

int kruskal(vector<Edge>& edges, int n) {
  sort(edges.begin(), edges.end());
  init(n);

  int mstCost = 0;
  int edgeCount = 0;

  for (auto& e : edges) {
    // 두 정점이 다른 집합이면 (사이클이 안 생기면)
    if (!isSameSet(e.u, e.v)) {
      unite(e.u, e.v);
      mstCost += e.cost;
      edgeCount++;

      if (edgeCount == n - 1)
        break;  // MST 완성
    }
  }

  return mstCost;
}
```

<br>

---

## 그래프에서 사이클 판별

무방향 그래프에서 간선을 하나씩 추가하면서, **이미 같은 집합에 있는 두 정점을 연결하려 하면** 사이클이 발생합니다.

```cpp
bool hasCycle(vector<Edge>& edges, int n) {
  init(n);

  for (auto& e : edges) {
    if (isSameSet(e.u, e.v))
      return true;  // 사이클 발견
    unite(e.u, e.v);
  }

  return false;
}
```

<br>

---

## 마무리

유니온-파인드는 서로소 집합을 관리하는 효율적인 자료구조입니다.

<br>

| 연산 | 최적화 전 | 최적화 후 |
|------|----------|----------|
| Find | O(n) | O(α(n)) ≈ O(1) |
| Union | O(n) | O(α(n)) ≈ O(1) |

<br>

**핵심 최적화**:
- **경로 압축**: Find 시 모든 노드를 루트에 직접 연결
- **랭크 기반 합치기**: 작은 트리를 큰 트리에 붙이기

<br>

두 최적화를 모두 적용하면 거의 상수 시간에 동작합니다.

<br>

**관련 문제**
- [백준 1717번 - 집합의 표현](https://www.acmicpc.net/problem/1717)
- [백준 1976번 - 여행 가자](https://www.acmicpc.net/problem/1976)
- [백준 4195번 - 친구 네트워크](https://www.acmicpc.net/problem/4195)
- [백준 1197번 - 최소 스패닝 트리](https://www.acmicpc.net/problem/1197)
- [백준 20040번 - 사이클 게임](https://www.acmicpc.net/problem/20040)
