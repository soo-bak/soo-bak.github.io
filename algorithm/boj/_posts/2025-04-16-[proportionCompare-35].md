---
layout: single
title: "[백준 16485] 평균 속도의 비교 (C#, C++) - soo:bak"
date: "2025-04-16 01:57:00 +0900"
description: 두 경로의 시간 대비 거리 비율을 비교해 상대적 속도를 구하는 백준 16485번 평균 속도의 비교 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[16485번 - 평균 속도의 비교](https://www.acmicpc.net/problem/16485)

## 설명
**두 경로의 길이 대비 시간 비율을 계산하여 평균 속도를 비교하는 문제**입니다.<br>
<br>

- 문제에서는 두 구간 `AB`와 `AC`의 거리 값이 주어집니다.<br>
- 두 구간의 평균 속도를 비교하는 것이 아니라, 단순히 **거리 비율**을 통해 어느 쪽이 더 효율적인지를 확인합니다.<br>
- 이때 단순히 다음 비율을 계산하면 됩니다:<br>
  $$ \frac{AB}{AC} $$<br>
- 계산 결과는 소수점 아래 7자리까지 출력해야 합니다.<br>

### 접근법
- 두 거리 `AB`, `AC`를 실수형으로 입력받습니다.<br>
- `AB / AC`를 계산하여 출력하면 됩니다.<br>
- 문제에서 요구하는 출력 형식에 따라 소수점 아래 7자리 고정 출력 형식을 사용합니다.<br>

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
    var ac = double.Parse(input[1]);

    var res = ab / ac;
    Console.WriteLine($"{res:F7}");
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

  double ab, ac; cin >> ab >> ac;

  cout.setf(ios::fixed); cout.precision(7);
  cout << ab / ac << "\n";

  return 0;
}
```
