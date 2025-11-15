---
layout: single
title: "[백준 6749] Next in line (C#, C++) - soo:bak"
date: "2025-11-15 01:05:00 +0900"
description: 등차수열 관계를 이용해 막내와 둘째를 보고 첫째 나이를 구하는 백준 6749번 Next in line 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[6749번 - Next in line](https://www.acmicpc.net/problem/6749)

## 설명

세 사람의 나이가 등차수열을 이룬다고 할 때, 막내와 둘째의 나이를 보고 첫째의 나이를 구하는 문제입니다.<br>

등차수열은 연속된 항들의 차이가 일정한 수열입니다.<br>

막내를 `Y`, 둘째를 `M`, 첫째를 `O`라고 하면, `M - Y = O - M`의 관계가 성립합니다.<br>

<br>

## 접근법

등차수열의 성질을 이용한 수식 계산으로 해결합니다.

막내와 둘째의 나이를 입력받고, 두 나이의 차이 `M - Y`를 구합니다.

등차수열에서는 연속된 항들의 차이가 일정하므로, 첫째의 나이는 둘째의 나이에 같은 차이를 더한 `M + (M - Y)`가 됩니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    var y = int.Parse(Console.ReadLine()!);
    var m = int.Parse(Console.ReadLine()!);
    Console.WriteLine(m + (m - y));
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

  int y, m; cin >> y >> m;
  cout << m + (m - y) << "\n";
  
  return 0;
}
```

