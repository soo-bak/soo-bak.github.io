---
layout: single
title: "[백준 10448] 유레카 이론 (C#, C++) - soo:bak"
date: "2025-05-16 20:50:00 +0900"
description: 주어진 수가 정확히 세 개의 삼각수의 합으로 표현 가능한지를 판단하는 백준 10448번 유레카 이론 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10448
  - C#
  - C++
  - 알고리즘
  - 수학
  - 브루트포스
keywords: "백준 10448, 백준 10448번, BOJ 10448, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10448번 - 유레카 이론](https://www.acmicpc.net/problem/10448)

## 설명

**주어진 수가 서로 같을 수도 있는 세 개의 삼각수의 합으로 표현될 수 있는지를 판단하는 문제입니다.**

삼각수란 `1 + 2 + 3 + ... + n` 형태로 누적된 수이며, 공식으로는 다음과 같이 정의됩니다:

$$
T_n = \frac{n(n+1)}{2}
$$

<br>
예를 들어 삼각수의 앞 몇 개 항은 다음과 같습니다:

- `T₁ = 1`, `T₂ = 3`, `T₃ = 6`, `T₄ = 10`, `T₅ = 15`, `T₆ = 21`, `...`

<br>

## 접근법

가장 먼저 고려할 점은, `1000 이하의 자연수`**는** `삼각수 3개의 합`**으로 충분히 표현할 수 있다는 것**입니다.

왜냐하면 최대 삼각수는 약 `T₄₃ ≈ 990` 이므로 `1000`보다 작거나 같은 수를 구성하기에 충분합니다.

문제 해결은 다음과 같은 순서로 진행합니다:

1. 미리 `T₁`부터 `T₄₄`까지의 삼각수를 배열로 구해둡니다.
2. 각 테스트 케이스마다 삼중 반복문을 사용하여:
   - 세 개의 삼각수를 중복 허용하여 더한 결과가 `K`와 같은지 확인합니다.
3. 이때 선택한 세 개의 삼각수는 서로 다른 수일 필요도 없고, 어떤 순서로 선택했는지도 상관없습니다.

완전 탐색으로 모든 조합을 탐색해도 최대 `44³ = 약 85,000`번의 연산이므로 제한 시간 내에 충분히 처리됩니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int[] tri = new int[44];
    for (int i = 0; i < 44; i++)
      tri[i] = (i + 1) * (i + 2) / 2;

    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      int n = int.Parse(Console.ReadLine());
      bool found = false;
      for (int i = 0; i < 44 && !found; i++) {
        for (int j = 0; j < 44 && !found; j++) {
          for (int k = 0; k < 44; k++) {
            if (tri[i] + tri[j] + tri[k] == n) {
              found = true;
              break;
            }
          }
        }
      }
      Console.WriteLine(found ? 1 : 0);
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int tri[44];
  for (int i = 0; i < 44; ++i)
    tri[i] = (i + 1) * (i + 2) / 2;

  int t; cin >> t;
  while (t--) {
    int n; cin >> n;
    bool found = false;
    for (int i = 0; i < 44 && !found; ++i) {
      for (int j = i; j < 44 && !found; ++j) {
        for (int k = j; k < 44; ++k) {
          if (tri[i] + tri[j] + tri[k] == n) {
            found = true;
            break;
          }
        }
      }
    }
    cout << (found ? "1" : "0") << "\n";
  }

  return 0;
}
```
