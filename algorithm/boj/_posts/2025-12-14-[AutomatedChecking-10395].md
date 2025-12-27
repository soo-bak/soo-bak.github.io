---
layout: single
title: "[백준 10395] Automated Checking Machine (C#, C++) - soo:bak"
date: "2025-12-14 09:03:00 +0900"
description: 동일 위치에서 두 커넥터의 핀 형태가 달라야 호환되므로 5자리 모두가 서로 다르면 Y, 하나라도 같으면 N을 출력하는 백준 10395번 문제의 C#/C++ 풀이
tags:
  - 백준
  - BOJ
  - 10395
  - C#
  - C++
  - 알고리즘
keywords: "백준 10395, 백준 10395번, BOJ 10395, AutomatedChecking, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10395번 - Automated Checking Machine](https://www.acmicpc.net/problem/10395)

## 설명
두 커넥터가 호환되는지 판별하는 문제입니다.

각 위치마다 한쪽은 플러그(1), 다른 쪽은 아웃렛(0)이어야 호환됩니다.

다섯 자리 모두 값이 달라야 하며, 하나라도 같으면 호환되지 않습니다.

<br>

## 접근법
두 줄의 5개 정수를 읽어 같은 위치에 같은 값이 있는지 확인합니다.

전부 다르면 Y, 아니면 N을 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var a = Console.ReadLine()!.Split();
    var b = Console.ReadLine()!.Split();
    var ok = true;
    for (var i = 0; i < 5; i++) {
      if (a[i] == b[i]) { ok = false; break; }
    }
    Console.WriteLine(ok ? "Y" : "N");
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

  int a[5], b[5];
  for (int i = 0; i < 5; i++) cin >> a[i];
  for (int i = 0; i < 5; i++) cin >> b[i];

  bool ok = true;
  for (int i = 0; i < 5; i++) {
    if (a[i] == b[i]) { ok = false; break; }
  }
  cout << (ok ? "Y" : "N") << "\n";

  return 0;
}
```
