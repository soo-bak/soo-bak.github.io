---
layout: single
title: "[백준 10833] 사과 (C#, C++) - soo:bak"
date: "2025-04-16 02:00:00 +0900"
description: 각 학교에서 나눠주고 남는 사과의 총합을 계산하는 나머지 연산 기반의 단순 누적 문제인 백준 10833번 사과 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10833번 - 사과](https://www.acmicpc.net/problem/10833)

## 설명
**각 학교에 사과를 나누어줄 때, 나눠주고 남는 사과의 총 개수를 구하는 문제**입니다.<br>
<br>

- 총 `S`개의 학교가 있으며, 각 학교마다 `A`명의 학생과 `사과 개수`가 주어집니다.<br>
- 각 학생에게 **동일한 수의 사과**를 나눠줘야 하므로, 사과의 수를 `A`로 나눈 나머지가 **남는 사과**가 됩니다.<br>
- 모든 학교에서 남은 사과를 합산하면 최종적으로 버려지는 사과의 총 개수를 알 수 있습니다.<br>
<br>

### 접근법
- 첫 줄에 학교의 수 `S`가 주어집니다.<br>
- 이후 `S`개의 줄에 걸쳐 각 학교의 학생 수 `A`와 사과 수가 주어집니다.<br>
- 각 줄마다 `사과 % A` 값을 구하여 누적합을 더합니다.<br>
- 최종적으로 모든 남은 사과의 총합을 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    int s = int.Parse(Console.ReadLine());
    int sum = 0;
    for (int i = 0; i < s; i++) {
      var input = Console.ReadLine().Split();
      int a = int.Parse(input[0]);
      int apples = int.Parse(input[1]);
      sum += apples % a;
    }
    Console.WriteLine(sum);
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

  int cntS; cin >> cntS;
  int sum = 0;
  for (int i = 0; i < cntS; i++) {
    int cntA, cntSt; cin >> cntA >> cntSt;
    sum += cntSt % cntA;
  }
  cout << sum << "\n";

  return 0;
}
```
