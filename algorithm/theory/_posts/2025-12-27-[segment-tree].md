---
layout: single
title: "세그먼트 트리 - 구간 쿼리의 효율적 처리 - soo:bak"
date: "2025-12-27 02:20:00 +0900"
description: 세그먼트 트리의 구조와 원리, 구간 합/최솟값 쿼리, 점 업데이트와 구간 업데이트의 구현을 설명합니다.
---

## 세그먼트 트리란?

**세그먼트 트리(Segment Tree)** 는 배열의 **구간 쿼리**와 **업데이트**를 효율적으로 처리하는 자료구조입니다.

<br>
일반 배열에서 구간 합을 구하려면 **O(n)** 이 걸립니다.

세그먼트 트리를 사용하면 **O(log n)** 에 가능합니다.

<br>

| 연산 | 일반 배열 | 세그먼트 트리 |
|------|----------|--------------|
| 구간 쿼리 | O(n) | O(log n) |
| 점 업데이트 | O(1) | O(log n) |

<br>

---

<br>

## 세그먼트 트리의 구조

세그먼트 트리는 **완전 이진 트리** 형태입니다.

<br>

### 노드의 의미

- **리프 노드**: 배열의 각 원소
- **내부 노드**: 자식 노드들의 구간 정보 (합, 최솟값 등)

<br>

### 예시: 구간 합 트리

배열: `[1, 3, 5, 7, 9, 11]`

```
                 36 [0,5]
               /         \
         9 [0,2]        27 [3,5]
        /      \        /      \
    4 [0,1]  5 [2,2]  16 [3,4]  11 [5,5]
    /    \            /    \
1 [0,0] 3 [1,1]   7 [3,3] 9 [4,4]
```

<br>
각 노드는 해당 구간의 합을 저장합니다.

<br>

---

<br>

## 세그먼트 트리 구현

### 트리 크기

n개의 원소에 대해 트리 크기는 최대 **4n** 입니다.

```cpp
int tree[4 * MAX_N];
```

<br>

### 트리 초기화 (Build)

```cpp
#include <bits/stdc++.h>
using namespace std;

int arr[MAX_N];
int tree[4 * MAX_N];

void build(int node, int start, int end) {
    if (start == end) {
        tree[node] = arr[start];
        return;
    }

    int mid = (start + end) / 2;
    build(node * 2, start, mid);
    build(node * 2 + 1, mid + 1, end);
    tree[node] = tree[node * 2] + tree[node * 2 + 1];
}
```

시간 복잡도: **O(n)**

<br>

### 구간 쿼리 (Query)

구간 `[l, r]`의 합을 구합니다.

```cpp
int query(int node, int start, int end, int l, int r) {
    // 범위를 완전히 벗어난 경우
    if (r < start || end < l)
        return 0;

    // 범위에 완전히 포함된 경우
    if (l <= start && end <= r)
        return tree[node];

    // 일부만 포함된 경우 → 분할
    int mid = (start + end) / 2;
    int leftSum = query(node * 2, start, mid, l, r);
    int rightSum = query(node * 2 + 1, mid + 1, end, l, r);
    return leftSum + rightSum;
}
```

시간 복잡도: **O(log n)**

<br>

### 점 업데이트 (Update)

인덱스 `idx`의 값을 `val`로 변경합니다.

```cpp
void update(int node, int start, int end, int idx, int val) {
    if (start == end) {
        arr[idx] = val;
        tree[node] = val;
        return;
    }

    int mid = (start + end) / 2;
    if (idx <= mid)
        update(node * 2, start, mid, idx, val);
    else
        update(node * 2 + 1, mid + 1, end, idx, val);

    tree[node] = tree[node * 2] + tree[node * 2 + 1];
}
```

시간 복잡도: **O(log n)**

<br>

---

<br>

## 구간 쿼리 동작 원리

구간 `[2, 5]`의 합을 구하는 과정:

```
                 36 [0,5]
               /         \
         9 [0,2]        27 [3,5] ← 완전 포함
        /      \
    4 [0,1]  5 [2,2] ← 완전 포함
```

<br>
`[2,2]`와 `[3,5]`는 쿼리 범위에 완전히 포함되므로 바로 반환합니다.

결과: 5 + 27 = 32

<br>

---

<br>

## 구간 최솟값 쿼리

합 대신 최솟값을 저장하면 **구간 최솟값 트리**가 됩니다.

<br>

```cpp
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
        return INF;  // 항등원

    if (l <= start && end <= r)
        return tree[node];

    int mid = (start + end) / 2;
    return min(query(node * 2, start, mid, l, r),
               query(node * 2 + 1, mid + 1, end, l, r));
}
```

<br>

---

<br>

## Lazy Propagation (게으른 전파)

**구간 업데이트**를 효율적으로 처리하는 기법입니다.

<br>
구간 `[l, r]`의 모든 값에 `val`을 더하는 경우,

각 원소를 개별 업데이트하면 **O(n log n)** 이 걸립니다.

<br>
Lazy Propagation을 사용하면 **O(log n)** 에 가능합니다.

<br>

### 아이디어

업데이트를 즉시 반영하지 않고 **나중에 필요할 때** 전파합니다.

각 노드에 **지연된 업데이트 값**을 저장합니다.

<br>

### 구현 개요

```cpp
int tree[4 * MAX_N];
int lazy[4 * MAX_N];

void propagate(int node, int start, int end) {
    if (lazy[node] != 0) {
        tree[node] += (end - start + 1) * lazy[node];
        if (start != end) {
            lazy[node * 2] += lazy[node];
            lazy[node * 2 + 1] += lazy[node];
        }
        lazy[node] = 0;
    }
}

void updateRange(int node, int start, int end, int l, int r, int val) {
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
```

<br>

---

<br>

## 세그먼트 트리 활용

### 다양한 구간 연산

| 연산 | 항등원 | 결합 |
|------|-------|------|
| 합 | 0 | a + b |
| 최솟값 | INF | min(a, b) |
| 최댓값 | -INF | max(a, b) |
| GCD | 0 | gcd(a, b) |
| XOR | 0 | a ^ b |

<br>
**결합 법칙**이 성립하는 연산이면 세그먼트 트리에 적용 가능합니다.

<br>

---

<br>

## 관련 문제 유형

세그먼트 트리는 다음과 같은 문제에서 활용됩니다:

- 구간 합 / 최솟값 / 최댓값 쿼리
- 구간 업데이트와 쿼리
- 좌표 압축 후 개수 세기
- 역순 쌍 개수 (Inversion Count)
- k번째 수 찾기

<br>

