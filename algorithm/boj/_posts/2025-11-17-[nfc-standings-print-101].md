---
layout: single
title: "[백준 10170] NFC West vs North (C#, C++) - soo:bak"
date: "2025-11-17 23:03:00 +0900"
description: NFC 서부·북부 디비전 순위를 예제 그대로 출력하는 백준 10170번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[10170번 - NFC West vs North](https://www.acmicpc.net/problem/10170)

## 설명

NFC West와 NFC North 디비전의 순위표를 출력하는 문제입니다.<br>

입력은 없으며, 문제에서 주어진 표를 그대로 출력합니다.<br>

<br>

## 접근법

주어진 표를 그대로 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      Console.WriteLine("NFC West       W   L  T");
      Console.WriteLine("-----------------------");
      Console.WriteLine("Seattle        13  3  0");
      Console.WriteLine("San Francisco  12  4  0");
      Console.WriteLine("Arizona        10  6  0");
      Console.WriteLine("St. Louis      7   9  0");
      Console.WriteLine();
      Console.WriteLine("NFC North      W   L  T");
      Console.WriteLine("-----------------------");
      Console.WriteLine("Green Bay      8   7  1");
      Console.WriteLine("Chicago        8   8  0");
      Console.WriteLine("Detroit        7   9  0");
      Console.WriteLine("Minnesota      5  10  1");
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

  cout << "NFC West       W   L  T\n";
  cout << "-----------------------\n";
  cout << "Seattle        13  3  0\n";
  cout << "San Francisco  12  4  0\n";
  cout << "Arizona        10  6  0\n";
  cout << "St. Louis      7   9  0\n\n";
  cout << "NFC North      W   L  T\n";
  cout << "-----------------------\n";
  cout << "Green Bay      8   7  1\n";
  cout << "Chicago        8   8  0\n";
  cout << "Detroit        7   9  0\n";
  cout << "Minnesota      5  10  1\n";

  return 0;
}
```

