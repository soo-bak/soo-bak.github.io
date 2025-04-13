---
layout: single
title: "[백준 9414] 구슬 반지 (C#, C++) - soo:bak"
date: "2025-04-14 04:08:48 +0900"
description: 제곱 기반 누적 비용을 계산하며 상한선을 넘는 경우 예외 처리를 적용하는 백준 9414번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[9414번 - 구슬 반지](https://www.acmicpc.net/problem/9414)

## 설명
이 문제는 각 연도마다 구슬 반지를 구매하는데 드는 **비용이 누적 제곱 기반으로 증가**하는 구조입니다.
각 해마다 구매한 반지의 수치가 주어지며, 연도별 비용은 다음과 같이 계산됩니다:

$$
2 \times (\text{반지의 가치})^{\text{연도}}
$$

---

## 접근법
- 각 테스트 케이스는 여러 줄의 반지 가치로 이루어지며, `0`으로 끝납니다.
- 큰 수부터 정렬하여 연도 비용이 적게 들도록 최적화합니다.
- 비용은 $$2 \times a^b$$ 형태로 누적되며, 이 값이 `MAX = 5,000,000`을 넘으면 **Too expensive**를 출력합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;

namespace Solution {
  class Program {
    const int MAX = 5_000_000;

    static void Main(string[] args) {
      int t = int.Parse(Console.ReadLine()!);
      while (t-- > 0) {
        var estimates = new List<BigInteger>();
        while (true) {
          var val = int.Parse(Console.ReadLine()!);
          if (val == 0) break;
          estimates.Add(val);
        }

        estimates.Sort((a, b) => b.CompareTo(a));
        if (estimates.Count > 0 && estimates[0] <= MAX / 2) {
          BigInteger sum = 0;
          for (int i = 0; i < estimates.Count; i++) {
            var cost = BigInteger.Pow(estimates[i], i + 1) * 2;
            sum += cost;
          }
          Console.WriteLine(sum > MAX ? "Too expensive" : sum.ToString());
        } else Console.WriteLine("Too expensive");
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
#define MAX 5'000'000

using namespace std;
typedef long long ll;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    vi estimate;

    int input = 1;
    while (input != 0) {
      cin >> input;
      estimate.push_back(input);
    }

    sort(estimate.rbegin(), estimate.rend());

    if (estimate[0] <= MAX / 2) {
      ll sum = 0; int year = 1;
      for (size_t i = 0; i < estimate.size(); i++) {
        ll cost = 1;
        for (int y = 0; y < year; y++)
          cost *= estimate[i];
        sum += 2 * cost;
        year++;
      }

      if (sum > MAX) cout << "Too expensive\n";
      else cout << sum << "\n";
    } else cout << "Too expensive\n";
  }

  return 0;
}
```
