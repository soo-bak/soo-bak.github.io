---
layout: single
title: "[백준 10698] Ahmed Aly (C#, C++) - soo:bak"
date: "2025-05-04 19:04:00 +0900"
description: 단순한 사칙연산 수식을 입력받아 식이 맞는지 판별하는 시뮬레이션 문제, 백준 10698번 Ahmed Aly 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10698번 - Ahmed Aly](https://www.acmicpc.net/problem/10698)

## 설명

두 개의 주사위를 던졌을 때, 나온 두 숫자를 바탕으로 **특정 별칭 문장**을 구성하는 문제입니다.

각 숫자에 대응하는 별칭이 정해져 있으며, 다음과 같은 규칙이 적용됩니다:

- 두 주사위의 수가 같은 경우, 특별한 이름으로 대응합니다. <br>
  예를 들어 `1-1`은 `"Habb Yakk"`, `6-6`은 `"Dosh"` 등으로 문제에 주어져 있습니다.
- 서로 다른 숫자가 나온 경우, **큰 수를 먼저 출력하고 작은 수를 나중에 출력합니다**.
- 단, 예외적으로 `5`와 `6`이 함께 나온 경우에는 `"Sheesh Beesh"`로 출력해야 합니다.

<br>

## 접근법

- 숫자에 대응되는 기본 별칭과 해당 숫자에 대해 대응되는 별칭을 미리 준비합니다.
- 각 테스트케이스마다 두 수를 입력받아 **작은 수가 앞에 오도록 정렬**합니다.
- 아래의 조건 순서에 따라 적절한 문장을 결정합니다:
  1. 두 수가 같다면, 해당 수에 대응되는 별칭 하나를 출력합니다.
  2. 두 수가 `5`와 `6`이라면 예외 문장 `"Sheesh Beesh"`를 출력합니다다.
  3. 그 외의 경우에는 큰 수의 별칭을 앞에, 작은 수의 별칭을 뒤에 연결하여 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    string[] dice = { "Yakk", "Doh", "Seh", "Ghar", "Bang", "Sheesh" };
    string[] ex = { "Habb Yakk", "Dobara", "Dousa", "Dorgy", "Dabash", "Dosh" };

    int t = int.Parse(Console.ReadLine());
    for (int i = 1; i <= t; i++) {
      var ab = Console.ReadLine().Split().Select(int.Parse).ToArray();
      int a = Math.Min(ab[0], ab[1]), b = Math.Max(ab[0], ab[1]);

      string ans = a == b ? ex[a - 1] :
                   a == 5 && b == 6 ? "Sheesh Beesh" :
                   $"{dice[b - 1]} {dice[a - 1]}";

      Console.WriteLine($"Case {i}: {ans}");
    }
  }
}
```

<br>

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string dice[6] = {"Yakk", "Doh", "Seh", "Ghar", "Bang", "Sheesh"};
  string ex[6] = {"Habb Yakk", "Dobara", "Dousa", "Dorgy", "Dabash", "Dosh"};

  int t; cin >> t;
  for (int i = 1; i <= t; i++) {
    int a, b; cin >> a >> b;
    if (a > b) swap(a, b);

    string ans = a == b ? ex[a - 1] :
                 a == 5 && b == 6 ? "Sheesh Beesh" :
                 dice[b - 1] + " " + dice[a - 1];

    cout << "Case " << i << ": " << ans << "\n";
  }

  return 0;
}
```
