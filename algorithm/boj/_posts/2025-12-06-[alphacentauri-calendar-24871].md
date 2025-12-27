---
layout: single
title: "[백준 24871] Календарь на Альфе Центавра (C#, C++) - soo:bak"
date: "2025-12-06 17:52:00 +0900"
description: 주어진 날짜의 요일을 계산하는 백준 24871번 알파 센타우리 달력 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 24871
  - C#
  - C++
  - 알고리즘
keywords: "백준 24871, 백준 24871번, BOJ 24871, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[24871번 - Календарь на Альфе Центавра](https://www.acmicpc.net/problem/24871)

## 설명
알파 센타우리 행성의 달력이 주어집니다. 1년은 m개월이고 각 달은 d일입니다. 1주는 w일이며 요일은 a부터 연속된 소문자로 표현됩니다.

1년 1월 1일의 요일이 a일 때, 주어진 날짜의 요일을 구하는 문제입니다.

<br>

## 접근법
먼저, 1년 1월 1일을 기준으로 주어진 날짜까지의 경과 일수를 계산합니다. 연도에서 1을 빼고 월 수와 일 수를 곱한 값, 월에서 1을 빼고 일 수를 곱한 값, 그리고 일에서 1을 뺀 값을 모두 더합니다.

다음으로, 경과 일수를 주 길이로 나눈 나머지가 요일 인덱스가 됩니다. a에 이 인덱스를 더하면 해당 요일 문자가 됩니다.

경과 일수가 매우 커질 수 있으므로 64비트 정수를 사용합니다.

<br>

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var f = Console.ReadLine()!.Split();
      var d = long.Parse(f[0]);
      var m = long.Parse(f[1]);
      var w = long.Parse(f[2]);
      var s = Console.ReadLine()!.Split();
      var i = long.Parse(s[0]);
      var j = long.Parse(s[1]);
      var k = long.Parse(s[2]);

      var offset = (k - 1) * m * d + (j - 1) * d + (i - 1);
      var idx = offset % w;
      var ans = (char)('a' + idx);
      Console.WriteLine(ans);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll d, m, w; cin >> d >> m >> w;
  ll i, j, k; cin >> i >> j >> k;

  ll offset = (k - 1) * m * d + (j - 1) * d + (i - 1);
  ll idx = offset % w;
  char ans = char('a' + idx);
  cout << ans << "\n";

  return 0;
}
```
