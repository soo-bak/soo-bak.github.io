---
layout: single
title: "[백준 31776] 예비 소집 결과 보고서 (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: 해결한 문제가 앞에서부터 연속이고 시간 순서가 맞는 팀의 수를 세는 문제
---

## 문제 링크
[31776번 - 예비 소집 결과 보고서](https://www.acmicpc.net/problem/31776)

## 설명
세 문제의 해결 시간이 주어질 때, 앞번호부터 순서대로 풀었고 최소 한 문제를 해결한 팀의 수를 구하는 문제입니다.

<br>

## 접근법
해결한 문제는 1번부터 연속된 접두사여야 합니다. 따라서 첫 -1이 나온 뒤에 해결 시간이 있으면 탈락입니다. 또한 해결한 구간의 시간은 비내림차순이어야 하므로 인접한 시간들이 감소하면 탈락입니다. 조건을 만족하는 팀만 카운트합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var count = 0;

    for (var i = 0; i < n; i++) {
      var parts = Console.ReadLine()!.Split();
      var t = new int[3];
      for (var j = 0; j < 3; j++)
        t[j] = int.Parse(parts[j]);

      var k = 0;
      while (k < 3 && t[k] != -1)
        k++;
      if (k == 0) continue;

      var ok = true;
      for (var j = k; j < 3; j++) {
        if (t[j] != -1) ok = false;
      }
      for (var j = 1; j < k; j++) {
        if (t[j - 1] > t[j]) ok = false;
      }

      if (ok) count++;
    }

    Console.WriteLine(count);
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
  int count = 0;

  for (int i = 0; i < n; i++) {
    int t[3];
    for (int j = 0; j < 3; j++)
      cin >> t[j];

    int k = 0;
    while (k < 3 && t[k] != -1)
      k++;
    if (k == 0) continue;

    bool ok = true;
    for (int j = k; j < 3; j++) {
      if (t[j] != -1) ok = false;
    }

    for (int j = 1; j < k; j++) {
      if (t[j - 1] > t[j]) ok = false;
    }

    if (ok) count++;
  }

  cout << count << "\n";

  return 0;
}
```
