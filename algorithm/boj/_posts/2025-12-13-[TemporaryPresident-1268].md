---
layout: single
title: "[백준 1268] 임시 반장 정하기 (C#, C++) - soo:bak"
date: "2025-12-13 05:01:00 +0900"
description: 각 학생별로 한 번이라도 같은 반이었던 학생 수를 세어 최댓값을 가진 학생 번호를 출력하는 백준 1268번 임시 반장 정하기 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1268
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 1268, 백준 1268번, BOJ 1268, TemporaryPresident, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1268번 - 임시 반장 정하기](https://www.acmicpc.net/problem/1268)

## 설명
한 번이라도 같은 반이었던 학생 수가 가장 많은 학생 번호를 구하는 문제입니다.

<br>

## 접근법
각 학생 쌍에 대해 1~5학년 중 한 학년이라도 같은 반이면 같은 반으로 간주합니다.

모든 쌍을 검사하여 각 학생별로 같은 반이었던 학생 수를 셉니다.

최댓값을 가진 학생 번호를 출력하고, 동점이면 번호가 작은 학생을 선택합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var cls = new int[n, 5];
    for (var i = 0; i < n; i++) {
      var line = Console.ReadLine()!.Split();
      for (var k = 0; k < 5; k++) cls[i, k] = int.Parse(line[k]);
    }

    var best = 0; var bestCnt = -1;
    for (var i = 0; i < n; i++) {
      var cnt = 0;
      for (var j = 0; j < n; j++) {
        if (i == j) continue;
        for (var k = 0; k < 5; k++) {
          if (cls[i, k] == cls[j, k]) { cnt++; break; }
        }
      }
      if (cnt > bestCnt) { bestCnt = cnt; best = i + 1; }
    }

    Console.WriteLine(best);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;
typedef vector<vi> vvi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vvi cls(n, vi(5));
  for (int i = 0; i < n; i++)
    for (int k = 0; k < 5; k++) cin >> cls[i][k];

  int best = 0, bestCnt = -1;
  for (int i = 0; i < n; i++) {
    int cnt = 0;
    for (int j = 0; j < n; j++) if (i != j) {
      for (int k = 0; k < 5; k++) {
        if (cls[i][k] == cls[j][k]) { cnt++; break; }
      }
    }
    if (cnt > bestCnt) { bestCnt = cnt; best = i + 1; }
  }

  cout << best << "\n";

  return 0;
}
```
