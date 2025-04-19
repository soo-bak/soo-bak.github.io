---
layout: single
title: "[백준 1453] 피시방 알바 (C#, C++) - soo:bak"
date: "2025-04-19 20:31:32 +0900"
description: 이미 자리가 차있을 경우 손님을 받지 않는 로직을 구현하는 백준 1453번 피시방 알바 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[1453번 - 피시방 알바](https://www.acmicpc.net/problem/1453)

## 설명
**피시방에 자리가 부족할 때 손님을 거절하는 경우의 수를 세는 간단한 시뮬레이션 문제**입니다.<br>
<br>

- 총 `100`개의 자리 중 일부가 사용될 수 있으며, 손님이 원하는 자리가 이미 사용 중이면 해당 손님은 받지 못합니다.<br>
- 각 손님이 원하는 자리 번호를 하나씩 제시할 때, 해당 자리가 비어 있으면 예약을 받고, 이미 차 있으면 거절합니다.<br>
- 최종적으로 거절된 손님의 수를 출력하는 문제입니다.<br>

## 접근법
- `100`개의 좌석에 대해 사용 여부를 저장하는 불리언 배열을 선언합니다.<br>
- 각 손님의 요청을 순회하면서 해당 자리가 비어 있는지 확인하며 :<br>
  - 해당 자리가 비어있지 않다면 거절 수를 증가시킵니다.<br>
- 배열 인덱스는 `0`부터 시작하므로, 입력받은 자리 번호에서 `1`을 뺀 값을 인덱스로 사용합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    bool[] occupied = new bool[100];
    int cnt = int.Parse(Console.ReadLine());
    var inputs = Console.ReadLine().Split();
    int rejected = 0;

    for (int i = 0; i < cnt; i++) {
      int seat = int.Parse(inputs[i]) - 1;
      if (occupied[seat])
        rejected++;
      else
        occupied[seat] = true;
    }

    Console.WriteLine(rejected);
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  bool sieve[100] = {false, };

  int cntC; cin >> cntC;
  int ans = 0;
  for (int i = 0; i < cntC; i++) {
    int s; cin >> s;
    if (sieve[s - 1]) ans++;
    else sieve[s - 1] = true;
  }

  cout << ans << "\n";

  return 0;
}
```
