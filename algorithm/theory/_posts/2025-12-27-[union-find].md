---
layout: single
title: "유니온-파인드 - 분리 집합의 효율적 관리 - soo:bak"
date: "2025-12-27 02:30:00 +0900"
description: 유니온-파인드(서로소 집합)의 원리와 경로 압축, 랭크 기반 합치기 최적화를 통한 효율적인 구현을 설명합니다.
---

## 유니온-파인드란?

**유니온-파인드(Union-Find)** 는 **서로소 집합(Disjoint Set)** 을 효율적으로 관리하는 자료구조입니다.

<br>
두 가지 핵심 연산을 지원합니다:

- **Find**: 원소가 속한 집합의 대표(루트) 찾기
- **Union**: 두 집합을 하나로 합치기

<br>
친구 관계, 네트워크 연결, 그래프의 연결 요소 등을 표현할 때 유용합니다.

<br>

---

<br>

## 기본 아이디어

각 집합을 **트리**로 표현합니다.

트리의 **루트**가 집합의 **대표**입니다.

<br>

### 예시

```
초기: {1}, {2}, {3}, {4}, {5}  (각자 별개의 집합)

Union(1, 2): {1, 2}, {3}, {4}, {5}
Union(3, 4): {1, 2}, {3, 4}, {5}
Union(1, 3): {1, 2, 3, 4}, {5}

트리 구조:
    1
   /|\
  2 3 ...
    |
    4
```

<br>

---

<br>

## 기본 구현

### 배열을 이용한 표현

`parent[i]` = 노드 i의 부모 노드

루트는 자기 자신을 부모로 가집니다.

<br>

```cpp
#include <bits/stdc++.h>
using namespace std;

int parent[MAX_N];

// 초기화: 모든 노드가 자기 자신을 부모로
void init(int n) {
    for (int i = 0; i < n; i++)
        parent[i] = i;
}

// Find: 루트 찾기
int find(int x) {
    if (parent[x] == x)
        return x;
    return find(parent[x]);
}

// Union: 두 집합 합치기
void unite(int x, int y) {
    int rootX = find(x);
    int rootY = find(y);
    if (rootX != rootY)
        parent[rootX] = rootY;
}
```

<br>

### 시간 복잡도 (최적화 전)

최악의 경우 트리가 **일자로** 늘어나면,

Find 연산이 **O(n)** 까지 느려집니다.

<br>

---

<br>

## 최적화 1: 경로 압축 (Path Compression)

Find 연산 시 **방문한 모든 노드를 루트에 직접 연결**합니다.

<br>

```cpp
int find(int x) {
    if (parent[x] == x)
        return x;
    return parent[x] = find(parent[x]);  // 경로 압축
}
```

<br>

### 동작 과정

```
Find(4) 호출:

변경 전:          변경 후:
    1                 1
    |               / | \
    2              2  3  4
    |
    3
    |
    4
```

<br>
다음 번 Find(4)는 한 번에 루트를 찾습니다.

<br>

---

<br>

## 최적화 2: 랭크 기반 합치기 (Union by Rank)

항상 **작은 트리를 큰 트리에** 붙입니다.

트리의 높이가 급격히 증가하는 것을 방지합니다.

<br>

```cpp
int parent[MAX_N];
int rank_[MAX_N];  // 트리의 높이 (근사값)

void init(int n) {
    for (int i = 0; i < n; i++) {
        parent[i] = i;
        rank_[i] = 0;
    }
}

void unite(int x, int y) {
    int rootX = find(x);
    int rootY = find(y);

    if (rootX == rootY) return;

    // 랭크가 작은 트리를 큰 트리에 붙이기
    if (rank_[rootX] < rank_[rootY])
        parent[rootX] = rootY;
    else if (rank_[rootX] > rank_[rootY])
        parent[rootY] = rootX;
    else {
        parent[rootY] = rootX;
        rank_[rootX]++;
    }
}
```

<br>

---

<br>

## 최적화된 시간 복잡도

경로 압축과 랭크 기반 합치기를 모두 적용하면:

- **Find**: O(α(n)) ≈ O(1)
- **Union**: O(α(n)) ≈ O(1)

<br>
α(n)은 **애커만 함수의 역함수**로, 실질적으로 상수입니다.

n이 우주의 원자 수보다 커도 α(n) < 5 입니다.

<br>

---

<br>

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

int find(int x) {
    if (parent[x] != x)
        parent[x] = find(parent[x]);
    return parent[x];
}

void unite(int x, int y) {
    int rootX = find(x);
    int rootY = find(y);

    if (rootX == rootY) return;

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

<br>

## 유니온-파인드 활용

### 연결 요소 개수 세기

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

```cpp
int size_[MAX_N];

void init(int n) {
    for (int i = 0; i <= n; i++) {
        parent[i] = i;
        size_[i] = 1;
    }
}

void unite(int x, int y) {
    int rootX = find(x);
    int rootY = find(y);

    if (rootX == rootY) return;

    if (size_[rootX] < size_[rootY])
        swap(rootX, rootY);

    parent[rootY] = rootX;
    size_[rootX] += size_[rootY];
}

int getSize(int x) {
    return size_[find(x)];
}
```

<br>

---

<br>

## 크루스칼 알고리즘과 유니온-파인드

**최소 스패닝 트리(MST)** 를 구하는 크루스칼 알고리즘에서 유니온-파인드가 핵심적으로 사용됩니다.

<br>

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
        if (!isSameSet(e.u, e.v)) {
            unite(e.u, e.v);
            mstCost += e.cost;
            edgeCount++;
            if (edgeCount == n - 1) break;
        }
    }

    return mstCost;
}
```

<br>

---

<br>

## 관련 문제 유형

유니온-파인드는 다음과 같은 문제에서 활용됩니다:

- 그래프의 연결 요소 판별
- 사이클 존재 여부 확인
- 최소 스패닝 트리 (크루스칼)
- 네트워크 연결 문제
- 집합의 동적 관리
- 친구 네트워크

<br>

