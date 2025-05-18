---
layout: single
title: "[백준 7770] 아즈텍 피라미드 (C#, C++) - soo:bak"
date: "2025-05-18 20:39:00 +0900"
description: 주어진 블록 개수로 만들 수 있는 아즈텍 피라미드의 최대 높이를 계산하는 백준 7770번 아즈텍 피라미드 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[7770번 - 아즈텍 피라미드](https://www.acmicpc.net/problem/7770)

## 설명

주어진 블록 개수로 만들 수 있는 **가장 높은 아즈텍 피라미드의 높이를 계산하는 문제입니다.**

<br>
아즈텍 피라미드는 아래에서부터 위로 쌓아올리는 방식으로 구성되며,
각 층은 정사각형의 형태를 이루는 블록들로 채워져야 합니다.

* 가장 아래 층은 `1 x 1` 블록이 `1`개만 필요하고,
* 두 번째 층은 `3 x 3` 블록이 필요하며,
* 세 번째 층은 `5 x 5` 블록이 필요합니다.

<br>
즉, `i`번째 층을 쌓기 위해서는 다음 개수의 블록이 필요합니다:

$$
(2i - 1)^2 = 4i^2 - 4i + 1
$$

<br>
이처럼, 각 층을 올릴수록 필요한 블록 수가 급격히 증가하며,

주어진 블록 수 내에서 최대한 많은 층을 쌓는 것이 목표입니다.

<br>

## 접근법

처음에는 블록을 하나도 사용하지 않은 상태에서 시작하여,

가장 아래층부터 차례대로 쌓아올리며 블록을 차감합니다.

<br>
각 층을 쌓기 위해 필요한 블록의 개수는 다음과 같은 수식으로 표현됩니다:

$$
\text{필요 블록 수} = 2h^2 + 2h + 1
$$

<br>
이때, `h`는 현재까지 쌓은 피라미드의 높이입니다.

<br>
따라서 매 단계마다 위의 수식을 누적하면서,

전체 블록 개수를 초과하는 순간 중단하면 그 직전까지 쌓을 수 있었던 높이가 최댓값이 됩니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    int h = 0, total = 0;

    while (true) {
      int next = 2 * h * h + 2 * h + 1;
      if (total + next > n) break;
      total += next;
      h++;
    }

    Console.WriteLine(h);
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

  int n; cin >> n;
  int h = 0, b = 0;
  while (b <= n) {
    b += 2 * h * h + 2 * h + 1;
    h++;
  }

  cout << h - 1 << "\n";

  return 0;
}
```
