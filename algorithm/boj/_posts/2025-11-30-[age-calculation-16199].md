---
layout: single
title: "[백준 16199] 나이 계산하기 (C#, C++) - soo:bak"
date: "2025-11-30 01:48:00 +0900"
description: 출생일과 기준일이 주어졌을 때 만 나이, 세는 나이, 연 나이를 각각 계산하는 백준 16199번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[16199번 - 나이 계산하기](https://www.acmicpc.net/problem/16199)

## 설명

생년월일과 기준 날짜가 주어지는 상황에서, 출생 연월일과 기준 연월일이 주어질 때, 세 가지 방식으로 계산한 나이를 구하는 문제입니다.

세 가지 나이 계산 방식은 다음과 같습니다:
- **만 나이**: 생일이 지났으면 (기준연도 - 출생연도), 생일이 지나지 않았으면 (기준연도 - 출생연도 - 1)
- **세는 나이**: 기준연도 - 출생연도 + 1
- **연 나이**: 기준연도 - 출생연도

입력은 항상 유효한 날짜이며, 기준일은 출생일과 같거나 이후입니다.

<br>

## 접근법

세 가지 나이는 모두 연도 차이를 기반으로 계산됩니다.

<br>
만 나이는 기준연도에서 출생연도를 뺀 후 1을 뺀 값에서 시작합니다. 기준 월이 출생 월보다 크거나, 같은 월인데 기준 일이 출생 일 이상이면 생일이 지난 것이므로 1을 더합니다.

세는 나이는 태어난 해를 1세로 계산하므로 기준연도에서 출생연도를 빼고 1을 더합니다. 연 나이는 단순히 기준연도에서 출생연도를 뺀 값입니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var birth = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
      var current = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);

      var birthYear = birth[0];
      var birthMonth = birth[1];
      var birthDay = birth[2];
      var currentYear = current[0];
      var currentMonth = current[1];
      var currentDay = current[2];

      var koreanAge = currentYear - birthYear + 1;
      var yearAge = currentYear - birthYear;
      
      var internationalAge = currentYear - birthYear - 1;
      if (currentMonth > birthMonth || (currentMonth == birthMonth && currentDay >= birthDay))
        internationalAge++;

      Console.WriteLine(internationalAge);
      Console.WriteLine(koreanAge);
      Console.WriteLine(yearAge);
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

  int birthYear, birthMonth, birthDay;
  cin >> birthYear >> birthMonth >> birthDay;
  int currentYear, currentMonth, currentDay;
  cin >> currentYear >> currentMonth >> currentDay;

  int koreanAge = currentYear - birthYear + 1;
  int yearAge = currentYear - birthYear;
  
  int internationalAge = currentYear - birthYear - 1;
  if (currentMonth > birthMonth || (currentMonth == birthMonth && currentDay >= birthDay))
    internationalAge++;

  cout << internationalAge << "\n";
  cout << koreanAge << "\n";
  cout << yearAge << "\n";

  return 0;
}
```


