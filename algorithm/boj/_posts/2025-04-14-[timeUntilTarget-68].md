---
layout: single
title: "[백준 1408] 24 (C#, C++) - soo:bak"
date: "2025-04-14 20:48:58 +0900"
description: 현재 시각과 설정된 시각 사이의 차이를 구하는 백준 1408번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[1408번 - 24](https://www.acmicpc.net/problem/1408)

## 설명
**현재 시각**과 **임무 시작 시각**이 주어졌을 때,  <br>
그 사이에 남은 시간을 **시:분:초 형식**으로 출력하는 문제입니다.

---

## 접근법
- 현재 시각과 시작 시각을 **초 단위로 환산**합니다.
- 시작 시각이 더 늦다면 단순히 두 값을 뺀 차이만큼의 초가 답입니다.
- 현재 시각이 더 늦다면 **자정(24시간 = 86400초)**을 기준으로
  다음 날 시작 시각까지의 차이를 구합니다: <br>

$$\text{남은 시간} = 86400 - (현재 초 - 시작 초)$$

- 계산된 초 값을 다시 `hh:mm:ss`로 변환하여 출력합니다.
  - 이때 자릿수는 항상 `2자리`로 맞춰주어어야 합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var now = Console.ReadLine()!.Split(':');
      var target = Console.ReadLine()!.Split(':');

      int nowSec = int.Parse(now[0]) * 3600 + int.Parse(now[1]) * 60 + int.Parse(now[2]);
      int targetSec = int.Parse(target[0]) * 3600 + int.Parse(target[1]) * 60 + int.Parse(target[2]);

      int diffSec = targetSec >= nowSec ? targetSec - nowSec : 86400 - (nowSec - targetSec);

      Console.WriteLine($@"{diffSec / 3600:D2}:{(diffSec % 3600) / 60:D2}:{diffSec % 60:D2}");
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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string now, sTime;
  cin >> now >> sTime;

  int nowSec = stoi(now.substr(0, 2)) * 3600 +
               stoi(now.substr(3, 2)) * 60 +
               stoi(now.substr(6, 2));
  int sTimeSec = stoi(sTime.substr(0, 2)) * 3600 +
                 stoi(sTime.substr(3, 2)) * 60 +
                 stoi(sTime.substr(6, 2));

  int diffSec = (sTimeSec >= nowSec) ? sTimeSec - nowSec : 86400 - (nowSec - sTimeSec);

  cout << setw(2) << setfill('0') << diffSec / 3600 << ":"
       << setw(2) << setfill('0') << (diffSec % 3600) / 60 << ":"
       << setw(2) << setfill('0') << diffSec % 60 << "\n";
}
```
