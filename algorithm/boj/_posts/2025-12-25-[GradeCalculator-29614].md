---
layout: single
title: "[백준 29614] 학점계산프로그램 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: 등급 문자열을 해석해 평균 학점을 구하는 문제
---

## 문제 링크
[29614번 - 학점계산프로그램](https://www.acmicpc.net/problem/29614)

## 설명
등급 문자열 S가 주어질 때, 각 과목의 학점을 평균 내어 출력하는 문제입니다.

<br>

## 접근법
문자열을 왼쪽부터 읽으며 `+`가 붙는지 확인해 학점 값을 누적합니다.  
학점은 0.5 단위이므로 2배 값으로 합산한 뒤 평균을 계산합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    var sum2 = 0;
    var cnt = 0;

    for (var i = 0; i < s.Length; ) {
      var c = s[i];
      var plus = c != 'F' && i + 1 < s.Length && s[i + 1] == '+';

      if (c == 'A') sum2 += plus ? 9 : 8;
      else if (c == 'B') sum2 += plus ? 7 : 6;
      else if (c == 'C') sum2 += plus ? 5 : 4;
      else if (c == 'D') sum2 += plus ? 3 : 2;
      else sum2 += 0;

      cnt++;
      i += plus ? 2 : 1;
    }

    var avg = sum2 / 2.0 / cnt;
    Console.WriteLine($"{avg:F5}");
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

  string s; cin >> s;
  int sum2 = 0, cnt = 0;

  for (int i = 0; i < (int)s.size(); ) {
    char c = s[i];
    bool plus = c != 'F' && i + 1 < (int)s.size() && s[i + 1] == '+';

    if (c == 'A') sum2 += plus ? 9 : 8;
    else if (c == 'B') sum2 += plus ? 7 : 6;
    else if (c == 'C') sum2 += plus ? 5 : 4;
    else if (c == 'D') sum2 += plus ? 3 : 2;
    else sum2 += 0;

    cnt++;
    i += plus ? 2 : 1;
  }

  double avg = sum2 / 2.0 / cnt;
  cout << fixed << setprecision(5) << avg << "\n";

  return 0;
}
```
