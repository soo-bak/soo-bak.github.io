---
layout: single
title: "[백준 7572] 간지(干支) (C#, C++) - soo:bak"
date: "2025-04-19 00:04:00 +0900"
description: 육십갑자의 간지 표기법을 계산하여 연도에 대응되는 두 문자 코드를 출력하는 백준 7572번 간지 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 7572
  - C#
  - C++
  - 알고리즘
keywords: "백준 7572, 백준 7572번, BOJ 7572, zodiacCode, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[7572번 - 간지(干支)](https://www.acmicpc.net/problem/7572)

## 설명
**주어진 연도를 육십갑자(간지) 체계에 따라 두 자리 코드로 변환하는 문제**입니다.<br>
<br>

- 간지 표기법은 10간(갑을병정무기경신임계)과 12지(자축인묘진사오미신유술해)의 조합으로 이루어져 있습니다.<br>
- 이 문제에서는 알파벳 `'A'`부터 `'L'`까지 12지를, 숫자 `'0'`부터 `'9'`까지 10간을 사용하여 조합한 2자리 문자열을 출력합니다.<br>
- 기준 연도는 `2013년`, 기준 문자는 `'F9'`입니다.<br>
- 입력으로 연도 `Y`가 주어졌을 때, `2013년`과의 차이만큼 알파벳과 숫자를 각각 순회시켜 출력합니다.<br>

### 접근법
- 입력받은 연도에서 기준 연도 `2013`을 뺀 차이를 계산합니다.<br>
- 알파벳 부분은 `'F'`에서 12진법 순환으로 계산하여 `'A'`~`'L'` 범위로 맞춥니다.<br>
- 숫자 부분은 `'9'`에서 10진법 순환으로 계산하여 `'0'`~`'9'` 범위로 맞춥니다.<br>
- 두 문자를 합쳐 출력하면 해당 연도의 간지(干支) 표기 결과가 됩니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    int year = int.Parse(Console.ReadLine());
    int diff = year - 2013;

    char g = (char)('F' + diff % 12), z = (char)('9' + diff % 10);

    if (g > 'L') g -= (char)12;
    else if (g < 'A') g += (char)12;

    if (z > '9') z -= (char)10;
    else if (z < '0') z += (char)10;

    Console.WriteLine($"{g}{z}");
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

  int year; cin >> year;
  int diff = year - 2013;
  char g = 'F' + diff % 12, z = '9' + diff % 10;

  if (g > 'L') g -= 12;
  else if (g < 'A') g += 12;

  if (z > '9') z -= 10;
  else if (z < '0') z += 10;

  cout << g << z << "\n";

  return 0;
}
```
