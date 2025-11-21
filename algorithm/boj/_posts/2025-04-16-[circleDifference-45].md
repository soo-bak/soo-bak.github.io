---
layout: single
title: "[백준 16483] 접시 안의 원 (C#, C++) - soo:bak"
date: "2025-04-16 01:59:00 +0900"
description: 두 원의 중심이 같고 접선의 길이가 주어졌을 때 피타고라스의 정리를 통해 a^2 - b^2 값을 계산하는 백준 16483번 접시 안의 원 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[16483번 - 접시 안의 원](https://www.acmicpc.net/problem/16483)

## 설명
**접시 모양으로 겹쳐진 두 원에서 작은 원의 접선이 큰 원과 만나는 두 점 사이의 길이가 주어졌을 때,** <br>
<br>

**두 반지름의 제곱 차를 구하는 문제**입니다.<br>
<br>

- 접시에는 중심이 같은 두 원이 있습니다.<br>
- 큰 원의 반지름을 `a`, 작은 원의 반지름을 `b`라고 할 때,<br>
- 작은 원의 접선이 큰 원과 만나는 두 점 사이의 길이 `T`가 주어집니다. <br>
- 이때 피타고라스 정리에 따라 다음 식이 성립합니다:<br>
  $$a^2 - b^2 = \left(\frac{T}{2}\right)^2$$<br>
- 해당 값을 반올림하여 정수로 출력하면 됩니다.<br>

### 접근법
- 접선의 길이 `T`를 입력받습니다.<br>
- 공식을 그대로 계산하여 $$(T / 2)^2$$을 구한 뒤, 소수점 첫째 자리에서 반올림해 정수로 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    double t = double.Parse(Console.ReadLine());
    var res = Math.Round((t / 2) * (t / 2));
    Console.WriteLine((int)res);
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

  double t; cin >> t;
  cout << (int)(round((t / 2) * (t / 2))) << "\n";

  return 0;
}
```
