---
layout: single
title: "[백준 21614] Secret Instructions (C#, C++) - soo:bak"
date: "2025-12-21 20:42:00 +0900"
description: "백준 21614번 C#, C++ 풀이 - 다섯 자리 코드에서 방향 규칙을 해석해 좌우와 이동 칸수를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 21614
  - C#
  - C++
  - 알고리즘
keywords: "백준 21614, 백준 21614번, BOJ 21614, SecretInstructions, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[21614번 - Secret Instructions](https://www.acmicpc.net/problem/21614)

## 설명
다섯 자리 코드에서 방향 규칙을 해석해 좌우와 이동 칸수를 출력하는 문제입니다.

<br>

## 접근법
다섯 자리 코드에서 앞 두 자릿수의 합이 홀수이면 왼쪽, 짝수이면 오른쪽으로 회전합니다. 다만 합이 0인 경우는 이전 지시어의 방향을 그대로 따릅니다. 뒤 세 자릿수는 이동할 칸수입니다.

종료 코드 99999가 나올 때까지 지시어를 하나씩 읽으면서 방향과 칸수를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var prevDir = "";

    while (true) {
      var s = Console.ReadLine();
      if (s == null || s == "99999") break;

      var d1 = s[0] - '0';
      var d2 = s[1] - '0';
      var sum = d1 + d2;

      var dir = "";
      if (sum == 0) dir = prevDir;
      else if ((sum & 1) == 1) dir = "left";
      else dir = "right";

      prevDir = dir;
      var steps = int.Parse(s.Substring(2));
      Console.WriteLine($"{dir} {steps}");
    }
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

  string s, prevDir;

  while (cin >> s) {
    if (s == "99999") break;

    int d1 = s[0] - '0';
    int d2 = s[1] - '0';
    int sum = d1 + d2;

    string dir;
    if (sum == 0) dir = prevDir;
    else if (sum % 2 == 1) dir = "left";
    else dir = "right";

    prevDir = dir;
    int steps = stoi(s.substr(2));
    cout << dir << ' ' << steps << '\n';
  }

  return 0;
}
```
