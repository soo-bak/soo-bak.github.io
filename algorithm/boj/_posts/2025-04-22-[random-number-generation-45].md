---
layout: single
title: "[백준 6500] 랜덤 숫자 만들기 (C#, C++) - soo:bak"
date: "2025-04-22 00:45:00 +0900"
description: 주어진 수를 제곱하고 중간 네 자리를 추출하는 방식으로 수열을 만들고, 값이 반복되기 전까지 몇 개의 숫자가 생성되는지를 구하는 백준 6500번 랜덤 숫자 만들기 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 6500
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 6500, 백준 6500번, BOJ 6500, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[6500번 - 랜덤 숫자 만들기](https://www.acmicpc.net/problem/6500)

## 설명
어떤 수를 정해진 방식으로 계속 변환하면서 새로운 수를 만들어나갈 때, **같은 수가 처음으로 다시 나타나기 전까지 총 몇 개의 수가 생성되는지**를 구하는 문제입니다.<br>
<br>

수의 변환 방식은 다음과 같습니다:
- 현재 수를 제곱한 후, 결과를 `100`으로 나눈 값을 `10,000`으로 나눈 나머지를 다음 수로 사용합니다.

<br>
즉, 아래와 같은 연산을 반복합니다:<br>

$$
x \rightarrow \left(\frac{x^2}{100}\right) \bmod 10000
$$

<br>
이 방식은 중간 네 자리를 추출하는 **Middle-Square 방식**과 유사합니다.<br>
<br>
`Middle-Square` 방식은 난수 생성 알고리듬의 한 종류로,<br>
<br>
주어진 수를 제곱한 후 중간 부분의 일부 자릿수를 추출하여 다음 난수로 사용하는 방법입니다.<br>
<br>
예를 들어 4자리 수 `1,234`를 제곱하면 `1,522,756`이 되고,<br>
<br>
여기서 중간의 4자리인 `5,227`을 추출하여 다음 수로 사용합니다.<br>
<br>
이 과정을 통해 수열을 계속 만들다 보면 언젠가는 이전에 나왔던 수가 다시 등장하게 됩니다.<br>
<br>
<br>
그리고, '반복' 이 발생하는 이유는 **비둘기집 원리** 때문입니다.<br>
<br>
비둘기집 원리란 `n + 1`개 이상의 물건을 `n`개의 상자에 넣을 때,<br>
<br>
적어도 하나의 상자에는 `2`개 이상의 물건이 들어가야 한다는 수학적 원리입니다.<br>
<br>
<br>
이 문제에서는 생성될 수 있는 모든 수가 `0`부터 `9,999`까지로 제한되어 있으므로,<br>
<br>
가능한 서로 다른 수의 최대 개수는 `10,000`개입니다.<br>
<br>
따라서 `10,000`개 이상의 수를 계속 생성한다면, 반드시 이전에 등장했던 수가 다시 나타나게 됩니다.<br>
<br>
<br>
마지막으로, 이 문제의 수 변환 방식은 같은 입력에 대해 항상 같은 결과를 내는 확정적인 규칙을 따릅니다.<br>
<br>
따라서, 수열에서 특정 숫자 `A` 다음에 `B`가 나왔다면, 이후에 다시 `A`가 나타날 때도 그 다음은 반드시 `B`가 됩니다.<br>
<br>
예를 들어, `4,567` 다음에 `8,342`가 계산되었다면, 나중에 다시 `4,567`이 등장할 때도 그 다음은 `8,342`가 됩니다.<br>
<br>
<br>
이러한 특성으로 인해 수열은 결국 다음과 같은 형태를 가지게 됩니다:<br>
- `초기값` → `값1` → `값2` → `...` → `값A` → `...` → `값B` → `값A`(여기서 처음으로 값이 반복됨)<br>
- 이후로는 `값A` → `...` → `값B` → `값A` → `...` 와 같이 같은 패턴이 반복됩니다.<br>

<br>
이 문제에서는 이러한 순환 구조에서 처음으로 값이 중복되기 전까지,<br>

<br>즉, 처음으로 이전에 나왔던 값이 다시 등장하기 전까지 **몇 개의 서로 다른 값이 만들어졌는지**를 찾는 것이 목표입니다.<br>


## 접근법
- 가능한 값의 범위는 `0`부터 `9999`까지이므로, 불리언 배열을 만들어 어떤 수가 등장했는지를 기록합니다.
- 매 연산마다 해당 수가 처음 보는 값인지 확인하고, 처음 본 값이면 배열에 표시 후 다음 수를 생성합니다.
- 이미 등장한 값이 나오면 그 즉시 중단하고, 지금까지 나온 수의 개수를 출력합니다.

이 과정을 입력마다 반복하면 되며, 각 테스트케이스는 수열의 길이가 길어도 `10,000`을 넘지 않으므로 시간 복잡도는 매우 작습니다.

<br>

## Code

### C#

```csharp
using System;

class Program {
  const int MOD = 10000;
  const int SHIFT = 100;

  static int Next(int x) => (x * x / SHIFT) % MOD;

  static void Main() {
    while (true) {
      int n = int.Parse(Console.ReadLine());
      if (n == 0) break;

      var visited = new bool[MOD];
      int cnt = 0;
      while (!visited[n]) {
        visited[n] = true;
        n = Next(n);
        cnt++;
      }

      Console.WriteLine(cnt);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
#define MOD 10000
#define SHIFT 100

using namespace std;
typedef long long ll;

ll nextNumber(ll x) {
  return (x * x / SHIFT) % MOD;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll n;
  while (cin >> n && n) {
    bool isVisited[MOD] = {0, };
    ll cnt = 0;
    while (!isVisited[n]) {
      isVisited[n] = true;
      n = nextNumber(n);
      cnt++;
    }

    cout << cnt << "\n";
  }

  return 0;
}
```
