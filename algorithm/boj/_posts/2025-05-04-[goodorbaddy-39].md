---
layout: single
title: "[백준 4447] 좋은놈 나쁜놈 (C#, C++) - soo:bak"
date: "2025-05-04 18:21:00 +0900"
description: 이름에 포함된 g와 b의 개수를 비교하여 좋은지 나쁜지 중립인지 판별하는 문자열 분석 문제, 백준 4447번 좋은놈 나쁜놈 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[4447번 - 좋은놈 나쁜놈](https://www.acmicpc.net/problem/4447)

## 설명
각 히어로의 이름이 주어졌을 때, 이름 속에 포함된 알파벳 `g`와 `b`의 개수를 비교하여

**g의 개수가 많으면 좋음, b의 개수가 많으면 나쁨, 같으면 중립**으로 판정하는 문제입니다.

<br>
대소문자를 구분하지 않으며, 공백이나 다른 문자는 무시합니다.<br>

<br>

## 접근법

- 테스트케이스 개수를 입력받고, 그만큼 이름을 입력받습니다.
- 각 이름 문자열에서 알파벳 `g` 또는 `G`, `b` 또는 `B`의 개수를 각각 카운트합니다.
  - `g`의 개수가 많으면 `"is GOOD"`
  - `b`가 많으면 `"is A BADDY"`
  - 같으면 `"is NEUTRAL"`<br>
- 결과에 따라 위 접미사를 이름 뒤에 이어 기준에 맞게 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    while (n-- > 0) {
      var name = Console.ReadLine();
      int g = 0, b = 0;
      foreach (char c in name) {
        if (c == 'g' || c == 'G') g++;
        else if (c == 'b' || c == 'B') b++;
      }
      Console.Write(name + " is ");
      if (g > b) Console.WriteLine("GOOD");
      else if (g < b) Console.WriteLine("A BADDY");
      else Console.WriteLine("NEUTRAL");
    }
  }
}
```

<br>

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  cin.ignore();
  while (t--) {
    string s; getline(cin, s);
    int g = 0, b = 0;
    for (char c : s)
      if (tolower(c) == 'g') g++;
      else if (tolower(c) == 'b') b++;

    cout << s << " is " << (g > b ? "GOOD" : g < b ? "A BADDY" : "NEUTRAL") << "\n";
  }

  return 0;
}
```
