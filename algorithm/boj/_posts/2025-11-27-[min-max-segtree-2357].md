---
layout: single
title: "[백준 2357] 최솟값과 최댓값 (C#, C++) - soo:bak"
date: "2025-11-27 01:20:00 +0900"
description: 세그먼트 트리로 구간 최솟값과 최댓값을 O(log N) 시간에 조회하는 백준 2357번 최솟값과 최댓값 문제의 C# 및 C++ 풀이
---

## 문제 링크
[2357번 - 최솟값과 최댓값](https://www.acmicpc.net/problem/2357)

## 설명

`N`개의 정수가 주어지고 `M`개의 쿼리마다 구간 `[a, b]`의 최솟값과 최댓값을 출력하는 상황에서 `N`과 `M` (`1 ≤ N, M ≤ 100,000`)이 주어질 때, 모든 쿼리의 결과를 구하는 문제입니다.

각 쿼리를 선형 탐색으로 처리하면 O(NM)이 되어 최대 100억 번의 연산이 필요하므로 시간 초과가 발생합니다.

<br>

## 접근법

매 쿼리마다 구간을 선형 탐색하면 O(N)이 소요되어 시간 초과가 발생합니다. 세그먼트 트리를 사용하면 미리 구간 정보를 계산해두고 쿼리당 O(log N)에 답을 구할 수 있습니다.

세그먼트 트리는 배열을 이진 트리 형태로 표현하여 각 노드가 특정 구간의 최솟값과 최댓값을 저장하는 자료구조입니다. 예를 들어 배열 `[1, 3, 2, 7]`이 주어지면, 루트 노드는 전체 구간 `[0, 3]`의 정보 (최솟값 1, 최댓값 7)를 저장하고, 왼쪽 자식은 구간 `[0, 1]`의 정보 (최솟값 1, 최댓값 3)를, 오른쪽 자식은 구간 `[2, 3]`의 정보 (최솟값 2, 최댓값 7)를 저장합니다.

<br>
트리를 구축할 때는 리프 노드에 각 원소를 배치하고, 상위 노드로 올라가며 왼쪽 자식과 오른쪽 자식의 최솟값 중 작은 값, 최댓값 중 큰 값을 저장합니다. 트리의 높이는 O(log N)이므로 전체 구축 시간은 O(N)입니다.

쿼리를 처리할 때는 루트에서 시작하여 다음과 같이 재귀적으로 탐색합니다:
- 현재 노드의 구간과 쿼리 구간이 겹치지 않으면 답에 영향을 주지 않는 값(`INT_MAX`, `INT_MIN`)을 반환합니다.
- 현재 노드의 구간이 쿼리 구간에 완전히 포함되면 해당 노드에 저장된 값을 반환합니다.
- 그 외의 경우 왼쪽 자식과 오른쪽 자식을 재귀적으로 탐색한 후, 두 결과를 병합하여 최솟값과 최댓값을 구합니다.

<br>
예를 들어 구간 `[1, 3]`을 쿼리하면, 트리를 탐색하며 해당 구간을 포함하는 노드들의 정보를 병합하여 O(log N) 시간에 답을 얻습니다.

전체 시간 복잡도는 트리 구축 O(N)과 각 쿼리 O(log N)을 합쳐 O(N + M log N)입니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    const int INF = int.MaxValue;
    static int N, M;
    static int[] arr;
    static int[] segMin, segMax;

    static void Build(int node, int l, int r) {
      if (l == r) {
        segMin[node] = arr[l];
        segMax[node] = arr[l];
        return;
      }

      var mid = (l + r) >> 1;

      Build(node * 2, l, mid);
      Build(node * 2 + 1, mid + 1, r);

      segMin[node] = Math.Min(segMin[node * 2], segMin[node * 2 + 1]);
      segMax[node] = Math.Max(segMax[node * 2], segMax[node * 2 + 1]);
    }

    static (int mn, int mx) Query(int node, int l, int r, int ql, int qr) {
      if (qr < l || r < ql) return (INF, int.MinValue);
      if (ql <= l && r <= qr) return (segMin[node], segMax[node]);

      var mid = (l + r) >> 1;
      var left = Query(node * 2, l, mid, ql, qr);
      var right = Query(node * 2 + 1, mid + 1, r, ql, qr);

      return (Math.Min(left.mn, right.mn), Math.Max(left.mx, right.mx));
    }

    static void Main(string[] args) {
      var first = Console.ReadLine()!.Split();
      N = int.Parse(first[0]);
      M = int.Parse(first[1]);

      arr = new int[N];

      for (var i = 0; i < N; i++)
        arr[i] = int.Parse(Console.ReadLine()!);

      segMin = new int[4 * N];
      segMax = new int[4 * N];

      Build(1, 0, N - 1);

      for (var i = 0; i < M; i++) {
        var q = Console.ReadLine()!.Split();
        var a = int.Parse(q[0]) - 1;
        var b = int.Parse(q[1]) - 1;

        var res = Query(1, 0, N - 1, a, b);

        Console.WriteLine($"{res.mn} {res.mx}");
      }
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;
typedef pair<int, int> pii;

struct SegTree {
  int n;
  vi tmin, tmax;
  SegTree(int n): n(n), tmin(4*n), tmax(4*n) {}

  void build(const vi& a, int node, int l, int r) {
    if (l == r) {
      tmin[node] = tmax[node] = a[l];
      return;
    }

    int mid = (l + r) >> 1;

    build(a, node*2, l, mid);
    build(a, node*2+1, mid+1, r);

    tmin[node] = min(tmin[node*2], tmin[node*2+1]);
    tmax[node] = max(tmax[node*2], tmax[node*2+1]);
  }

  pii query(int node, int l, int r, int ql, int qr) {
    if (qr < l || r < ql) return {INT_MAX, INT_MIN};
    if (ql <= l && r <= qr) return {tmin[node], tmax[node]};

    int mid = (l + r) >> 1;

    auto left = query(node*2, l, mid, ql, qr);
    auto right = query(node*2+1, mid+1, r, ql, qr);

    return {min(left.first, right.first), max(left.second, right.second)};
  }
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;

  vi a(n);

  for (int i = 0; i < n; i++)
    cin >> a[i];

  SegTree seg(n);
  seg.build(a, 1, 0, n-1);

  while (m--) {
    int l, r; cin >> l >> r;

    auto res = seg.query(1, 0, n-1, l-1, r-1);

    cout << res.first << " " << res.second << "\n";
  }

  return 0;
}
```

