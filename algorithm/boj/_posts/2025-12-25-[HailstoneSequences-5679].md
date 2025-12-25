---
layout: single
title: "[백준 5679] Hailstone Sequences (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: 하일스톤 수열에서 최댓값을 찾는 문제
---

## 문제 링크
[5679번 - Hailstone Sequences](https://www.acmicpc.net/problem/5679)

## 설명
주어진 시작값으로 하일스톤 수열을 만들 때, 등장하는 값 중 최댓값을 구하는 문제입니다.

<br>

## 접근법
현재 값이 1이 될 때까지 규칙대로 다음 값을 만들며 최댓값을 갱신합니다.  
모든 입력에 대해 이 과정을 반복하면 됩니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var sb = new StringBuilder();
    while (true) {
      var line = Console.ReadLine();
      if (line == null) break;
      var h = int.Parse(line);
      if (h == 0) break;

      var maxVal = h;
      var cur = h;
      while (cur != 1) {
        if (cur % 2 == 0) cur /= 2;
        else cur = cur * 3 + 1;
        if (cur > maxVal) maxVal = cur;
      }

      sb.AppendLine(maxVal.ToString());
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

  int h;
  while (cin >> h) {
    if (h == 0) break;
    int cur = h;
    int maxVal = h;
    while (cur != 1) {
      if (cur % 2 == 0) cur /= 2;
      else cur = cur * 3 + 1;
      if (cur > maxVal) maxVal = cur;
    }
    cout << maxVal << "\n";
  }

  return 0;
}
```
