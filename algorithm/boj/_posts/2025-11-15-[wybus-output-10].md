---
layout: single
title: "[백준 14645] 와이버스 부릉부릉 (C#, C++) - soo:bak"
date: "2025-11-15 01:25:00 +0900"
description: 입력과 관계없이 \"비와이\"만 출력하면 되는 백준 14645번 와이버스 부릉부릉 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[14645번 - 와이버스 부릉부릉](https://www.acmicpc.net/problem/14645)

## 설명

입출력으로 승객의 정보가 주어지지만, 출력해야하는 것은 승객이 아닌 버스 운전수의 정보이므로 실제 출력은 언제나 `"비와이"`입니다.

<br>

## 접근법

입력을 무시하고 `"비와이"`를 출력하면 됩니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    Console.WriteLine("비와이");
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

  cout << "비와이\n";
  
  return 0;
}
```

