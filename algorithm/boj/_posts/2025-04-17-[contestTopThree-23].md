---
layout: single
title: "[백준 5576] 콘테스트 (C#, C++) - soo:bak"
date: "2025-04-17 00:23:43 +0900"
description: 10개의 점수 중 상위 3개의 합을 구하여 출력하는 백준 5576번 콘테스트 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[5576번 - 콘테스트](https://www.acmicpc.net/problem/5576)

## 설명
**10개의 점수 중 상위 3개의 점수를 골라 합산하여 출력하는 문제**입니다.<br>
<br>

- 총 두 줄로 구성된 입력은 **W 대학과 K 대학의 각각 10명 점수**를 나타냅니다.<br>
- 각 대학의 상위 `3`명 점수를 골라 합한 값을 **각각 출력**하면 됩니다.<br>

### 접근법
- 각 대학 점수 `10`개를 입력받고, 내림차순 정렬하여 상위 `3`개의 점수를 추출합니다.<br>
- 상위 `3`개 점수의 합을 계산한 후 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var w = new int[10];
    var k = new int[10];

    for (int i = 0; i < 10; i++)
      w[i] = int.Parse(Console.ReadLine());

    for (int i = 0; i < 10; i++)
      k[i] = int.Parse(Console.ReadLine());

    var sumW = w.OrderByDescending(x => x).Take(3).Sum();
    var sumK = k.OrderByDescending(x => x).Take(3).Sum();

    Console.WriteLine($"{sumW} {sumK}");
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vi tmp(10);
  for (int i = 0; i < 10; i++)
    cin >> tmp[i];

  sort(tmp.rbegin(), tmp.rend());

  int sumW = tmp[0] + tmp[1] + tmp[2];
  for (int i = 0; i < 10; i++)
    cin >> tmp[i];

  sort(tmp.rbegin(), tmp.rend());

  int sumK = tmp[0] + tmp[1] + tmp[2];

  cout << sumW << " " << sumK << "\n";

  return 0;
}
```
