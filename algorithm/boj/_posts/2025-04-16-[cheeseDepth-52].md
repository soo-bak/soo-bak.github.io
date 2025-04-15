---
layout: single
title: "[백준 16479] 컵라면 측정 (C#, C++) - soo:bak"
date: "2025-04-16 01:57:00 +0900"
description: 원기둥 형태 컵라면 용기 속 치즈의 깊이를 계산하는 백준 16479번 컵라면 측정 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[16479번 - 컵라면 측정](https://www.acmicpc.net/problem/16479)

## 설명
**컵라면 용기 속 치즈의 깊이를 계산하는 문제**입니다.<br>
<br>

- 컵라면 용기의 윗면 반지름, 아랫면 반지름, 높이가 주어집니다.<br>
- 용기 모양은 위가 넓고 아래가 좁은 형태입니다.<br>
- 컵라면 용기의 원기둥의 깊이만 계산하면 됩니다.<br>
<br>

이 치즈 원기둥의 깊이는 피타고라스 정리를 응용해 다음과 같이 계산됩니다:<br>
- 전체 높이에서 원기둥 상단의 중심이 빗면으로부터 얼마나 들어가 있는지를 빼는 방식으로 계산<br>
- 정식 수식: $$k^2 - \left(\frac{tR - bR}{2}\right)^2$$<br>

### 접근법
- 컵라면 전체 높이와 윗면/아랫면 반지름을 입력받습니다.<br>
- 공식을 그대로 구현해 깊이를 계산하고 출력합니다.<br>
- 출력은 실수 형태이며, 소수점 자릿수 제한이 없으므로 그대로 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    var k = double.Parse(input[0]);
    var tR = double.Parse(input[1]);
    var bR = double.Parse(input[2]);

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
  cout << ans << '\n';

  return 0;
}
```
