---
layout: single
title: "[백준 25830] Microwave Mishap (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: 분:초를 시간:분으로 잘못 해석했을 때 초과 조리 시간을 구하는 문제
---

## 문제 링크
[25830번 - Microwave Mishap](https://www.acmicpc.net/problem/25830)

## 설명
전자레인지에 MM:SS를 입력했지만 실제로는 HH:MM으로 처리됩니다. 기대했던 조리 시간(분·초)과 실제 조리 시간(시·분)의 차이를 HH:MM:SS 형식으로 출력하는 문제입니다.

<br>

## 접근법
입력된 MM:SS를 분과 초로 파싱합니다. 기대했던 조리 시간은 분을 60으로, 초를 그대로 더한 값이고, 실제 조리 시간은 분을 시간으로, 초를 분으로 해석하므로 분에 3600을, 초에 60을 곱한 값입니다.

두 시간의 차이를 초 단위로 구한 뒤, 3600으로 나누어 시를, 나머지를 60으로 나누어 분을, 최종 나머지를 초로 변환하여 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split(':');
    var m = int.Parse(parts[0]);
    var s = int.Parse(parts[1]);

    var expected = m * 60 + s;
    var actual = m * 3600 + s * 60;
    var diff = actual - expected;

    var hh = diff / 3600;
    diff %= 3600;
    var mm = diff / 60;
    var ss = diff % 60;

    Console.WriteLine($"{hh:D2}:{mm:D2}:{ss:D2}");
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

  string input; cin >> input;
  int m = stoi(input.substr(0, 2));
  int s = stoi(input.substr(3, 2));

  int expected = m * 60 + s;
  int actual = m * 3600 + s * 60;
  int diff = actual - expected;

  int hh = diff / 3600;
  diff %= 3600;
  int mm = diff / 60;
  int ss = diff % 60;

  cout << setfill('0') << setw(2) << hh << ":"
       << setw(2) << mm << ":" << setw(2) << ss << "\n";

  return 0;
}
```
