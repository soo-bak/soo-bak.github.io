---
layout: single
title: "[백준 13752] 히스토그램 (C#, C++) - soo:bak"
date: "2025-11-21 23:27:00 +0900"
description: 테스트 케이스마다 길이만큼 '='을 출력해 히스토그램을 만드는 백준 13752번 히스토그램 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[13752번 - 히스토그램](https://www.acmicpc.net/problem/13752)

## 설명

테스트 케이스의 개수 `N`이 주어지고, 이후 `N`개의 줄에 각각 정수 하나가 주어집니다.<br>

각 정수는 히스토그램 막대의 길이를 나타내며, 해당 길이만큼 `=` 문자를 반복하여 한 줄씩 출력하는 문제입니다.<br>

<br>

## 접근법

`N`개의 테스트 케이스를 순서대로 읽으며, 각 케이스마다 주어진 길이만큼 `=` 문자를 반복하여 출력합니다.<br>

예를 들어 길이가 `3`이면 `===`을, 길이가 `5`이면 `=====`를 출력합니다.

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

      for (var i = 0; i < n; i++) {
        var size = int.Parse(Console.ReadLine()!);
        Console.WriteLine(new string('=', size));
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

  int n; cin >> n;

  while (n--) {
    int size; cin >> size;
    cout << string(size, '=') << "\n";
  }

  return 0;
}
```

