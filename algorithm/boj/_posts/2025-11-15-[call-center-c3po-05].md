---
layout: single
title: "[백준 5339] 콜센터 (C#, C++) - soo:bak"
date: "2025-11-15 01:10:00 +0900"
description: 예제 ASCII 아트를 그대로 출력하는 백준 5339번 콜센터 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[5339번 - 콜센터](https://www.acmicpc.net/problem/5339)

## 설명

입력 없이 콜센터에 앉아 있는 C3PO를 예제와 동일하게 출력하는 문제입니다.

<br>

## 접근법

주어진 ASCII 아트를 그대로 출력하면 됩니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    Console.WriteLine("     /~\\");
    Console.WriteLine("    ( oo|");
    Console.WriteLine("    _\\=/_");
    Console.WriteLine("   /  _  \\");
    Console.WriteLine("  //|/.\\|\\\\");
    Console.WriteLine(" ||  \\ /  ||");
    Console.WriteLine("============");
    for (var i = 0; i < 3; i++)
      Console.WriteLine("|          |");
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

  cout << "     /~\\\n";
  cout << "    ( oo|\n";
  cout << "    _\\=/_\n";
  cout << "   /  _  \\\n";
  cout << "  //|/.\\|\\\\\n";
  cout << " ||  \\ /  ||\n";
  cout << "============\n";
  for (int i = 0; i < 3; ++i)
    cout << "|          |\n";
  
  return 0;
}
```

