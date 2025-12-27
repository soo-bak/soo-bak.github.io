---
layout: single
title: "[백준 1676] 팩토리얼 0의 개수 (C#, C++) - soo:bak"
date: "2025-10-27 22:00:00 +0900"
description: 팩토리얼의 뒤에서 처음 만나는 0의 개수를 5의 배수 누적 합으로 계산하는 백준 1676번 팩토리얼 0의 개수 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1676
  - C#
  - C++
  - 알고리즘
  - 수학
keywords: "백준 1676, 백준 1676번, BOJ 1676, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1676번 - 팩토리얼 0의 개수](https://www.acmicpc.net/problem/1676)

## 설명

`N!`을 계산했을 때 맨 뒤에 연속으로 붙는 `0`의 개수를 묻습니다.<br>

팩토리얼 수 자체는 매우 커지지만, `0`이 생기는 이유는 인수에 포함된 `10`, 다시 말해 `2 × 5` 조합에서 나오므로 **인수만 보면 충분**합니다.<br>

<br>

## 접근법

팩토리얼의 뒤에 붙는 `0`은 `10 = 2 × 5`의 개수로 결정됩니다.  
팩토리얼에는 `2의 인수`가 훨씬 많으므로, **5가 몇 번 등장하는지만 세면 됩니다.**

- `5`의 배수마다 5가 한 번씩 등장합니다.
- `25`, `125`처럼 5의 거듭제곱은 5가 여러 번 포함되므로 그만큼 추가합니다.
- 따라서 `N`을 5로 나누고, 몫을 계속 더하면서 `N`을 5로 갱신합니다.

<br>
반복문이 `log₅ N`만큼만 실행되므로 시간 복잡도는 매우 작습니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var ans = 0;
    while (n > 0) {
      n /= 5;
      ans += n;
    }
    Console.WriteLine(ans);
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

  int ans = 0;
  while (n > 0) {
    n /= 5;
    ans += n;
  }

  cout << ans << "\n";
  
  return 0;
}
```
