---
layout: single
title: "[백준 1748] 수 이어 쓰기 1 (C#, C++) - soo:bak"
date: "2025-05-04 21:12:00 +0900"
description: 1부터 N까지의 모든 수를 이어썼을 때 전체 자릿수를 구하는 누적 자릿수 계산 문제, 백준 1748번 수 이어 쓰기 1 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1748
  - C#
  - C++
  - 알고리즘
keywords: "백준 1748, 백준 1748번, BOJ 1748, digitlengthsum, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1748번 - 수 이어 쓰기 1](https://www.acmicpc.net/problem/1748)

## 설명
`1`부터 `N`까지의 모든 정수를 순서대로 이어붙여 만든 문자열의 `총 자릿수`를 구하는 문제입니다.

예를 들어,<br>
`N = 15`일 때 이어붙인 수는 `123456789101112131415`로, 총 자릿수는 `21`입니다.

`N`의 범위가 최대 `100,000,000`이므로, 단순히 반복문으로 문자열을 만들어 세는 방식은 시간 초과가 발생합니다.

따라서, **자릿수별 패턴**을 활용해 효율적으로 계산해야 합니다.

## 접근법
1. **자릿수별 패턴 분석**:
  - 숫자는 자릿수에 따라 구간으로 나뉩니다:
    - `1`자리 수: `1 ~ 9` (`9`개, 각 `1`자리)
    - `2`자리 수: `10 ~ 99` (`90`개, 각 `2`자리)
    - `3`자리 수: `100 ~ 999` (`900`개, 각 `3`자리)
    - `...`
   - 길이가 `i`인 수는 $$9 \times 10^{i-1}$$ 개이며, 각 수는 `i`자리입니다.
     - 따라서 해당 구간의 총 자릿수는:

     $$
     9 \times 10^{i-1} \times i
     $$

2. **`N`까지의 자릿수 계산**:
   - `N`이 속한 자릿수 `d`를 구합니다 (예: $$N=120 \implies d=3$$).
   - `1`자리부터 `d - 1`자리까지는 전체 구간을 계산:

     $$
     9 \times 10^{i-1} \times i
     $$
   - 마지막 구간(`d`자리)은 `N`까지의 수만 계산:

      - 마지막 구간의 수 개수 : (`구간의 끝` - `구간의 시작` + `1`)

      $$
      \text{마지막 구간의 수 개수} = N - 10^{d-1} + 1
      $$

      - 마지막 구간의 총 자릿수 : (`마지막 구간의 수 개수`) x (`속한 구간의 자릿수 d`)

      $$
      \text{자릿수 기여} = \left( N - 10^{d-1} + 1 \right) \times d
      $$

3. **구현**:
   - `N`의 자릿수 `d`를 계산
   - `1 ~ (d - 1)`자리 구간의 자릿수를 누적
   - `d`자리 구간의 자릿수를 추가하여 최종 결과 출력

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    int d = n.ToString().Length;
    long res = 0;

    for (int i = 1; i < d; i++) {
      res += 9L * (long)Math.Pow(10, i - 1) * i;
    }

    res += (long)(n - (int)Math.Pow(10, d - 1) + 1) * d;
    Console.WriteLine(res);
  }
}
```

<br>

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  int d = 0, t = n;
  while (t)
    d++, t /= 10;

  ll ans = 0;
  for (int i = 1; i < d; i++)
    ans += 9LL * pow(10, i - 1) * i;
  ans += 1LL * (n - pow(10, d - 1) + 1) * d;

  cout << ans << "\n";

  return 0;
}
```
