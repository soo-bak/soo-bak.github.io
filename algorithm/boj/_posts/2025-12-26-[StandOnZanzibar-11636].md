---
layout: single
title: "[백준 11636] Stand on Zanzibar (C#, C++) - soo:bak"
date: "2025-12-26 01:04:14 +0900"
description: 연속 연도의 최대 번식치를 넘는 증가량을 합산하는 문제
---

## 문제 링크
[11636번 - Stand on Zanzibar](https://www.acmicpc.net/problem/11636)

## 설명
거북이 수열이 주어질 때 외부 유입의 최소 합을 구하는 문제입니다.

<br>

## 접근법
먼저 연속한 두 해의 값 차이를 확인합니다.

다음으로 현재 값이 이전 값의 두 배를 넘는 경우, 초과분이 유입 최소치가 됩니다.

이후 그 초과분을 누적합니다.

마지막으로 0이 나올 때까지 처리한 합을 출력합니다.

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
    var t = int.Parse(parts[idx++]);
    var sb = new StringBuilder();

    for (var tc = 0; tc < t; tc++) {
      var prev = int.Parse(parts[idx++]);
      var sum = 0;
      while (true) {
        var cur = int.Parse(parts[idx++]);
        if (cur == 0) break;
        if (cur > prev * 2) sum += cur - prev * 2;
        prev = cur;
      }
      sb.AppendLine(sum.ToString());
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
    int prev; cin >> prev;
    int sum = 0;
    while (true) {
      int cur; cin >> cur;
      if (cur == 0) break;
      if (cur > prev * 2) sum += cur - prev * 2;
      prev = cur;
    }
    cout << sum << "\n";
  }

  return 0;
}
```
