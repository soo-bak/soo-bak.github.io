---
layout: single
title: "[백준 31215] 이상한 섞기 연산 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 31215번 C#, C++ 풀이 - 이상한 섞기 연산 후 1의 위치를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 31215
  - C#
  - C++
  - 알고리즘
  - 애드혹
keywords: "백준 31215, 백준 31215번, BOJ 31215, StrangeShuffleOperation, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[31215번 - 이상한 섞기 연산](https://www.acmicpc.net/problem/31215)

## 설명
1부터 n까지 k-교환을 수행한 뒤, 값 1이 위치한 인덱스를 출력하는 문제입니다.

<br>

## 접근법
값 1은 처음에 인덱스 1에 있습니다.  
인덱스 1과의 교환은 홀수 k에서만 발생하며, 가장 처음 가능한 교환은 k=3입니다.  
한 번 인덱스 3으로 이동하면 3은 2의 거듭제곱수가 아니므로 이후 어떤 교환에도 등장하지 않아 위치가 고정됩니다.  
따라서 n이 1 또는 2이면 정답은 1, n이 3 이상이면 정답은 3입니다.

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
    var t = int.Parse(parts[idx++]);
    var sb = new StringBuilder();

    for (var i = 0; i < t; i++) {
      var n = int.Parse(parts[idx++]);
      sb.AppendLine(n < 3 ? "1" : "3");
    }

    Console.Write(sb);
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

  int t; cin >> t;
  while (t--) {
    int n; cin >> n;
    cout << (n < 3 ? 1 : 3) << "\n";
  }

  return 0;
}
```
