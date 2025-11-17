---
layout: single
title: "[백준 15439] 베라의 패션 (C#, C++) - soo:bak"
date: "2025-11-17 23:03:00 +0900"
description: 상·하의 색상이 다른 조합의 수를 n×(n-1)로 계산하는 백준 15439번 베라의 패션 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[15439번 - 베라의 패션](https://www.acmicpc.net/problem/15439)

## 설명

베라는 `N`벌의 상의와 `N`벌의 하의를 가지고 있으며, 각각의 색상은 `1`번부터 `N`번까지 모두 다릅니다.<br>

상의와 하의의 색상이 다른 조합의 수를 구해야 합니다.<br>

상의를 하나 선택하면 `N`가지 선택이 가능하고, 하의는 상의와 같은 색을 제외한 `N - 1`가지를 선택할 수 있습니다.

따라서 총 조합의 수는 `N × (N - 1)`입니다.<br>

<br>

## 접근법

상의 `N`가지 중 하나를 선택하고, 하의는 상의와 색이 다른 `N - 1`가지 중 하나를 선택하므로 `N × (N - 1)`을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      Console.WriteLine(n * (n - 1));
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

  int n; cin >> n;

  cout << n * (n - 1) << "\n";

  return 0;
}
```

