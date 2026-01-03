---
layout: single
title: "세그먼트 트리 - 구간 쿼리의 효율적 처리 - soo:bak"
date: "2025-12-27 02:20:00 +0900"
description: 세그먼트 트리의 구조와 원리, 구간 합/최솟값 쿼리, 점 업데이트와 구간 업데이트의 구현을 설명합니다.
tags:
  - 자료구조
  - 세그먼트트리
  - 트리
---

## 세그먼트 트리란?

길이가 10만인 배열이 있고, "3번째부터 7만번째까지의 합은?"이라는 질문에 답해야 한다고 가정해보겠습니다.

단순히 반복문으로 더하면 O(n)이 걸리며, 만약 이런 질의를 10만 번 수행해야 된다면 총 O(n²) = 100억 번의 연산이 필요합니다.

<br>

**세그먼트 트리(Segment Tree)** 는 이런 **구간 쿼리**를 **O(log n)** 에 처리하는 자료구조입니다.

구간 합, 구간 최솟값, 구간 최댓값 등 다양한 구간 연산을 빠르게 수행할 수 있습니다.

<br>

| 연산 | 일반 배열 | 누적 합 | 세그먼트 트리 |
|------|----------|--------|--------------|
| 구간 쿼리 | O(n) | O(1) | O(log n) |
| 점 업데이트 | O(1) | O(n) | O(log n) |

<br>

누적 합(Prefix Sum)은 구간 합을 O(1)에 구할 수 있지만, 값이 바뀌면 누적 합 배열 전체를 다시 계산해야 합니다.

**쿼리와 업데이트가 모두 빈번**할 때 세그먼트 트리가 유용합니다.

<br>

---

## 세그먼트 트리의 구조

세그먼트 트리는 **완전 이진 트리** 형태입니다.

<br>

### 노드의 의미

- **리프 노드**: 배열의 각 원소
- **내부 노드**: 자식 노드들이 담당하는 구간의 정보 (합, 최솟값 등)

<br>

각 노드는 특정 **구간**을 담당합니다.

루트는 전체 구간을 담당하고, 왼쪽 자식은 왼쪽 절반, 오른쪽 자식은 오른쪽 절반을 담당합니다.

<br>

### 예시: 구간 합 트리

배열 `[1, 3, 5, 7, 9, 11]`에 대한 세그먼트 트리:

```
                  36 [0,5]          ← 전체 구간의 합
                /         \
          9 [0,2]        27 [3,5]
         /      \        /      \
     4 [0,1]  5 [2,2]  16 [3,4]  11 [5,5]
     /    \            /    \
 1 [0,0] 3 [1,1]   7 [3,3] 9 [4,4]
```

<br>

노드의 `[i,j]`는 해당 노드가 담당하는 구간입니다. 각 노드는 해당 구간의 합을 저장합니다.

<br>

---

## 세그먼트 트리 구현

### 트리 크기

n개의 원소에 대해 트리 크기는 최대 **4n** 입니다. 완전 이진 트리가 아닐 수 있으므로 여유있게 잡습니다.

```cpp
const int MAX_N = 100000;
int tree[4 * MAX_N];
```

<br>

### 인덱스 규칙 (1-based)

- 루트: 노드 1
- 노드 `node`의 왼쪽 자식: `node * 2`
- 노드 `node`의 오른쪽 자식: `node * 2 + 1`

<br>

### 트리 초기화 (Build)

배열을 기반으로 세그먼트 트리를 구축합니다.

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

const int MAX_N = 100000;
ll arr[MAX_N];
ll tree[4 * MAX_N];

// node: 현재 노드 번호
// start, end: 현재 노드가 담당하는 구간
void build(int node, int start, int end) {
  // 리프 노드: 배열 원소 저장
  if (start == end) {
    tree[node] = arr[start];
    return;
  }

  int mid = (start + end) / 2;
  build(node * 2, start, mid);       // 왼쪽 자식
  build(node * 2 + 1, mid + 1, end); // 오른쪽 자식

  // 자식들의 합으로 현재 노드 값 계산
  tree[node] = tree[node * 2] + tree[node * 2 + 1];
}

// 호출: build(1, 0, n-1);
```

<br>

**시간 복잡도**: O(n) - 모든 노드를 한 번씩 방문

<br>

### 구간 쿼리 (Query)

구간 `[l, r]`의 합을 구합니다.

```cpp
// l, r: 쿼리 구간
ll query(int node, int start, int end, int l, int r) {
  // Case 1: 현재 구간이 쿼리 구간과 완전히 겹치지 않음
  if (r < start || end < l)
    return 0;  // 합의 항등원

  // Case 2: 현재 구간이 쿼리 구간에 완전히 포함됨
  if (l <= start && end <= r)
    return tree[node];

  // Case 3: 일부만 겹침 → 자식에게 위임
  int mid = (start + end) / 2;
  ll leftSum = query(node * 2, start, mid, l, r);
  ll rightSum = query(node * 2 + 1, mid + 1, end, l, r);
  return leftSum + rightSum;
}

// 호출: query(1, 0, n-1, l, r);
```

<br>

**시간 복잡도**: O(log n) - 트리의 높이만큼만 탐색

<br>

### 점 업데이트 (Update)

인덱스 `idx`의 값을 `val`로 변경합니다.

```cpp
void update(int node, int start, int end, int idx, ll val) {
  // 리프 노드에 도달
  if (start == end) {
    arr[idx] = val;
    tree[node] = val;
    return;
  }

  int mid = (start + end) / 2;
  if (idx <= mid)
    update(node * 2, start, mid, idx, val);       // 왼쪽으로
  else
    update(node * 2 + 1, mid + 1, end, idx, val); // 오른쪽으로

  // 자식 값이 바뀌었으므로 현재 노드 갱신
  tree[node] = tree[node * 2] + tree[node * 2 + 1];
}

// 호출: update(1, 0, n-1, idx, val);
```

<br>

**시간 복잡도**: O(log n) - 루트에서 리프까지 한 경로만 갱신

<br>

---

## 구간 쿼리 동작 원리

구간 `[2, 5]`의 합을 구하는 과정을 시각화합니다.

```
                  36 [0,5]    ← 일부 겹침, 자식으로 분할
                /         \
          9 [0,2]        27 [3,5]  ← 완전 포함! 바로 반환
         /      \
     4 [0,1]  5 [2,2]  ← 완전 포함! 바로 반환
     ↑
  벗어남
```

<br>

1. 루트 `[0,5]`는 `[2,5]`와 일부 겹침 → 자식으로 분할
2. `[0,2]`도 일부 겹침 → 자식으로 분할
3. `[0,1]`은 `[2,5]`와 겹치지 않음 → 0 반환
4. `[2,2]`는 완전 포함 → 5 반환
5. `[3,5]`는 완전 포함 → 27 반환

결과: 0 + 5 + 27 = **32**

<br>

---

## 구간 최솟값 쿼리

합 대신 최솟값을 저장하면 **구간 최솟값 트리(Range Minimum Query, RMQ)** 가 됩니다.

```cpp
const int INF = 1e9;

void build(int node, int start, int end) {
  if (start == end) {
    tree[node] = arr[start];
    return;
  }

  int mid = (start + end) / 2;
  build(node * 2, start, mid);
  build(node * 2 + 1, mid + 1, end);
  tree[node] = min(tree[node * 2], tree[node * 2 + 1]);  // 최솟값
}

int query(int node, int start, int end, int l, int r) {
  if (r < start || end < l)
    return INF;  // 최솟값의 항등원

  if (l <= start && end <= r)
    return tree[node];

  int mid = (start + end) / 2;
  return min(query(node * 2, start, mid, l, r),
             query(node * 2 + 1, mid + 1, end, l, r));
}
```

<br>

**항등원**: 연산의 결과에 영향을 주지 않는 값
- 합: 0
- 최솟값: INF (충분히 큰 값)
- 최댓값: -INF

<br>

---

## Lazy Propagation (느리게 갱신되는 세그먼트 트리)

지금까지는 하나의 원소만 변경하는 점 업데이트를 다루었지만, 여러 원소를 한 번에 변경하는 구간 업데이트가 필요한 경우도 있습니다.

<br>

구간 [l, r]의 모든 값에 val을 더하는 경우, 각 원소를 개별 업데이트하면 O((r-l+1) × log n)이 걸립니다.

하지만, Lazy Propagation을 사용하면 O(log n)에 처리할 수 있습니다.

<br>

### 아이디어

업데이트를 **즉시 반영하지 않고**, **나중에 필요할 때** 자식에게 전파합니다.

각 노드에 **지연된 업데이트 값(lazy)** 을 저장합니다.

<br>

### 핵심 원리

1. 구간 업데이트 시, 해당 구간을 완전히 포함하는 노드만 갱신하고, lazy 값을 자식에게 남겨둠
2. 나중에 그 노드를 방문할 때, lazy 값을 자식에게 전파(propagate)

<br>

### 구현

```cpp
ll tree[4 * MAX_N];
ll lazy[4 * MAX_N];

// lazy 값을 자식에게 전파
void propagate(int node, int start, int end) {
  if (lazy[node] != 0) {
    // 현재 노드에 lazy 값 반영
    tree[node] += (end - start + 1) * lazy[node];

    // 리프가 아니면 자식에게 lazy 전달
    if (start != end) {
      lazy[node * 2] += lazy[node];
      lazy[node * 2 + 1] += lazy[node];
    }

    lazy[node] = 0;  // lazy 초기화
  }
}

// 구간 [l, r]에 val을 더함
void updateRange(int node, int start, int end, int l, int r, ll val) {
  propagate(node, start, end);

  if (r < start || end < l)
    return;

  if (l <= start && end <= r) {
    tree[node] += (end - start + 1) * val;
    if (start != end) {
      lazy[node * 2] += val;
      lazy[node * 2 + 1] += val;
    }
    return;
  }

  int mid = (start + end) / 2;
  updateRange(node * 2, start, mid, l, r, val);
  updateRange(node * 2 + 1, mid + 1, end, l, r, val);
  tree[node] = tree[node * 2] + tree[node * 2 + 1];
}

ll query(int node, int start, int end, int l, int r) {
  propagate(node, start, end);  // 쿼리 전에 항상 propagate

  if (r < start || end < l)
    return 0;

  if (l <= start && end <= r)
    return tree[node];

  int mid = (start + end) / 2;
  return query(node * 2, start, mid, l, r) +
         query(node * 2 + 1, mid + 1, end, l, r);
}
```

<br>

---

## 다양한 구간 연산

세그먼트 트리는 **결합 법칙**이 성립하는 연산이면 모두 적용 가능합니다.

<br>

| 연산 | 항등원 | 결합 함수 |
|------|-------|----------|
| 합 | 0 | a + b |
| 최솟값 | INF | min(a, b) |
| 최댓값 | -INF | max(a, b) |
| GCD | 0 | gcd(a, b) |
| XOR | 0 | a ^ b |
| 곱 | 1 | a * b |

<br>

---

## 마무리

세그먼트 트리는 구간 쿼리와 업데이트를 O(log n)에 처리하는 자료구조입니다.

<br>

| 연산 | 시간 복잡도 |
|------|-----------|
| 트리 구축 | O(n) |
| 점 업데이트 | O(log n) |
| 구간 쿼리 | O(log n) |
| 구간 업데이트 (Lazy) | O(log n) |

<br>

쿼리만 필요하고 업데이트가 없다면 누적 합이 더 간단합니다. 하지만 **쿼리와 업데이트가 모두 빈번**할 때는 세그먼트 트리가 유용합니다.

<br>

**관련 문제**
- [백준 2042번 - 구간 합 구하기](https://www.acmicpc.net/problem/2042)
- [백준 10868번 - 최솟값](https://www.acmicpc.net/problem/10868)
- [백준 11505번 - 구간 곱 구하기](https://www.acmicpc.net/problem/11505)
- [백준 10999번 - 구간 합 구하기 2](https://www.acmicpc.net/problem/10999)
- [백준 14427번 - 수열과 쿼리 15](https://www.acmicpc.net/problem/14427)
