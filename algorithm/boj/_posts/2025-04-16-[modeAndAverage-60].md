---
layout: single
title: "[백준 2592] 대표값 (C#, C++) - soo:bak"
date: "2025-04-16 02:12:00 +0900"
description: 10개의 정수에 대해 평균과 최빈값을 구하는 백준 2592번 대표값 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2592
  - C#
  - C++
  - 알고리즘
keywords: "백준 2592, 백준 2592번, BOJ 2592, modeAndAverage, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2592번 - 대표값](https://www.acmicpc.net/problem/2592)

## 설명
**10개의 정수에 대해 평균과 최빈값을 구하는 간단한 통계 문제**입니다.<br>
<br>

- 총 `10`개의 자연수가 주어집니다.<br>
- 이 수들의 **평균(소수점 버림)**과 **최빈값**(가장 자주 등장한 수)을 구해 출력해야 합니다.<br>
- 주어지는 수들은 모두 `0` 이상 `100` 이하입니다.<br>

### 접근법
- 먼저 `10`개의 수를 입력받으며 누적합과 동시에 각 수의 빈도수를 배열에 기록합니다.<br>
- 평균은 총합을 `10`으로 나눈 몫입니다.<br>
- 최빈값은 빈도수가 가장 큰 수를 찾아 출력합니다.<br>
- 여러 수가 동일한 빈도일 경우, **입력 순서상 먼저 등장한 값**을 기준으로 처리되도록 구현합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    int[] freq = new int[101];
    int sum = 0;

    for (int i = 0; i < 10; i++) {
      int num = int.Parse(Console.ReadLine());
      sum += num;
      freq[num / 10]++;
    }

    int maxFreq = 0, mode = 0;
    for (int i = 0; i < freq.Length; i++) {
      if (freq[i] > maxFreq) {
        maxFreq = freq[i];
        mode = i * 10;
      }
    }

    Console.WriteLine(sum / 10);
    Console.WriteLine(mode);
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

  int sieve[101] = {0, };
  int sum = 0;
  for (int i = 0; i < 10; i++) {
    int num; cin >> num;
    sum += num;
    sieve[num / 10]++;
  }

  int maxF = 0, ans;
  for (int i = 0; i < 101; i++) {
    if (maxF < sieve[i]) {
      maxF = sieve[i];
      ans = i * 10;
    }
  }

  cout << sum / 10 << "\n" << ans << "\n";

  return 0;
}
```
