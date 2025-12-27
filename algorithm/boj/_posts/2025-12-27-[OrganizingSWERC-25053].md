---
layout: single
title: "[백준 25053] Organizing SWERC (C#, C++) - soo:bak"
date: "2025-12-27 07:45:00 +0900"
description: 난이도 1~10별 최고 미적 점수를 더하거나 부족하면 MOREPROBLEMS을 출력하는 문제
---

## 문제 링크
[25053번 - Organizing SWERC](https://www.acmicpc.net/problem/25053)

## 설명
각 문제마다 아름다움 점수와 난이도가 주어집니다. 난이도 1부터 10까지 각각에서 가장 아름다운 문제를 하나씩 골라 총합을 구하는 문제입니다.

<br>

## 접근법
난이도 1~10에 대해 최고 미적 점수를 저장합니다. 입력을 순회하며 갱신하고, 마지막에 모두 채워졌는지 확인해 합계 또는 MOREPROBLEMS를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split((char[])null, StringSplitOptions.RemoveEmptyEntries);
    var idx = 0;
    var t = int.Parse(parts[idx++]);
    var sb = new StringBuilder();

    for (var cs = 0; cs < t; cs++) {
      var n = int.Parse(parts[idx++]);
      var best = new int[11];
      for (var i = 0; i < n; i++) {
        var b = int.Parse(parts[idx++]);
        var d = int.Parse(parts[idx++]);
        if (b > best[d]) best[d] = b;
      }
      var ok = true;
      var sum = 0;
      for (var d = 1; d <= 10; d++) {
        if (best[d] == 0) { ok = false; break; }
        sum += best[d];
      }
      sb.AppendLine(ok ? sum.ToString() : "MOREPROBLEMS");
    }

    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int n; cin >> n;
    vi best(11, 0);
    for (int i = 0; i < n; i++) {
      int b, d; cin >> b >> d;
      best[d] = max(best[d], b);
    }
    bool ok = true;
    int sum = 0;
    for (int d = 1; d <= 10; d++) {
      if (best[d] == 0) { ok = false; break; }
      sum += best[d];
    }
    if (!ok) cout << "MOREPROBLEMS\n";
    else cout << sum << "\n";
  }

  return 0;
}
```
