---
layout: single
title: "[백준 34010] e-코너 시스템 테스트 (Easy) (C#, C++) - soo:bak"
date: "2025-12-26 00:47:49 +0900"
description: "백준 34010번 C#, C++ 풀이 - 최단 경로를 유지하며 피봇턴을 최대로 하는 값을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 34010
  - C#
  - C++
  - 알고리즘
keywords: "백준 34010, 백준 34010번, BOJ 34010, ECornerSystemTestEasy, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[34010번 - e-코너 시스템 테스트 (Easy)](https://www.acmicpc.net/problem/34010)

## 설명
격자에서 최단 경로로 이동하면서 피봇턴을 최대한 많이 수행할 때의 총 거리와 회전 횟수를 구하는 문제입니다.

<br>

## 접근법
먼저 모든 도로 길이가 1이므로 최단 경로는 오른쪽과 아래 이동 횟수만으로 결정됩니다.

다음으로 피봇턴은 이동 방향이 바뀔 때마다 1회 발생합니다.

이후 오른쪽과 아래 이동 횟수가 같으므로 방향을 번갈아 이동하면 회전을 최대화할 수 있습니다.

마지막으로 총 이동 횟수와 그에 따른 회전 횟수를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var dist = 2 * (n - 1);
    var turns = 2 * n - 3;
    Console.WriteLine($"{dist} {turns}");
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
  int dist = 2 * (n - 1);
  int turns = 2 * n - 3;
  cout << dist << " " << turns << "\n";
  return 0;
}
```
