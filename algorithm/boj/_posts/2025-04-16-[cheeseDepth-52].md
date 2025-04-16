---
layout: single
title: "[백준 16479] 컵라면 측정 (C#, C++) - soo:bak"
date: "2025-04-16 01:57:00 +0900"
description: 원기둥 형태 컵라면 용기 깊이를 계산하는 백준 16479번 컵라면 측정 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[16479번 - 컵라면 측정](https://www.acmicpc.net/problem/16479)

## 설명
**원기둥의 높이를 계산하는 문제**입니다.<br>
<br>

- 용기 모양은 위가 넓고 아래가 좁은 등벼 사다리꼴 형태입니다.<br>
- 컵라면 용기의 윗면 반지름, 아랫면 반지름, 등변 사다리꼴의 빗변 길이가 주어집니다.<br>
- 컵라면 용기의 원기둥의 높이, 즉, 컵라면 용기의 깊이를 계산하여 출력합니다.<br>
<br>

용기의 깊이는 피타고라스 정리를 응용해 다음과 같이 계산됩니다:<br>
- $$용기 깊이 = 빗변 길이^2 - \left(\frac{윗변 반지름 - 아랫변 반지름}{2}\right)^2$$<br>

### 접근법
- 공식을 그대로 구현해 깊이를 계산하고 제곱값을 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    var k = int.Parse(Console.ReadLine());

    var input = Console.ReadLine().Split();
    var tR = double.Parse(input[0]);
    var bR = double.Parse(input[1]);

    var ans = k * k - Math.Pow((tR - bR) / 2, 2);
    Console.WriteLine(ans);
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

  double k, tR, bR; cin >> k >> tR >> bR;
  double ans = k * k - ((tR - bR) / 2) * ((tR - bR) / 2);
  cout << ans << "\n";

  return 0;
}
```
