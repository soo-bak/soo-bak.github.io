---
layout: single
title: "[백준 18309] Extreme Temperatures (C#, C++) - soo:bak"
date: "2025-12-21 20:42:00 +0900"
description: 여러 줄의 측정 데이터에서 전체 최저·최고 기온을 찾는 문제
---

## 문제 링크
[18309번 - Extreme Temperatures](https://www.acmicpc.net/problem/18309)

## 설명
여러 날의 기온 측정 데이터에서 전체 최저 기온과 최고 기온을 구하는 문제입니다.

<br>

## 접근법
각 줄의 첫 번째 토큰은 날짜이고 나머지는 기온 측정값입니다. 입력이 끝날 때까지 줄을 읽으면서 날짜를 건너뛰고 기온값들을 순회합니다. 각 값을 현재까지의 최솟값, 최댓값과 비교하며 갱신합니다. 모든 입력을 처리한 뒤 최종 결과를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var mn = int.MaxValue;
    var mx = int.MinValue;

    string? line;
    while ((line = Console.ReadLine()) != null) {
      var parts = line.Split(' ', StringSplitOptions.RemoveEmptyEntries);
      for (var i = 1; i < parts.Length; i++) {
        var val = int.Parse(parts[i]);
        if (val < mn) mn = val;
        if (val > mx) mx = val;
      }
    }

    Console.WriteLine($"{mn} {mx}");
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

  string line;
  int mn = 1e9, mx = -1e9;
  while (getline(cin, line)) {
    if (line.empty()) continue;

    stringstream ss(line);
    string date; ss >> date;

    int val;
    while (ss >> val) {
      mn = min(mn, val);
      mx = max(mx, val);
    }
  }

  if (mn != (int)1e9) cout << mn << " " << mx << "\n";

  return 0;
}
```
