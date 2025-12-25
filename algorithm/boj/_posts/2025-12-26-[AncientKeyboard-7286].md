---
layout: single
title: "[백준 7286] Ancient Keyboard (C#, C++) - soo:bak"
date: "2025-12-26 01:55:00 +0900"
description: 시간에 따른 LED 개수로 출력 문자열을 만드는 문제
---

## 문제 링크
[7286번 - Ancient Keyboard](https://www.acmicpc.net/problem/7286)

## 설명
각 키의 LED가 켜지는 구간이 주어질 때 시간 순서대로 출력되는 문자를 구하는 문제입니다.

<br>

## 접근법
먼저 각 키가 켜지는 구간을 시간 축에 표시해 각 시각의 켜진 개수를 알 수 있게 합니다.

다음으로 시간 순서대로 켜진 개수를 확인하고, 1 이상일 때만 해당 개수에 맞는 문자를 이어 붙입니다.

마지막으로 만들어진 문자열을 출력합니다.

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
      var n = int.Parse(parts[idx++]);
      var diff = new int[1002];
      var maxB = 0;

      for (var i = 0; i < n; i++) {
        idx++;
        var a = int.Parse(parts[idx++]);
        var b = int.Parse(parts[idx++]);
        diff[a] += 1;
        diff[b] -= 1;
        if (b > maxB) maxB = b;
      }

      var cur = 0;
      var outSb = new StringBuilder();
      for (var time = 0; time < maxB; time++) {
        cur += diff[time];
        if (cur > 0) outSb.Append((char)('A' + cur - 1));
      }

      sb.AppendLine(outSb.ToString());
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

  for (int tc = 0; tc < t; tc++) {
    int n; cin >> n;

    vi diff(1002, 0);
    int maxB = 0;

    for (int i = 0; i < n; i++) {
      char ch; int a, b; cin >> ch >> a >> b;
      diff[a] += 1;
      diff[b] -= 1;
      if (b > maxB) maxB = b;
    }

    int cur = 0;
    string out;
    for (int time = 0; time < maxB; time++) {
      cur += diff[time];
      if (cur > 0) out.push_back(char('A' + cur - 1));
    }

    cout << out << "\n";
  }

  return 0;
}
```
