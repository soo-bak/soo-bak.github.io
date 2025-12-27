---
layout: single
title: "[백준 8320] 직사각형을 만드는 방법 (C#, C++) - soo:bak"
date: "2025-12-09 10:32:00 +0900"
description: 변 길이 1 정사각형 n개로 만들 수 있는 직사각형 개수를 세는 백준 8320번 직사각형을 만드는 방법 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 8320
  - C#
  - C++
  - 알고리즘
keywords: "백준 8320, 백준 8320번, BOJ 8320, MakeRectangles, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[8320번 - 직사각형을 만드는 방법](https://www.acmicpc.net/problem/8320)

## 설명
n개의 정사각형을 빈틈없이 배열하여 만들 수 있는 직사각형의 개수를 구하는 문제입니다. 회전해서 같은 모양이 되는 직사각형은 하나로 셉니다.

<br>

## 접근법
가로 길이를 1부터 n까지 시도하면서, 각 가로 길이에 대해 세로 길이를 가로 이상으로 늘려가며 넓이가 n 이하인 경우를 모두 셉니다. 가로가 세로 이하인 경우만 세므로 중복 없이 모든 직사각형을 셀 수 있습니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var cnt = 0;
    for (var i = 1; i <= n; i++) {
      for (var j = i; i * j <= n; j++)
        cnt++;
    }
    Console.WriteLine(cnt);
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
  int cnt = 0;
  for (int i = 1; i <= n; i++) {
    for (int j = i; i * j <= n; j++)
      cnt++;
  }
  cout << cnt << "\n";

  return 0;
}
```
