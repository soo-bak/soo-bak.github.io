---
layout: single
title: "[백준 11320] 삼각 무늬 - 1 (C#, C++) - soo:bak"
date: "2025-05-05 03:15:00 +0900"
description: 큰 정삼각형을 작은 정삼각형으로 완전히 덮기 위해 필요한 개수를 계산하는 백준 11320번 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[11320 - 삼각 무늬 - 1](https://www.acmicpc.net/problem/11320)

## 설명

한 변의 길이가 `A`인 정삼각형을,

한 변의 길이가 `B`인 정삼각형 여러 개로 **완전히 덮기 위해 필요한 최소 개수**를 구하는 문제입니다.

<br>
문제에서 주어지는 조건은 다음과 같습니다:
- `B`는 `A`보다 작거나 같다.
- `A`는 `B`로 나누어떨어진다.

즉, 큰 정삼각형을 작은 정삼각형들로 **완벽히 겹치거나 격자처럼 채워넣는 상황**을 가정할 수 있습니다.

<br>

## 접근법
- 큰 삼각형의 각 변을 따라 작은 삼각형을 나열할 수 있는 개수는 `A / B개`입니다:<br>
  이는 작은 삼각형의 한 변의 길이 `B`가 큰 삼각형의 한 변 `A`를 정확히 나누기 때문입니다.
- 한 줄에 `A / B개`의 작은 삼각형이 배치되고,<br>
  같은 방식으로 총 `A / B줄`이 쌓이게 되므로,<br>
- 최종적으로 필요한 삼각형의 개수는 다음과 같이 계산됩니다:

  $$
  \left( \frac{A}{B} \right)^2
  $$

- 각 테스트케이스마다 위 수식을 계산한 결과를 출력합니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var input = Console.ReadLine().Split();
      int a = int.Parse(input[0]);
      int b = int.Parse(input[1]);

      int div = a / b;
      int res = div * div;

      Console.WriteLine(res);
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

  int t; cin >> t;
  while (t--) {
    int a, b; cin >> a >> b;
    int div = a / b;
    int ans = div * div;
    cout << ans << "\n";
  }

  return 0;
}
```
