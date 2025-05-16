---
layout: single
title: "[백준 1834] 나머지와 몫이 같은 수 (C#, C++) - soo:bak"
date: "2025-05-16 19:33:00 +0900"
description: 나머지와 몫이 같은 수의 규칙을 찾아 전체 합을 구하는 백준 1834번 나머지와 몫이 같은 수 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[1834번 - 나머지와 몫이 같은 수](https://www.acmicpc.net/problem/1834)

## 설명

**N으로 나누었을 때 몫과 나머지가 같은 자연수들을 모두 찾아 그 합을 구하는 문제입니다.**

예를 들어 `N = 3`인 경우:

- `4 ÷ 3 = 1...1`, 몫과 나머지가 같음
- `8 ÷ 3 = 2...2`, 몫과 나머지가 같음

이러한 수들을 모두 찾아서 더한 값을 출력해야 합니다.

<br>

## 접근법

`나머지`와 `몫`이 같은 수는 다음과 같은 수식으로 표현할 수 있습니다:

$$
x = k \times N + k = k (N + 1)
$$

즉, 어떤 정수 `k`가 있을 때 `x`는 `k (N + 1)` 형태로 표현될 수 있으며,

이때 나눗셈 결과는 다음과 같습니다:

- 몫: $$k$$
- 나머지: $$x \mod N = k$$

따라서 이 조건을 만족하는 `x`는 $$1 \leq k < N$$ 범위의 정수에 대해 `k (N + 1)` 꼴의 수가 됩니다.

<br>
이러한 수들을 모두 합하면 다음과 같은 등차수열의 합이 됩니다:

$$
\sum_{k=1}^{N-1} k(N+1)
= (N+1) \sum_{k=1}^{N-1} k
= (N+1) \cdot \frac{(N-1)N}{2}
$$

하지만 직접 수열을 순회하면서 합산하는 방식으로 처리하여도 문제 조건을 통과할 수 있습니다.

`C#` 은 순회하는 방식으로, `C++` 은 일반항을 구하여 계산하는 방식으로 풀이하였습니다.

큰 수까지 고려해야 하므로 반드시 `long` 혹은 `long long` 자료형을 사용해야 함에 유의합니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    long n = long.Parse(Console.ReadLine());
    long sum = 0;
    for (long i = 1; i < n; i++)
      sum += i * (n + 1);

    Console.WriteLine(sum);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>

using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll n; cin >> n;
  cout << (n + 1) * (n - 1) * n / 2 << "\n";

  return 0;
}
```
