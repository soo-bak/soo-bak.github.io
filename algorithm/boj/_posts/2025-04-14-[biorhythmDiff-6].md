---
layout: single
title: "[백준 23292] 생체리듬 (C#, C++) - soo:bak"
date: "2025-04-14 05:01:09 +0900"
description: 생일과 날짜 간의 자릿수 제곱 차이를 기반으로 생체 유사도를 계산하는 백준 23292번 생체리듬 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 23292
  - C#
  - C++
  - 알고리즘
keywords: "백준 23292, 백준 23292번, BOJ 23292, biorhythmDiff, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23292번 - 생체리듬](https://www.acmicpc.net/problem/23292)

## 설명
이 문제는 어떤 기준 생일(8자리 숫자)과 여러 날짜를 비교하여  <br>
**생체 유사도 지수가 가장 높은 날짜**를 구하는 문제입니다.

생체 유사도는 다음과 같은 방식으로 계산됩니다:

- 생년월일은 8자리 (`YYYYMMDD`)로 주어집니다.
- 이를 세 그룹으로 나누어 계산합니다:
  - 연(4자리)
  - 월(2자리)
  - 일(2자리)
- 각 그룹 내의 **같은 자릿수끼리 차를 제곱한 뒤 더한 값**을 계산한 후,
  세 그룹의 값을 모두 곱한 결과가 해당 날짜의 생체 유사도입니다.

---

## 접근법
- 입력된 생일과 각 날짜를 비교합니다.
- 연도 4자리 → 월 2자리 → 일 2자리로 나누고, 대응되는 자릿수끼리의 **제곱차 합**을 구합니다.
- 각 그룹마다 합을 구하고, 최종적으로 세 값을 모두 곱한 결과를 사용합니다.
- 생체 유사도가 가장 높은 날짜를 찾되, **동률인 경우 더 이른 날짜를 선택**합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

namespace Solution {
  class Program {
    static int Biorhythm(int birth, int now) {
      int[] groupLens = { 2, 2, 4 };
      int ans = 1;

      foreach (var g in groupLens) {
        int part = 0;
        for (int i = 0; i < g; i++) {
          int bd = birth % 10;
          int nw = now % 10;
          part += (bd - nw) * (bd - nw);
          birth /= 10;
          now /= 10;
        }
        ans *= part;
      }
      return ans;
    }

    static void Main(string[] args) {
      var birth = int.Parse(Console.ReadLine()!);
      var n = int.Parse(Console.ReadLine()!);
      int maxVal = -1, minDate = int.MaxValue;

      for (int i = 0; i < n; i++) {
        int now = int.Parse(Console.ReadLine()!);
        int score = Biorhythm(birth, now);

        if (score > maxVal || (score == maxVal && now < minDate)) {
          maxVal = score;
          minDate = now;
        }
      }

      Console.WriteLine(minDate);
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

int biorhythm(int birthday, int now) {
  int ans = 1;
  int groupsDigits[] = {2, 2, 4};

  for (int g : groupsDigits) {
    int tmp = 0;
    for (int i = 0; i < g; i++) {
      tmp += (birthday % 10 - now % 10) * (birthday % 10 - now % 10);
      birthday /= 10;
      now /= 10;
    }
    ans *= tmp;
  }

  return ans;
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int birthday, n, now, maxVal = -1, minDate = 2e9;
  cin >> birthday >> n;

  while (n--) {
    cin >> now;
    int val = biorhythm(birthday, now);
    if (val > maxVal || (val == maxVal && now < minDate)) {
      maxVal = val;
      minDate = now;
    }
  }

  cout << minDate << "\n";

  return 0;
}
```
