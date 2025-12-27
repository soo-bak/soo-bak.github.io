---
layout: single
title: "[백준 20978] 共通要素 (Common Elements) (C#, C++) - soo:bak"
date: "2025-12-27 00:35:00 +0900"
description: 두 수열에 공통으로 등장하는 정수를 오름차순으로 출력하는 백준 20978번 共通要素 (Common Elements) 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 20978
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 20978, 백준 20978번, BOJ 20978, CommonElements, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[20978번 - 共通要素 (Common Elements)](https://www.acmicpc.net/problem/20978)

## 설명
길이 N의 수열 A와 길이 M의 수열 B가 주어질 때, 두 수열에 모두 등장하는 정수를 오름차순으로 한 번씩 출력하는 문제입니다.

<br>

## 접근법
두 수열의 값을 기록해 둔 뒤, 둘 다 등장한 수만 모아 오름차순으로 출력합니다.

값의 범위가 1~100이므로 등장 여부를 배열로 표시하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split((char[])null, StringSplitOptions.RemoveEmptyEntries);
    var idx = 0;
    var n = int.Parse(parts[idx++]);
    var m = int.Parse(parts[idx++]);

    var seenA = new bool[101];
    var seenB = new bool[101];

    for (var i = 0; i < n; i++) {
      var v = int.Parse(parts[idx++]);
      seenA[v] = true;
    }
    for (var i = 0; i < m; i++) {
      var v = int.Parse(parts[idx++]);
      seenB[v] = true;
    }

    var sb = new StringBuilder();
    for (var v = 1; v <= 100; v++) {
      if (seenA[v] && seenB[v]) sb.AppendLine(v.ToString());
    }

    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<bool> vb;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;
  vb seenA(101, false), seenB(101, false);

  for (int i = 0; i < n; i++) {
    int v; cin >> v;
    seenA[v] = true;
  }
  for (int i = 0; i < m; i++) {
    int v; cin >> v;
    seenB[v] = true;
  }

  for (int v = 1; v <= 100; v++) {
    if (seenA[v] && seenB[v])
      cout << v << "\n";
  }

  return 0;
}
```
