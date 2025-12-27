---
layout: single
title: "[백준 2336] 굉장한 학생 (C#, C++) - soo:bak"
date: "2025-12-06 12:51:00 +0900"
description: 첫 시험 순으로 정렬 후 세그트리로 두 번째 시험까지의 최소 세 번째 시험 등수를 관리해 '굉장한' 학생 수를 세는 백준 2336번 문제 풀이
tags:
  - 백준
  - BOJ
  - 2336
  - C#
  - C++
  - 알고리즘
  - 자료구조
  - 세그먼트트리
keywords: "백준 2336, 백준 2336번, BOJ 2336, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2336번 - 굉장한 학생](https://www.acmicpc.net/problem/2336)

## 설명

세 시험 등수가 모두 더 좋은 학생이 한 명도 없으면 그 학생은 굉장한 학생입니다. 굉장한 학생의 수를 구하는 문제입니다.

<br>

## 접근법

세 시험 등수를 모두 비교하면 복잡하므로, 첫 시험 등수 순으로 정렬해서 조건 하나를 없앱니다. 정렬 후 앞에서부터 처리하면 이미 처리한 학생들은 항상 첫 등수가 더 좋으므로, 나머지 두 등수만 확인하면 됩니다.

어떤 학생이 굉장한지 판단하려면, 이미 처리한 학생들 중 두 번째와 세 번째 등수가 모두 더 좋은 학생이 있는지 확인해야 합니다. 세그먼트 트리를 사용해 두 번째 등수가 더 좋은 구간에서 세 번째 등수의 최솟값을 관리합니다.

현재 학생보다 두 번째 등수가 좋은 구간에서 세 번째 등수의 최솟값을 쿼리합니다. 이 값이 현재 학생의 세 번째 등수보다 크면, 두 조건을 모두 만족하는 학생이 없으므로 굉장한 학생입니다. 판단 후에는 현재 학생의 정보를 트리에 반영합니다.

<br>

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    const int INF = 1_000_000_000;
    static int n;
    static int[] seg = Array.Empty<int>();

    static int Query(int node, int l, int r, int ql, int qr) {
      if (qr < l || r < ql)
        return INF;
      if (ql <= l && r <= qr)
        return seg[node];
      var mid = (l + r) >> 1;
      var left = Query(node << 1, l, mid, ql, qr);
      var right = Query(node << 1 | 1, mid + 1, r, ql, qr);
      return left < right ? left : right;
    }

    static void Update(int node, int l, int r, int pos, int val) {
      if (pos < l || pos > r)
        return;
      if (l == r) {
        seg[node] = Math.Min(seg[node], val);
        return;
      }
      var mid = (l + r) >> 1;
      Update(node << 1, l, mid, pos, val);
      Update(node << 1 | 1, mid + 1, r, pos, val);
      seg[node] = Math.Min(seg[node << 1], seg[node << 1 | 1]);
    }

    static void Main(string[] args) {
      n = int.Parse(Console.ReadLine()!);
      var rank = new int[n + 1, 3];

      for (var exam = 0; exam < 3; exam++) {
        var line = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
        for (var i = 0; i < n; i++) {
          var student = line[i];
          rank[student, exam] = i + 1;
        }
      }

      var arr = new int[n][];
      for (var s = 1; s <= n; s++)
        arr[rank[s, 0] - 1] = new int[] { rank[s, 1], rank[s, 2] };

      seg = new int[4 * (n + 2)];
      for (var i = 0; i < seg.Length; i++)
        seg[i] = INF;

      var ans = 0;
      foreach (var stu in arr) {
        var second = stu[0];
        var third = stu[1];
        var best = Query(1, 1, n, 1, second);
        if (best > third)
          ans++;
        Update(1, 1, n, second, third);
      }

      Console.WriteLine(ans);
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

const int INF = 1e9;
int n;
vi seg;

int query(int node, int l, int r, int ql, int qr) {
  if (qr < l || r < ql)
    return INF;
  if (ql <= l && r <= qr)
    return seg[node];
  int mid = (l + r) >> 1;
  return min(query(node << 1, l, mid, ql, qr),
             query(node << 1 | 1, mid + 1, r, ql, qr));
}

void update(int node, int l, int r, int pos, int val) {
  if (pos < l || pos > r)
    return;
  if (l == r) {
    seg[node] = min(seg[node], val);
    return;
  }
  int mid = (l + r) >> 1;
  update(node << 1, l, mid, pos, val);
  update(node << 1 | 1, mid + 1, r, pos, val);
  seg[node] = min(seg[node << 1], seg[node << 1 | 1]);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  cin >> n;
  vector<array<int, 3>> rnk(n + 1);

  for (int exam = 0; exam < 3; exam++) {
    for (int i = 1; i <= n; i++) {
      int stu; cin >> stu;
      rnk[stu][exam] = i;
    }
  }

  vector<pii> arr(n);
  for (int s = 1; s <= n; s++) {
    int firstRank = rnk[s][0] - 1;
    arr[firstRank] = {rnk[s][1], rnk[s][2]};
  }

  seg.assign(4 * (n + 2), INF);
  int ans = 0;
  for (auto [second, third] : arr) {
    int best = query(1, 1, n, 1, second);
    if (best > third)
      ans++;
    update(1, 1, n, second, third);
  }

  cout << ans << "\n";

  return 0;
}
```
