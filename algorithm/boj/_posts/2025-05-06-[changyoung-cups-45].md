---
layout: single
title: "[백준 3028] 창영마을 (C#, C++) - soo:bak"
date: "2025-05-06 08:37:00 +0900"
description: 세 개의 컵을 주어진 순서대로 교환하여 공의 위치를 추적하는 백준 3028번 창영마을 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[3028번 - 창영마을](https://www.acmicpc.net/problem/3028)

## 설명
세 개의 컵 중 하나에 공이 들어 있을 때 주어진 교환 순서대로 컵을 계속 바꿔나간 뒤,

**마지막에 공이 어떤 컵에 들어있는지를 알아내는 시뮬레이션 문제입니다.**

<br>
처음에는 **왼쪽에 있는 컵 (1번 컵)**에 공이 들어 있습니다.

이후 다음 세 가지 방식 중 하나로 교환이 진행됩니다:

- `A`: 1번 컵과 2번 컵 교환
- `B`: 2번 컵과 3번 컵 교환
- `C`: 1번 컵과 3번 컵 교환

<br>

## 접근법
- 공의 초기 위치를 표시합니다.
- 이후 각 문자를 순회하며 해당 조건에 따라 컵 위치를 교환합니다.
- 마지막에 공이 위치한 인덱스를 찾아 컵의 번호를 출력합니다.

<br>

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    var s = Console.ReadLine();
    bool[] cup = { true, false, false };

    foreach (var c in s) {
      if (c == 'A') (cup[0], cup[1]) = (cup[1], cup[0]);
      else if (c == 'B') (cup[1], cup[2]) = (cup[2], cup[1]);
      else if (c == 'C') (cup[0], cup[2]) = (cup[2], cup[0]);
    }

    for (int i = 0; i < 3; i++) {
      if (cup[i]) {
        Console.WriteLine(i + 1);
        break;
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

  string s; cin >> s;
  bool cup[3] = {true, };
  for (char c : s) {
    if (c == 'A') swap(cup[0], cup[1]);
    if (c == 'B') swap(cup[1], cup[2]);
    if (c == 'C') swap(cup[0], cup[2]);
  }
  for (int i = 0; i < 3; i++) {
    if (cup[i]) cout << i + 1 << "
";
  }

  return 0;
}
```
