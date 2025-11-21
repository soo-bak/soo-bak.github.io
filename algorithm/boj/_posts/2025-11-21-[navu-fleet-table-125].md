---
layout: single
title: "[백준 9654] 나부 함대 데이터 (C#, C++) - soo:bak"
date: "2025-11-21 23:39:00 +0900"
description: 예제와 동일한 함대 정보를 표 형태로 출력하는 백준 9654번 나부 함대 데이터 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[9654번 - 나부 함대 데이터](https://www.acmicpc.net/problem/9654)

## 설명

입력 없이 함대 정보를 예제 표와 동일한 형식으로 출력합니다.

<br>

## 접근법

문제를 참고해 문자열을 그대로 출력하면 됩니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    Console.WriteLine("SHIP NAME      CLASS          DEPLOYMENT IN SERVICE");
    Console.WriteLine("N2 Bomber      Heavy Fighter  Limited    21        ");
    Console.WriteLine("J-Type 327     Light Combat   Unlimited  1         ");
    Console.WriteLine("NX Cruiser     Medium Fighter Limited    18        ");
    Console.WriteLine("N1 Starfighter Medium Fighter Unlimited  25        ");
    Console.WriteLine("Royal Cruiser  Light Combat   Limited    4         ");
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

  cout << "SHIP NAME      CLASS          DEPLOYMENT IN SERVICE\n";
  cout << "N2 Bomber      Heavy Fighter  Limited    21        \n";
  cout << "J-Type 327     Light Combat   Unlimited  1         \n";
  cout << "NX Cruiser     Medium Fighter Limited    18        \n";
  cout << "N1 Starfighter Medium Fighter Unlimited  25        \n";
  cout << "Royal Cruiser  Light Combat   Limited    4         \n";
  return 0;
}
```

