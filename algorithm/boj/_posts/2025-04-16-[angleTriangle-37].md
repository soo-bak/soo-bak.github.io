---
layout: single
title: "[백준 10101] 삼각형 외우기 (C#, C++) - soo:bak"
date: "2025-04-16 02:05:00 +0900"
description: 세 각의 합이 180도를 만족하는지 확인하고 각의 크기에 따라 삼각형의 종류를 분류하는 백준 10101번 삼각형 외우기 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10101
  - C#
  - C++
  - 알고리즘
keywords: "백준 10101, 백준 10101번, BOJ 10101, angleTriangle, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10101번 - 삼각형 외우기](https://www.acmicpc.net/problem/10101)

## 설명
**세 각을 통해 삼각형이 가능한지 판단하고, 각의 크기에 따라 삼각형의 종류를 분류하는 문제**입니다.<br>
<br>

- 세 각의 크기를 입력받고, 그 합이 `180`도가 아니면 삼각형이 될 수 없습니다.<br>
- 삼각형이 될 수 있는 경우, 각의 크기에 따라 다음과 같이 분류합니다:<br>
  - 세 각이 모두 `60`도이면 `Equilateral`<br>
  - 두 각이 같으면 `Isosceles`<br>
  - 세 각이 모두 다르면 `Scalene`<br>

### 접근법
- 세 각을 입력받아 합을 계산합니다.<br>
- 세 각의 합이 `180`이 아니라면 `"Error"`를 출력합니다.<br>
- 세 각이 모두 `60`도이면 `"Equilateral"`<br>
- 두 각이 같으면 `"Isosceles"`<br>
- 모두 다르면 `"Scalene"`을 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    var a = int.Parse(Console.ReadLine());
    var b = int.Parse(Console.ReadLine());
    var c = int.Parse(Console.ReadLine());

    if (a + b + c != 180)
      Console.WriteLine("Error");
    else if (a == 60 && b == 60 && c == 60)
      Console.WriteLine("Equilateral");
    else if (a == b || b == c || a == c)
      Console.WriteLine("Isosceles");
    else
      Console.WriteLine("Scalene");
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

  int f, s, t; cin >> f >> s >> t;
  if (f + s + t != 180) cout << "Error\n";
  else {
    if (f == 60 && s == 60 && t == 60) cout << "Equilateral\n";
    else {
      if (f == s || f == t || s == t) cout << "Isosceles\n";
      else cout << "Scalene\n";
    }
  }

  return 0;
}
```
