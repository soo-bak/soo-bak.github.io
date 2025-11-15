---
layout: single
title: "[백준 5337] 웰컴 (C#, C++) - soo:bak"
date: "2025-11-15 00:25:00 +0900"
description: 예제와 동일한 ASCII 아트를 그대로 출력하는 백준 5337번 웰컴 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[5337번 - 웰컴](https://www.acmicpc.net/problem/5337)

## 설명

입력 없이 “Welcome” ASCII 아트를 그대로 출력하는 문제입니다.

<br>

## 접근법

예제 출력과 동일한 문자열을 그대로 출력하면 됩니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    Console.WriteLine(".  .   .");
    Console.WriteLine("|  | _ | _. _ ._ _  _");
    Console.WriteLine("|/\\|(/.|(_.(_)[ | )(/.");
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

  cout << ".  .   .\n";
  cout << "|  | _ | _. _ ._ _  _\n";
  cout << "|/\\|(/.|(_.(_)[ | )(/.\n";
  return 0;
}
```

