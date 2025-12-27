---
layout: single
title: "[백준 4118] Fred's Lotto Tickets (C#, C++) - soo:bak"
date: "2025-12-06 21:50:00 +0900"
description: 여러 장의 로또 티켓이 1부터 49까지 모든 번호를 포함하는지 판정하는 백준 4118번 Fred's Lotto Tickets 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 4118
  - C#
  - C++
  - 알고리즘
keywords: "백준 4118, 백준 4118번, BOJ 4118, FredsLottoTickets, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4118번 - Fred's Lotto Tickets](https://www.acmicpc.net/problem/4118)

## 설명
각 테스트케이스에서 N장의 로또 티켓이 주어집니다. 티켓 한 장에는 1~49 사이의 중복 없는 6개 숫자가 적혀 있습니다.

모든 티켓을 합쳐 1부터 49까지 모든 숫자가 적어도 한 번씩 등장하면 Yes, 하나라도 빠지면 No를 출력하는 문제입니다.

<br>

## 접근법
먼저, 49칸짜리 배열이나 비트마스크를 만들어 숫자가 나오면 해당 위치를 표시합니다.

다음으로, 한 테스트케이스에서 숫자는 총 6 * N개이므로 바로 읽어가며 갱신합니다.

이후, 모든 숫자를 처리한 뒤 표시된 개수가 49이면 Yes, 아니면 No를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      while (true) {
        var line = Console.ReadLine();
        if (line == null) break;
        var n = int.Parse(line);
        if (n == 0) break;

        var seen = new bool[49];
        for (var i = 0; i < n; i++) {
          var parts = Console.ReadLine()!.Split();
          for (var j = 0; j < 6; j++) {
            var num = int.Parse(parts[j]);
            seen[num - 1] = true;
          }
        }

        var cnt = 0;
        for (var i = 0; i < 49; i++) {
          if (seen[i]) cnt++;
        }
        Console.WriteLine(cnt == 49 ? "Yes" : "No");
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

  int n;
  while (cin >> n) {
    if (n == 0) break;

    bitset<49> bits;
    for (int i = 0; i < 6 * n; i++) {
      int num; cin >> num;
      bits.set(num - 1);
    }

    cout << (bits.count() == 49 ? "Yes" : "No") << "\n";
  }

  return 0;
}
```
