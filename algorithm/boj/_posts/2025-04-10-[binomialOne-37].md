---
layout: single
title: "[백준 11050] 이항 계수 1 (C#, C++) - soo:bak"
date: "2025-04-10 15:22:00 +0900"
description: 구현, 수학, 조합 개념을 활용한 백준 11050번 이항 계수 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[11050번 - 이항 계수 1](https://www.acmicpc.net/problem/11050)

## 설명
**이항 계수**(Binomial Coefficient)를 계산하는 기본적인 수학 문제입니다.

### 이항 계수란?
이항 계수란, `n`개의 원소 중에서 `k`개를 선택하는 경우의 수를 말하며, 조합(Combination)이라고도 부릅니다.
수학적으로는 다음과 같이 정의됩니다:

$$
\binom{n}{k} = \frac{n!}{k!(n-k)!}
$$

이는 순서와는 관계없이 `k`개를 선택하는 모든 가능한 경우의 수를 의미하며, 조합 문제의 기초 개념으로 자주 등장합니다.

### 접근법
1. `n!`, `k!`, `(n-k)!`을 각각 반복문을 통해 직접 계산합니다.
2. 그 값을 이항 계수 공식에 대입하여 결과를 출력합니다.
3. 문제 조건 상 `0 ≤ k ≤ n ≤ 10` 이므로 수가 작아 오버플로우 걱정이 없습니다.

### 시간 복잡도
- 팩토리얼은 모두 반복문으로 계산하므로 각 계산의 시간 복잡도는 **O(n)**입니다.
- 하지만 `n`의 최댓값이 10이므로 전체 연산은 매우 작아 **O(1)**로 간주할 수 있습니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
namespace Solution {
  class Program {
    static int Factorial(int n) {
      int result = 1;
      for (int i = 2; i <= n; i++) result *= i;
      return result;
    }

    static void Main(string[] args) {
      var input = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
      int n = input[0], k = input[1];

      int result = Factorial(n) / (Factorial(k) * Factorial(n - k));
      Console.WriteLine(result);
    }
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

  int n, k; cin >> n >> k;

  int ans = 1;
  for (int i = 2; i <= n; i++)
    ans *= i;
  for (int i = 2; i <= k; i++)
    ans /= i;
  for (int i = 2; i <= (n - k); i++)
    ans /= i;

  cout << ans << "\n";

  return 0;
}
```
