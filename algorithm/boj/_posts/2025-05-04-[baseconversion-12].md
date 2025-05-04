---
layout: single
title: "[백준 2745] 진법 변환 (C#, C++) - soo:bak"
date: "2025-05-04 09:03:00 +0900"
description: 주어진 B진법 수를 10진법으로 변환하는 과정을 구현하는 백준 2745번 진법 변환 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[2745번 - 진법 변환](https://www.acmicpc.net/problem/2745)

## 설명
임의의 `B진법`으로 주어진 수를 `10진법`으로 변환하는 문제입니다.

<br>
각 자리의 문자를 오른쪽에서부터 차례로 확인하면서,

해당 문자의 값에 B의 거듭제곱을 곱해 모두 더한 값을 출력하면 됩니다.

<br>

---

## 접근법

각 자리의 문자를 **가장 오른쪽(1의 자리)**부터 차례대로 확인하면서,

해당 문자가 의미하는 값을 **기수 `B`의 자리값(거듭제곱)**과 곱하여 모두 더하면,

**B진법 수를 10진법으로 변환한 값**이 됩니다.

<br>
예를 들어, 진법이 `B`일 때 수 `N = d_0 d_1 ... d_(n-1)` 은 다음과 같은 수식으로 계산됩니다:

$$
N_{value} = d_0 \cdot B^{n-1} + d_1 \cdot B^{n-2} + \cdots + d_{n-1} \cdot B^0
$$

이 원리를 코드로 그대로 구현하면 됩니다.

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    string s = input[0];
    int b = int.Parse(input[1]);

    int res = 0;
    for (int i = 0; i < s.Length; i++) {
      int digit = s[i] >= 'A' ? s[i] - 'A' + 10 : s[i] - '0';
      res = res * b + digit;
    }

    Console.WriteLine(res);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string s; int b; cin >> s >> b;
  int n = s.size();

  vi pow(n);
  pow[0] = 1;
  for (int i = 1; i < n; i++)
    pow[i] = pow[i - 1] * b;

  int ans = 0;
  for (int i = 0; i < n; i++) {
    int d = isalpha(s[i]) ? s[i] - 55 : s[i] - 48;
    ans += d * pow[n - 1 - i];
  }
  cout << ans << "\n";

  return 0;
}
```
