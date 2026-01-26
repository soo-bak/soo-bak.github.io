---
layout: single
title: "[백준 17931] Greedily Increasing Subsequence (C#, C++) - soo:bak"
date: "2026-01-26 21:41:00 +0900"
description: "백준 17931번 C#, C++ 풀이 - 가장 왼쪽에서부터 더 큰 값을 고르는 GIS를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 17931
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 17931, 백준 17931번, BOJ 17931, Greedily Increasing Subsequence, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17931번 - Greedily Increasing Subsequence](https://www.acmicpc.net/problem/17931)

## 설명
첫 원소를 g₁으로 두고, 이후에는 바로 앞에 뽑은 값보다 큰 값 중 가장 왼쪽에 있는 원소를 차례로 고르는 GIS(Greedily Increasing Subsequence)를 구하는 문제입니다. 더 이상 큰 값이 없으면 종료합니다.

<br>

## 접근법
배열을 한 번 순회하며 직전에 선택한 값 last를 저장합니다.

처음 원소를 무조건 선택하고, 이후 원소가 last보다 크면 결과에 추가하고 last를 갱신합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var input = Console.In.ReadToEnd().Split((char[])null, StringSplitOptions.RemoveEmptyEntries);
    var idx = 0;
    var n = int.Parse(input[idx++]);

    var res = new int[n];
    var len = 0;

    int last = int.Parse(input[idx++]);
    res[len++] = last;
    for (int i = 1; i < n; i++) {
      int v = int.Parse(input[idx++]);
      if (v > last) {
        res[len++] = v;
        last = v;
      }
    }

    var sb = new StringBuilder();
    sb.Append(len).Append('\n');
    for (int i = 0; i < len; i++) {
      if (i > 0) sb.Append(' ');
      sb.Append(res[i]);
    }
    Console.Write(sb.ToString());
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  vector<int> ans;
  ans.reserve(n);

  int last; cin >> last;
  ans.push_back(last);
  for (int i = 1; i < n; i++) {
    int v; cin >> v;
    if (v > last) {
      ans.push_back(v);
      last = v;
    }
  }

  cout << ans.size() << "\n";
  for (size_t i = 0; i < ans.size(); i++) {
    if (i) cout << ' ';
    cout << ans[i];
  }
  cout << "\n";

  return 0;
}
```
