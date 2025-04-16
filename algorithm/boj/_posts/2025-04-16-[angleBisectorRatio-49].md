---
layout: single
title: "[백준 16485] 작도하자! - ② (C#, C++) - soo:bak"
date: "2025-04-16 01:57:00 +0900"
description: 삼각형의 각의 이등분선 정리에 따라 선분 BM과 CM의 비율을 구하는 백준 16485번 작도하자! - ② 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[16485번 - 작도하자! - ②](https://www.acmicpc.net/problem/16485)

## 설명
**삼각형에서 각의 이등분선 정리를 이용하여 선분의 비율을 계산하는 문제**입니다.<br>
<br>

- 삼각형 ABC에서 각 `BAC`의 이등분선과 변 `BC`의 교점을 `M`이라고 합니다.<br>
- 변 `AB`의 길이 \( c \), 변 `AC`의 길이 \( b \)가 주어질 때,<br>
  이등분선 정리에 따라 다음 비율이 성립합니다:<br>
  $$ \frac{BM}{CM} = \frac{AB}{AC} = \frac{c}{b} $$<br>
- 이 비율을 계산하여 소수점 아래 7자리까지 출력하면 됩니다.<br>

### 접근법
- 정수형으로 주어진 두 변의 길이 `c`, `b`를 실수형으로 변환해 나눗셈을 수행합니다.<br>
- 출력 형식에 따라 소수점 아래 7자리까지 고정된 형식으로 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    double c = double.Parse(input[0]);
    double b = double.Parse(input[1]);

    double ratio = c / b;
    Console.WriteLine($"{ratio:F7}");
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

  double c, b;
  cin >> c >> b;

  cout.setf(ios::fixed);
  cout.precision(7);
  cout << c / b << "\n";

  return 0;
}
```
