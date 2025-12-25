---
layout: single
title: "[백준 19946] 2의 제곱수 계산하기 (C#, C++) - soo:bak"
date: "2025-12-25 14:56:00 +0900"
description: 한번의 -1 실수로 만들어진 값에서 처음 실수한 지점을 찾는 문제
---

## 문제 링크
[19946번 - 2의 제곱수 계산하기](https://www.acmicpc.net/problem/19946)

## 설명
2의 거듭제곱을 계산하다 한 번만 1을 빼는 실수를 했을 때, 최종 결과로부터 처음 실수한 지점을 찾는 문제입니다.

<br>

## 접근법
정상이라면 2^64가 되어야 하므로, 실수 시점이 K라면 최종 값은
`N = (2^K - 1) * 2^(64 - K) = 2^64 - 2^(64 - K)`가 됩니다.
따라서 `diff = 2^64 - N`은 2의 거듭제곱이고, `diff = 2^(64 - K)`입니다.
즉, diff의 자리수를 구해 `K = 64 - log2(diff)`를 계산하면 됩니다.

2^64는 unsigned 64비트 범위를 넘기므로, `diff = ~N + 1`로 계산합니다.
이 diff가 2의 거듭제곱이므로, 오른쪽 쉬프트로 지수만 구하면 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = ulong.Parse(Console.ReadLine()!);

    var diff = (~n) + 1;
    var p = 0;
    while (diff > 1) {
      diff >>= 1;
      p++;
    }

    var k = 64 - p;
    Console.WriteLine(k);
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

  unsigned long long n; cin >> n;
  unsigned long long diff = (~n) + 1ULL;

  int p = 0;
  while (diff > 1) {
    diff >>= 1;
    p++;
  }

  int k = 64 - p;
  cout << k << "\n";

  return 0;
}
```
