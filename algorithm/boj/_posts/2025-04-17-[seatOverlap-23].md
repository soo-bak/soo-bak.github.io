---
layout: single
title: "[백준 5176] 대회 자리 (C#, C++) - soo:bak"
date: "2025-04-17 00:27:43 +0900"
description: 앉으려는 자리가 이미 차 있는 경우의 횟수를 세는 시뮬레이션 문제인 백준 5176번 대회 자리 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5176
  - C#
  - C++
  - 알고리즘
  - 구현
  - set
keywords: "백준 5176, 백준 5176번, BOJ 5176, seatOverlap, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5176번 - 대회 자리](https://www.acmicpc.net/problem/5176)

## 설명
**각 참가자가 앉으려는 자리가 이미 다른 사람이 앉아 있는지 여부를 체크하여,** <br>
<br>
**자리를 겹쳐 앉는 시도를 몇 번 했는지 구하는 문제**입니다.<br>
<br>

- 입력으로는 **참가자 수**와 **좌석 수**, 그리고 각 참가자가 **원하는 좌석 번호**가 주어집니다.<br>
- 좌석 번호는 `1`번부터 시작하며, 이미 누군가가 앉아 있다면 해당 참가자는 앉지 못합니다.<br>
- 이때 **앉지 못한 참가자의 수**를 출력하면 됩니다.<br>

### 접근법
- 좌석 수만큼의 크기를 가지는 `bool` 배열을 생성하여 해당 좌석이 사용 중인지 여부를 기록합니다.<br>
- 참가자의 좌석 요청을 순서대로 처리하면서 이미 사용된 좌석이라면 카운트를 증가시킵니다.<br>
- 최종적으로 겹쳐 앉으려 한 횟수를 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var parts = Console.ReadLine().Split();
      int cntP = int.Parse(parts[0]);
      int cntS = int.Parse(parts[1]);

      var isDup = new bool[cntS + 1];
      int cntN = 0;

      for (int i = 0; i < cntP; i++) {
        int idx = int.Parse(Console.ReadLine());
        if (isDup[idx]) cntN++;
        else isDup[idx] = true;
      }

      Console.WriteLine(cntN);
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<bool> vb;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int cntP, cntS; cin >> cntP >> cntS;
    vb isDup(cntS + 1, false);
    int cntN = 0;
    for (int i = 0; i < cntP; i++) {
      int idx; cin >> idx;
      if (isDup[idx]) cntN++;
      else isDup[idx] = true;
    }
    cout << cntN << "\n";
  }

  return 0;
}
```
