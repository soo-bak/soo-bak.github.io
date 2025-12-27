---
layout: single
title: "[백준 33488] 아름다운 수열 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 33488번 C#, C++ 풀이 - 1부터 N까지 순서대로 출력해 조건을 만족하는 순열을 만드는 문제"
tags:
  - 백준
  - BOJ
  - 33488
  - C#
  - C++
  - 알고리즘
  - 애드혹
  - 구성적
keywords: "백준 33488, 백준 33488번, BOJ 33488, BeautifulSequence, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[33488번 - 아름다운 수열](https://www.acmicpc.net/problem/33488)

## 설명
조건을 만족하는 길이 N의 순열이 존재하면 출력하고, 없다면 NO를 출력하는 문제입니다.

<br>

## 접근법
순열을 1부터 N까지 그대로 두면, 인덱스 간 거리가 소수일 때 값의 차이도 같은 소수가 됩니다.  
따라서 모든 N에서 조건을 만족하는 순열이 존재하므로 항상 YES와 1부터 N까지를 출력합니다.

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

    for (var caseNo = 0; caseNo < t; caseNo++) {
      var n = int.Parse(parts[idx++]);
      sb.AppendLine("YES");
      for (var i = 1; i <= n; i++) {
        if (i > 1) sb.Append(' ');
        sb.Append(i);
      }
      sb.AppendLine();
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
    cout << "YES\n";
    for (int i = 1; i <= n; i++) {
      if (i > 1) cout << ' ';
      cout << i;
    }
    cout << "\n";
  }

  return 0;
}
```
