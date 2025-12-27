---
layout: single
title: "[백준 2587] 대표값2 (C#, C++) - soo:bak"
date: "2025-04-17 00:00:00 +0900"
description: 5개의 자연수에 대해 평균과 중앙값을 계산하는 백준 2587번 대표값2 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2587
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 정렬
  - arithmetic
keywords: "백준 2587, 백준 2587번, BOJ 2587, averageAndMedian, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2587번 - 대표값2](https://www.acmicpc.net/problem/2587)

## 설명
**다섯 개의 자연수가 주어졌을 때 평균과 중앙값을 출력하는 문제**입니다.<br>
<br>

- 주어진 수들은 모두 `100` 보다 작은 `10`의 배수입니다.<br>
- 평균은 전체 합을 `5`로 나눈 몫입니다 (소수점 버림).<br>
- 중앙값은 정렬 후 가운데 위치한 값을 의미합니다.<br>

### 접근법
- 다섯 개의 수를 입력받으며 동시에 총합을 누적합니다.<br>
- 입력된 수들을 정렬하여 중앙값을 추출합니다.<br>
- 총합의 평균(정수)과 중앙값을 차례대로 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var nums = new int[5];
    int sum = 0;

    for (int i = 0; i < 5; i++) {
      nums[i] = int.Parse(Console.ReadLine());
      sum += nums[i];
    }

    Array.Sort(nums);
    Console.WriteLine(sum / 5);
    Console.WriteLine(nums[2]);
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vi v(5);
  int sum = 0;
  for (int i = 0; i < 5; i++) {
    cin >> v[i];
    sum += v[i];
  }

  sort(v.begin(), v.end());

  cout << sum / 5 << "\n" << v[2] << "\n";

  return 0;
}
```
