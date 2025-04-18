---
layout: single
title: "[백준 2420] 사파리 월드 (C#, C++) - soo:bak"
date: "2025-04-19 03:01:12 +0900"
description: 두 정수의 차이의 절댓값을 계산하는 단순한 구현 문제인 백준 2420번 사파리 월드 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[2420번 - 사파리 월드](https://www.acmicpc.net/problem/2420)

## 설명
**두 정수의 차이의 절댓값을 구하는 단순한 구현 문제**입니다.<br>
<br>

- 입력으로 두 정수 `n`, `m`이 주어집니다.<br>
- 이 두 수의 차이의 **절댓값**을 계산하여 출력하면 됩니다.<br>
- 자료형 오버플로에 주의해야 하므로 `long` 또는 `long long`을 사용합니다.<br>

### 접근법
- `n - m` 또는 `m - n`을 계산한 뒤, `abs()` 함수를 통해 절댓값을 구합니다.<br>
- C++에서는 `ll`(long long), C#에서는 `long` 자료형을 사용하여 범위를 안전하게 처리합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    long n = long.Parse(input[0]);
    long m = long.Parse(input[1]);

    Console.WriteLine(Math.Abs(n - m));
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll n, m; cin >> n >> m;
  cout << abs(n - m) << "\n";

  return 0;
}
```
