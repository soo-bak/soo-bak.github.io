---
layout: single
title: "[백준 1003] 피보나치 함수 (C#, C++) - soo:bak"
date: "2025-04-19 22:46:00 +0900"
description: "피보나치 수열을 재귀적으로 호출할 때 0과 1이 출력되는 횟수를 미리 계산하는 백준 1003번 피보나치 함수 문제의 C# 및 C++ 풀이 및 해설"
---

## 문제 링크
[1003번 - 피보나치 함수](https://www.acmicpc.net/problem/1003)

## 설명
**피보나치 함수가 재귀적으로 호출되는 과정에서 출력되는 0과 1의 횟수를 구하는 문제**입니다.<br>

문제에서는 아래와 같은 피보나치 함수가 정의되어 있습니다:
```c++
int fibonacci(int n) {
  if (n == 0) {
    printf("0");
    return 0;
  } else if (n == 1) {
    printf("1");
    return 1;
  } else {
    return fibonacci(n - 1) + fibonacci(n - 2);
  }
}
```
위 코드에서 `fibonacci(0)`이 호출되면 `0`을 출력하고, `fibonacci(1)`이 호출되면 `1`을 출력합니다.<br>

즉, 입력으로 주어지는 `n` 에 대하여, <br>

`fibonacci(n)`을 호출했을 때 **함수 내부적으로 총 몇 번** `0`**과** `1`**이 출력되는지를 구하는 문제**입니다.<br>

## 접근법

재귀 호출을 그대로 구현하면 중복 계산이 너무 많기 때문에,<br>

`0`**과** `1`**이 호출되는 횟수를 각각 캐싱해두는 배열을 활용해 동적 프로그래밍으로 해결**할 수 있습니다.<br>

- `0`을 입력받았을 경우 → `0`이 1번, `1`이 0번 출력됨<br>
- `1`을 입력받았을 경우 → `0`이 0번, `1`이 1번 출력됨<br>

이후 `2`부터 `40`까지는 다음 점화식을 이용해 반복적으로 계산합니다:<br>

$$
\begin{aligned}
\text{zero}_n &= \text{zero}_{n-1} + \text{zero}_{n-2} \\
\text{one}_n &= \text{one}_{n-1} + \text{one}_{n-2}
\end{aligned}
$$<br>

- `0`의 호출 횟수 = 이전 두 수의 `0` 호출 횟수의 합<br>
- `1`의 호출 횟수 = 이전 두 수의 `1` 호출 횟수의 합<br>

이렇게 미리 결과를 계산해두고, 테스트케이스에서 주어진 입력에 대해 즉시 결과를 출력하면 됩니다.

<br>
> 참고 : [피보나치 수열 (Fibonacci Sequence) - soo:bak](https://soo-bak.github.io/algorithm/theory/fibonacciSeq/)

<br>

## Code

[ C# ]

```csharp
using System;

class Program {
  static void Main() {
    var ans = new (int zero, int one)[41];
    ans[0] = (1, 0);
    ans[1] = (0, 1);

    for (int i = 2; i <= 40; i++)
      ans[i] = (ans[i - 1].zero + ans[i - 2].zero, ans[i - 1].one + ans[i - 2].one);

    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      int n = int.Parse(Console.ReadLine());
      Console.WriteLine($"{ans[n].zero} {ans[n].one}");
    }
  }
}
```

[ C++ ]

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef pair<int, int> pii;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  pii ans[41];
  ans[0] = {1, 0};
  ans[1] = {0, 1};

  for (int i = 2; i <= 40; i++) {
    ans[i].first = ans[i - 1].first + ans[i - 2].first;
    ans[i].second = ans[i - 1].second + ans[i - 2].second;
  }

  int t; cin >> t;
  while (t--) {
    int n; cin >> n;
    cout << ans[n].first << " " << ans[n].second << "\n";
  }

  return 0;
}
```
