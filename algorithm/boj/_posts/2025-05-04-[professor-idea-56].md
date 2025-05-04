---
layout: single
title: "[백준 1731] 추론 (C#, C++) - soo:bak"
date: "2025-05-04 17:39:00 +0900"
description: 등차수열과 등비수열 중 어떤 규칙인지 판별하여 다음 항을 구하는 백준 1731번 추론 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[1731번 - 추론](https://www.acmicpc.net/problem/1731)

## 설명

주어진 수열이 **등차수열**인지 **등비수열**인지 판별한 뒤,

그 규칙에 따라 **다음 항**을 계산하여 출력하는 문제입니다.

<br>

## 접근법

- 입력으로 주어진 수열의 길이는 `최소 3 이상`이므로,<br>
  앞의 몇 항을 비교하여 등차인지 등비인지 충분히 판단할 수 있습니다.

- 수열의 첫 번째, 두 번째 항을 기준으로 다음과 같이 두 가지 가능성을 확인합니다.
  - **등차수열인 경우**: 두 수의 차이 `d = 두 번째 항 - 첫 번째 항`
  - **등비수열인 경우**: 두 수의 비율 `r = 두 번째 항 ÷ 첫 번째 항`

- 이후 전체 수열을 순회하며,
  - 각 인접한 두 항의 차이가 항상 `d`이면 등차수열
  - 각 인접한 두 항의 비율이 항상 `r`이면 등비수열입니다.

<br>
- 주어진 수열이 등차수열이면 다음 항은:<br>
  $$
  a_n = a_{{n-1}} + d
  $$

- 등비수열이면 다음 항은:<br>
  $$
  a_n = a_{{n-1}} \times r
  $$

<br>

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());

    var a = new int[n];
    for (int i = 0; i < n; i++)
      a[i] = int.Parse(Console.ReadLine());

    bool isArith = true;
    int d = a[1] - a[0];
    for (int i = 2; i < n; i++)
      if (a[i] - a[i - 1] != d)
        isArith = false;

    int ans = isArith ? a[n - 1] + d : a[n - 1] * (a[1] / a[0]);
    Console.WriteLine(ans);
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

  int n; cin >> n;
  vi a(n);
  for (int i = 0; i < n; i++)
    cin >> a[i];

  bool isArith = true;
  int d = a[1] - a[0];
  for (int i = 2; i < n; i++)
    if (a[i] - a[i - 1] != d) isArith = false;

  int ans = isArith ? a[n - 1] + d : a[n - 1] * (a[1] / a[0]);
  cout << ans << "\n";

  return 0;
}
```
