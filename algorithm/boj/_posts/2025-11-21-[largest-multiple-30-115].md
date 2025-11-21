---
layout: single
title: "[백준 10610] 30 (C#, C++) - soo:bak"
date: "2025-11-21 23:27:00 +0900"
description: 숫자들의 조합으로 30의 배수가 되는 가장 큰 수를 찾는 백준 10610번 30 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[10610번 - 30](https://www.acmicpc.net/problem/10610)

## 설명

주어진 숫자의 자릿수를 재배열하여 만들 수 있는 가장 큰 `30`의 배수를 구하는 문제입니다.

만들 수 없다면 `-1`을 출력합니다.<br>

<br>

## 접근법

`30`의 배수가 되려면 `10`의 배수이면서 `3`의 배수여야 합니다.

`10`의 배수는 일의 자리가 `0`이어야 하므로, 주어진 숫자에 `0`이 최소 하나 이상 포함되어야 합니다.

`3`의 배수는 모든 자릿수의 합이 `3`의 배수일 때 성립합니다.

예를 들어 `102`는 `1 + 0 + 2 = 3`이므로 `3`의 배수입니다.<br>

<br>
주어진 숫자에 `0`이 포함되어 있는지, 모든 자릿수의 합이 `3`의 배수인지 확인합니다.

두 조건 중 하나라도 만족하지 않으면 `-1`을 출력합니다.<br>

<br>
두 조건을 모두 만족한다면 자릿수를 내림차순으로 정렬합니다.

가장 큰 자리에 큰 숫자를 배치할수록 전체 값이 커지기 때문입니다.

예를 들어 `1`, `0`, `2`로는 `210 > 201 > 120`이므로 내림차순인 `210`이 최댓값입니다.

내림차순 정렬하면 자동으로 끝자리가 `0`이 되어 `10`의 배수 조건도 만족합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Linq;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var digits = Console.ReadLine()!;

      if (!digits.Contains('0') || digits.Sum(ch => ch - '0') % 3 != 0) {
        Console.WriteLine(-1);
        return;
      }

      var result = new string(digits.OrderByDescending(ch => ch).ToArray());
      Console.WriteLine(result);
    }
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

  string digits; cin >> digits;

  bool hasZero = false;
  ll sum = 0;
  for (char ch : digits) {
    int d = ch - '0';
    if (d == 0) hasZero = true;
    sum += d;
  }

  if (!hasZero || sum % 3 != 0) {
    cout << -1 << "\n";
    return 0;
  }

  sort(digits.rbegin(), digits.rend());
  cout << digits << "\n";

  return 0;
}
```

