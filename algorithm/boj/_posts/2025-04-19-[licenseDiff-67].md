---
layout: single
title: "[백준 1871] 좋은 자동차 번호판 (C#, C++) - soo:bak"
date: "2025-04-19 20:43:00 +0900"
description: 문자열을 해석하여 알파벳과 숫자의 차이를 계산하는 시뮬레이션 문제인 백준 1871번 좋은 자동차 번호판 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1871
  - C#
  - C++
  - 알고리즘
keywords: "백준 1871, 백준 1871번, BOJ 1871, licenseDiff, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1871번 - 좋은 자동차 번호판](https://www.acmicpc.net/problem/1871)

## 설명
**자동차 번호판의 알파벳 부분과 숫자 부분의 차이를 계산하여 조건에 따라 판별하는 문제**입니다.<br>
<br>

- 입력은 총 `N`개의 번호판이며, 각 번호판은 `"ABC-1234"`와 같은 형식으로 주어집니다.<br>
- 앞의 `3`글자는 대문자 알파벳, `-`를 기준으로 뒤의 `4`글자는 숫자입니다.<br>
- 알파벳 부분을 `26`진법처럼 해석하여 정수로 변환한 값을 계산합니다.<br>
- 변환된 알파벳 정수와 뒤의 숫자의 차이가 `100` 이하이면 `"nice"`, 그렇지 않으면 `"not nice"`를 출력합니다.<br>

### 접근법
- 알파벳 3글자를 각각 `26`진법 가중치로 처리합니다.<br>
  - 예를 들어 `"ABC"`는 $$0 \times 26^2 + 1 \times 26^1 + 2$$처럼 계산됩니다.<br>
- 숫자는 정수형으로 변환하여 차이를 계산합니다.<br>
- 이 차이가 `100` 이하인지 여부로 조건을 판별합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    int cntP = int.Parse(Console.ReadLine()!);
    for (int i = 0; i < cntP; i++) {
      var plate = Console.ReadLine()!;
      int first = 0;
      for (int j = 0; j < 3; j++) {
        int digit = plate[j] - 'A';
        for (int k = j + 1; k < 3; k++)
          digit *= 26;
        first += digit;
      }

      int second = int.Parse(plate.Substring(4));
      int diff = Math.Abs(first - second);
      if (diff > 100) Console.Write("not ");
      Console.WriteLine("nice");
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntP; cin >> cntP;
  for (int i = 0; i < cntP; i++) {
    string plate; cin >> plate;

    int f = 0;
    for (int j = 0; j < 3; j++) {
      int digit = plate[j] - 'A';
      for (int k = j + 1; k < 3; k++)
        digit *= 26;
      f += digit;
    }

    int s = stoi(plate.substr(4)), diff = abs(s - f);
    if (diff > 100) cout << "not ";
    cout << "nice\n";
  }

  return 0;
}
```
