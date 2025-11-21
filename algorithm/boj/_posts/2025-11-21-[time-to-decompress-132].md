---
layout: single
title: "[백준 17010] Time to Decompress (C#, C++) - soo:bak"
date: "2025-11-21 23:43:00 +0900"
description: 각 줄의 숫자만큼 문자를 반복해 압축을 해제하는 백준 17010번 Time to Decompress 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[17010번 - Time to Decompress](https://www.acmicpc.net/problem/17010)

## 설명

압축된 데이터를 해제하는 문제입니다.<br>

첫 줄에 줄의 개수 `L`이 주어지고, 이후 `L`개의 줄에 각각 정수 `N`과 문자 `c`가 주어집니다.<br>

각 줄마다 문자 `c`를 `N`번 반복한 문자열을 출력합니다.<br>

<br>

## 접근법

`L`개의 줄을 순서대로 읽으며 각 줄에서 정수 `N`과 문자 `c`를 입력받습니다.<br>

문자 `c`를 `N`번 반복하여 한 줄로 출력합니다. 예를 들어 `5 a`가 입력되면 `aaaaa`를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var l = int.Parse(Console.ReadLine()!);

      for (var i = 0; i < l; i++) {
        var line = Console.ReadLine()!.Split();
        var count = int.Parse(line[0]);
        var ch = line[1][0];
        Console.WriteLine(new string(ch, count));
      }
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

  int L; cin >> L;

  while (L--) {
    int count; char ch; cin >> count >> ch;

    for (int i = 0; i < count; ++i)
      cout << ch;
    cout << "\n";
  }

  return 0;
}
```

