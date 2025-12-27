---
layout: single
title: "[백준 19155] Copying Homework (C#, C++) - soo:bak"
date: "2025-12-26 01:00:35 +0900"
description: "백준 19155번 C#, C++ 풀이 - 각 값을 반대쪽 값으로 치환해 조건을 만족하는 순열을 만드는 문제"
tags:
  - 백준
  - BOJ
  - 19155
  - C#
  - C++
  - 알고리즘
keywords: "백준 19155, 백준 19155번, BOJ 19155, CopyingHomework, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[19155번 - Copying Homework](https://www.acmicpc.net/problem/19155)

## 설명
주어진 순열 A에 대해 차이가 충분히 큰 다른 순열을 만들어 출력하는 문제입니다.

<br>

## 접근법
먼저 1과 N, 2와 N-1처럼 값의 반대 위치를 서로 대응시키는 치환을 사용합니다.

다음으로 이 치환은 항상 새로운 순열을 만들고, 각 위치의 변화량이 고정되므로 전체 차이 합도 일정하게 유지됩니다.

마지막으로 이 합은 N 이상이므로 조건을 만족하는 순열을 출력할 수 있습니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var n = int.Parse(parts[idx++]);

    var sb = new StringBuilder();
    for (var i = 0; i < n; i++) {
      var a = int.Parse(parts[idx++]);
      var b = n + 1 - a;
      if (i > 0) sb.Append(' ');
      sb.Append(b);
    }

    Console.WriteLine(sb.ToString());
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
  for (int i = 0; i < n; i++) {
    int a; cin >> a;
    int b = n + 1 - a;
    if (i > 0) cout << ' ';
    cout << b;
  }
  cout << "\n";

  return 0;
}
```
