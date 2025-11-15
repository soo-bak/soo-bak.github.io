---
layout: single
title: "[백준 5338] 마이크로소프트 로고 (C#, C++) - soo:bak"
date: "2025-11-15 00:15:00 +0900"
description: 정해진 ASCII 아트 그대로 마이크로소프트 로고를 출력하는 백준 5338번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[5338번 - 마이크로소프트 로고](https://www.acmicpc.net/problem/5338)

## 설명

입력 없이 예제와 동일한 ASCII 아트를 출력하기만 하면 되는 단순 출력 문제입니다.

<br>

## 접근법

주어진 모양을 그대로 출력하면 됩니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    Console.WriteLine("       _.-;;-._");
    Console.WriteLine("'-..-'|   ||   |");
    Console.WriteLine("'-..-'|_.-;;-._|");
    Console.WriteLine("'-..-'|   ||   |");
    Console.WriteLine("'-..-'|_.-''-._|");
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

  cout << "       _.-;;-._\n";
  cout << "'-..-'|   ||   |\n";
  cout << "'-..-'|_.-;;-._|\n";
  cout << "'-..-'|   ||   |\n";
  cout << "'-..-'|_.-''-._|\n";
  return 0;
}
```

