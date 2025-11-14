---
layout: single
title: "[백준 10699] 오늘 날짜 (C#, C++) - soo:bak"
date: "2025-11-08 23:29:00 +0900"
description: 채점 서버 시간대가 UTC 기준일 때 KST(UTC+9) 날짜를 YYYY-MM-DD로 출력하는 백준 10699번 오늘 날짜 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[10699번 - 오늘 날짜](https://www.acmicpc.net/problem/10699)

## 설명

입력 없이 서울 표준시(KST, UTC+9) 기준으로 오늘 날짜를 `YYYY-MM-DD` 형식으로 출력하는 문제입니다.<br>

채점 서버는 UTC 시간대를 사용하므로, 현재 UTC 시간에 9시간을 더해 한국 시간으로 변환해야 합니다.<br>

<br>

## 접근법

현재 UTC 시간을 구한 뒤 9시간을 더해 한국 시간으로 맞춘 후, 연-월-일을 `YYYY-MM-DD` 형식으로 출력합니다.

C#은 `DateTime.UtcNow.AddHours(9)`로 시간을 더한 후 `ToString("yyyy-MM-dd")`로 포맷팅하고,

C++은 `std::chrono`를 사용해 UTC 시간에 9시간을 더한 뒤 `gmtime`으로 변환하여 연-월-일을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var today = DateTime.UtcNow.AddHours(9);
      Console.WriteLine(today.ToString("yyyy-MM-dd"));
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  using namespace chrono;
  auto nowUtc = system_clock::now();
  auto nowKst = nowUtc + hours(9);
  time_t timer = system_clock::to_time_t(nowKst);
  tm* t = gmtime(&timer);

  cout << (t->tm_year + 1900) << '-'
       << setw(2) << setfill('0') << (t->tm_mon + 1) << '-'
       << setw(2) << setfill('0') << t->tm_mday << "\n";

  return 0;
}
```

