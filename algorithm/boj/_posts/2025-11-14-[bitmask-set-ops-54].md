---
layout: single
title: "[백준 11723] 집합 (C#, C++) - soo:bak"
date: "2025-11-14 22:58:00 +0900"
description: 1부터 20까지의 원소에 대해 비트마스크로 집합 연산을 처리하는 백준 11723번 집합 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 11723
  - C#
  - C++
  - 알고리즘
  - 구현
  - set
  - 비트마스킹
keywords: "백준 11723, 백준 11723번, BOJ 11723, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11723번 - 집합](https://www.acmicpc.net/problem/11723)

## 설명

공집합에서 시작하여 `add`, `remove`, `check`, `toggle`, `all`, `empty` 연산을 처리하며 집합을 관리하는 문제입니다.<br>

원소는 `1`부터 `20`까지로 제한되어 있어, 각 원소를 정수의 비트 하나로 표현할 수 있습니다.

`check` 명령이 등장할 때마다 해당 원소가 집합에 포함되어 있으면 `1`, 없으면 `0`을 출력합니다.<br>

<br>

## 접근법

비트마스크를 사용하여 집합을 정수 하나로 표현합니다.

원소가 `1`부터 `20`까지 제한되어 있으므로, 정수의 각 비트를 원소의 포함 여부로 사용할 수 있습니다.

원소 `x`는 `(x - 1)`번째 비트에 대응되므로, 원소 `1`은 `0`번째 비트, 원소 `20`은 `19`번째 비트를 사용합니다.

<br>
`add x`는 원소를 추가하는 연산입니다. `1 << (x - 1)`로 해당 비트만 켜진 값을 만든 후, OR 연산 `mask |= bit`으로 마스크에 추가합니다.

`remove x`는 원소를 제거하는 연산입니다. `~(1 << (x - 1))`로 해당 비트만 꺼진 값을 만든 후, AND 연산 `mask &= ~bit`으로 마스크에서 제거합니다.

`check x`는 원소의 포함 여부를 확인합니다. `mask & (1 << (x - 1))`의 결과가 `0`이 아니면 `1`을, `0`이면 `0`을 출력합니다.

`toggle x`는 원소의 포함 여부를 반전시킵니다. XOR 연산 `mask ^= 1 << (x - 1)`을 사용하여 해당 비트를 토글합니다.

`all`은 모든 원소를 포함하는 연산입니다. `mask = (1 << 20) - 1`로 하위 20개 비트를 모두 켭니다.

`empty`는 모든 원소를 제거하는 연산입니다. `mask = 0`으로 마스크를 초기화합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.IO;
using System.Linq;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      using var sw = new StreamWriter(Console.OpenStandardOutput());
      var m = int.Parse(Console.ReadLine()!);
      var mask = 0;

      for (var i = 0; i < m; i++) {
        var tokens = Console.ReadLine()!.Split();
        var cmd = tokens[0];

        if (cmd == "all") mask = (1 << 20) - 1;
        else if (cmd == "empty") mask = 0;
        else {
          var x = int.Parse(tokens[1]) - 1;
          var bit = 1 << x;
          switch (cmd) {
            case "add":
              mask |= bit;
              break;
            case "remove":
              mask &= ~bit;
              break;
            case "check":
              sw.WriteLine((mask & bit) != 0 ? 1 : 0);
              break;
            case "toggle":
              mask ^= bit;
              break;
          }
        }
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

  int m; cin >> m;
  int mask = 0;

  while (m--) {
    string cmd; cin >> cmd;
    if (cmd == "all") mask = (1 << 20) - 1;
    else if (cmd == "empty") mask = 0;
    else {
      int x; cin >> x;
      int bit = 1 << (x - 1);
      if (cmd == "add") mask |= bit;
      else if (cmd == "remove") mask &= ~bit;
      else if (cmd == "check") cout << ((mask & bit) ? 1 : 0) << "\n";
      else if (cmd == "toggle") mask ^= bit;
    }
  }

  return 0;
}
```
