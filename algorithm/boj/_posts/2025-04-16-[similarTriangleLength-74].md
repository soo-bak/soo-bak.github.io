---
layout: single
title: "[백준 16478] 원의 반지름 (C#, C++) - soo:bak"
date: "2025-04-16 01:57:00 +0900"
description: 닮은 삼각형의 변 비례식을 이용해 선분의 길이를 계산하는 백준 16478번 원의 반지름 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[16478번 - 원의 반지름](https://www.acmicpc.net/problem/16478)

## 설명
**삼각형의 닮음을 활용하여 특정 선분의 길이를 계산하는 문제**입니다.<br>
<br>

- 선분 `AB`, `BC`, `CD`의 길이가 주어집니다.<br>
- 문제에서는 선분 사이에 존재하는 특정 삼각형의 닮음 관계를 이용해,<br>
  선분 `AD`의 길이를 계산하라는 의미입니다.<br>
- 이때 닮은 삼각형의 대응 변의 비를 통해 다음과 같은 비례식을 세울 수 있습니다:<br>
  $$ \frac{AB}{BC} = \frac{AD}{CD} $$<br>
  이를 변형하면:<br>
  $$ AD = \frac{AB \times CD}{BC} $$<br>

### 접근법
- 입력으로 세 선분의 길이 `AB`, `BC`, `CD`를 실수형으로 입력받습니다.<br>
- 위 수식을 구현하여 `AD` 값을 계산합니다.<br>
- 출력은 소수점 아래 `7`자리까지 고정 형식으로 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    var ab = double.Parse(input[0]);
    var bc = double.Parse(input[1]);
    var cd = double.Parse(input[2]);

    var ad = ab * cd / bc;
    Console.WriteLine($"{ad:F7}");
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

  double ab, bc, cd; cin >> ab >> bc >> cd;

  cout.setf(ios::fixed); cout.precision(7);
  cout << ab * cd / bc << "\n";

  return 0;
}
```
