---
layout: single
title: "[백준 2914] 저작권 (C#, C++) - soo:bak"
date: "2025-04-19 04:16:00 +0900"
description: 평균을 반올림한 결과로 주어진 곡 수에서 최소 실제 곡 수를 계산하는 수학적 역산 문제인 백준 2914번 저작권 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[2914번 - 저작권](https://www.acmicpc.net/problem/2914)

## 설명
**반올림된 평균 곡 수가 주어졌을 때, 최소 실제 곡 수의 총합을 계산하는 문제**입니다.<br>
<br>

- `A`곡이 수록된 앨범이 있고, 평균 `I`곡이 있다고 합니다.<br>
- 하지만 이 평균은 실제로는 반올림되어 표시된 값입니다.<br>
- 따라서 **반올림 결과가 I가 되는 가장 작은 실제 곡 수 총합**을 계산하면 됩니다.<br>

### 접근법
- 반올림은 소수점 첫째 자리에서 **올림(**`ceil`**)**되는 방식입니다.<br>
- 즉, 다음과 같은 **등식**을 만족하는 최소 `X`를 구해야 합니다:<br>

  $$
  \left\lceil \frac{X}{A} \right\rceil = I
  $$

- 이 등식은 다음 **부등식**을 만족하는 `X`에 의해 성립합니다:

  $$
  I - 1 < \frac{X}{A} \leq I
  $$

- 양변에 `A`를 곱하면 다음 범위로 바꿀 수 있습니다:

  $$
  A \cdot (I - 1) < X \leq A \cdot I
  $$

- 이 범위에서 가능한 최소 정수 `X`는 다음과 같습니다:

  $$
  X = A \cdot (I - 1) + 1
  $$

- 따라서 실제 곡 수의 총합은 `A * (I - 1) + 1` 로 계산하면 됩니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    int a = int.Parse(input[0]);
    int i = int.Parse(input[1]);

    Console.WriteLine(a * (i - 1) + 1);
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

  int cntS, avgM; cin >> cntS >> avgM;
  cout << cntS * (avgM - 1) + 1 << "\n";

  return 0;
}
```
