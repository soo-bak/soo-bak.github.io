---
layout: single
title: "[백준 1977] 완전제곱수 (C#, C++) - soo:bak"
date: "2025-04-14 05:16:15 +0900"
description: 완전제곱수의 합과 최솟값을 구하는 간단한 수학적 조건 검사 문제인 백준 1977번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[1977번 - 완전제곱수](https://www.acmicpc.net/problem/1977)

## 설명
이 문제는 **주어진 범위 내에서 완전제곱수(perfect square)**만을 골라서 그 합과 **최솟값을 출력하는 문제**입니다.

완전제곱수란 어떤 정수 $$x$$에 대해 $$x^2$$ 형태로 표현되는 수를 의미합니다. <br>
> 예: $$1^2$$, $$2^2$$, $$3^2$$, ..., $$100^2$$

---

## 접근법
- $$1^2$$부터 $$100^2$$까지 미리 완전제곱수를 표시해두기 위해 배열에 기록합니다.
- 입력된 `min`, `max` 범위 내에서 완전제곱수인지 여부를 확인하여:
  - 합을 누적하고
  - 가장 처음 등장한 완전제곱수를 최솟값으로 저장합니다.
- 만약 해당 범위 내에 완전제곱수가 없다면 `-1`을 출력합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var min = int.Parse(Console.ReadLine()!);
      var max = int.Parse(Console.ReadLine()!);

      var isSquare = new bool[10_001];
      for (int i = 1; i * i <= 10_000; i++)
        isSquare[i * i] = true;

      int sum = 0, minVal = 0;
      for (int i = min; i <= max; i++) {
        if (isSquare[i]) {
          sum += i;
          if (minVal == 0) minVal = i;
        }
      }

      if (minVal == 0) Console.WriteLine("-1");
      else {
        Console.WriteLine(sum);
        Console.WriteLine(minVal);
      }
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>
#define MAX 10'001

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  bool sieve[MAX] = {0, };
  for (int i = 1; i <= 100; i++)
    sieve[i * i] = true;

  int min, max; cin >> min >> max;
  int sum = 0, minAns = 0;
  for (int i = min; i <= max; i++) {
    if (sieve[i] == true) {
      if (!minAns) minAns = i;
      sum+= i;
    }
  }

  if (!minAns) cout << "-1\n";
  else cout << sum << "\n" << minAns << "\n";

  return 0;
}
```
