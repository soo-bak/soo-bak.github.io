---
layout: single
title: "[백준 18884] New Year and Naming (C#, C++) - soo:bak"
date: "2025-12-26 01:06:08 +0900"
description: "백준 18884번 C#, C++ 풀이 - 두 문자열 순환을 합쳐 연도 이름을 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 18884
  - C#
  - C++
  - 알고리즘
keywords: "백준 18884, 백준 18884번, BOJ 18884, NewYearAndNaming, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[18884번 - New Year and Naming](https://www.acmicpc.net/problem/18884)

## 설명
두 문자열 배열을 순환하며 이어 붙인 결과로 연도 이름을 구하는 문제입니다.

<br>

## 접근법
먼저 연도는 1부터 시작하므로 인덱스를 0부터 계산하도록 1을 뺍니다.

다음으로 두 배열에서 각각 나머지 연산으로 위치를 결정합니다.

마지막으로 두 문자열을 이어 붙여 출력합니다.

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
    var m = int.Parse(parts[idx++]);

    var s = new string[n];
    for (var i = 0; i < n; i++)
      s[i] = parts[idx++];

    var t = new string[m];
    for (var i = 0; i < m; i++)
      t[i] = parts[idx++];

    var q = int.Parse(parts[idx++]);
    var sb = new StringBuilder();
    for (var i = 0; i < q; i++) {
      var y = int.Parse(parts[idx++]) - 1;
      var a = s[(int)(y % n)];
      var b = t[(int)(y % m)];
      sb.Append(a).Append(b).AppendLine();
    }

    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<string> vs;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;

  vs s(n), t(m);
  for (int i = 0; i < n; i++)
    cin >> s[i];
  for (int i = 0; i < m; i++)
    cin >> t[i];

  int q; cin >> q;
  for (int i = 0; i < q; i++) {
    int y; cin >> y;
    y--;
    cout << s[y % n] << t[y % m] << "\n";
  }

  return 0;
}
```
