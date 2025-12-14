---
layout: single
title: "[백준 27940] 가지 산사태 (C#, C++) - soo:bak"
date: "2025-12-14 09:03:00 +0900"
description: 구간 [1,t]에 누적 비를 더하며 최대 높이가 K를 넘는 첫 시점과 아무 층이나 찾아 출력하는 세그먼트 트리 풀이
---

## 문제 링크
[27940번 - 가지 산사태](https://www.acmicpc.net/problem/27940)

## 설명
비가 올 때마다 1층부터 특정 층까지 누적되는 상황에서, 어떤 층이라도 누적이 k를 초과하는 최초의 시점과 층을 찾는 문제입니다.

모든 비가 끝날 때까지 k를 넘는 층이 없으면 -1을 출력합니다.

<br>

## 접근법
세그먼트 트리로 구간 덧셈과 최댓값을 관리합니다.

매 비마다 구간 [1, t]에 값을 더한 뒤, 전체 최댓값이 k를 초과하는지 확인합니다.

k를 넘었다면 트리를 내려가며 왼쪽부터 최초로 k를 초과하는 위치를 찾습니다.

찾으면 비 번호와 층 번호를 출력하고, 끝까지 없으면 -1을 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  const int MAXN = 100000;
  static long[] seg = new long[4 * MAXN + 5];
  static long[] lazy = new long[4 * MAXN + 5];
  static int n;
  static long k;

  static void Push(int node) {
    if (lazy[node] == 0) return;
    var val = lazy[node];
    seg[node << 1] += val;
    seg[node << 1 | 1] += val;
    lazy[node << 1] += val;
    lazy[node << 1 | 1] += val;
    lazy[node] = 0;
  }

  static void Update(int node, int l, int r, int ql, int qr, long val) {
    if (qr < l || r < ql) return;
    if (ql <= l && r <= qr) {
      seg[node] += val;
      lazy[node] += val;
      return;
    }
    Push(node);
    var mid = (l + r) >> 1;
    Update(node << 1, l, mid, ql, qr, val);
    Update(node << 1 | 1, mid + 1, r, ql, qr, val);
    seg[node] = Math.Max(seg[node << 1], seg[node << 1 | 1]);
  }

  static int FindFirst(int node, int l, int r) {
    if (l == r) return l;
    Push(node);
    var mid = (l + r) >> 1;
    if (seg[node << 1] > k) return FindFirst(node << 1, l, mid);
    else return FindFirst(node << 1 | 1, mid + 1, r);
  }

  static void Main() {
    var first = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
    n = first[0];
    var m = first[1];
    k = first[2];

    for (var i = 1; i <= m; i++) {
      var info = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
      var t = info[0];
      var rain = info[1];
      Update(1, 1, n, 1, t, rain);
      if (seg[1] > k) {
        var pos = FindFirst(1, 1, n);
        Console.WriteLine($"{i} {pos}");
        return;
      }
    }
    Console.WriteLine(-1);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef vector<ll> vll;

struct SegTree {
  int n;
  vll mx, lz;
  SegTree(int n): n(n), mx(4 * n + 4, 0), lz(4 * n + 4, 0) {}
  void push(int node) {
    if (lz[node] == 0) return;
    ll v = lz[node];
    mx[node << 1] += v;
    mx[node << 1 | 1] += v;
    lz[node << 1] += v;
    lz[node << 1 | 1] += v;
    lz[node] = 0;
  }
  void add(int node, int l, int r, int ql, int qr, ll v) {
    if (qr < l || r < ql) return;
    if (ql <= l && r <= qr) { mx[node] += v; lz[node] += v; return; }
    push(node);
    int mid = (l + r) >> 1;
    add(node << 1, l, mid, ql, qr, v);
    add(node << 1 | 1, mid + 1, r, ql, qr, v);
    mx[node] = max(mx[node << 1], mx[node << 1 | 1]);
  }
  int firstOver(int node, int l, int r, ll k) {
    if (l == r) return l;
    push(node);
    int mid = (l + r) >> 1;
    if (mx[node << 1] > k) return firstOver(node << 1, l, mid, k);
    return firstOver(node << 1 | 1, mid + 1, r, k);
  }
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; ll k;
  cin >> n >> m >> k;
  SegTree st(n);
  for (int i = 1; i <= m; i++) {
    int t; ll rain; cin >> t >> rain;
    st.add(1, 1, n, 1, t, rain);
    if (st.mx[1] > k) {
      int pos = st.firstOver(1, 1, n, k);
      cout << i << " " << pos << "\n";
      return 0;
    }
  }
  cout << -1 << "\n";

  return 0;
}
```
