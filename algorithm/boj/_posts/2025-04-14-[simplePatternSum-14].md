---
layout: single
title: "[백준 1292] 쉽게 푸는 문제 (C#, C++) - soo:bak"
date: "2025-04-14 06:08:09 +0900"
description: 숫자 패턴을 구성하고 특정 구간 합을 구하는 백준 1292번 쉽게 푸는 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1292
  - C#
  - C++
  - 알고리즘
keywords: "백준 1292, 백준 1292번, BOJ 1292, simplePatternSum, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1292번 - 쉽게 푸는 문제](https://www.acmicpc.net/problem/1292)

## 설명
이 문제는 수열을 특정 규칙으로 생성한 후, <br>
**입력으로 주어진 구간의 합을 구하는 문제**입니다.

수열은 다음과 같은 규칙을 따릅니다:

$$
1, 2, 2, 3, 3, 3, 4, 4, 4, 4, \dots
$$

즉, `1`은 한 번, `2`는 두 번, `3`은 세 번, ... `k`는 `k`번 반복됩니다.

---

## 접근법
- 수열을 `1000`번째 숫자까지 구성해 배열에 저장합니다.
- 인덱스 `A`부터 `B`까지의 구간 합을 계산하여 출력합니다.
- 구간은 1-based index이므로, 계산 시 배열 접근을 `A-1`부터 `B-1`까지로 처리합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var parts = Console.ReadLine()!.Split();
      int a = int.Parse(parts[0]) - 1;
      int b = int.Parse(parts[1]) - 1;

      int[] arr = new int[1_000];
      int idx = 0, cnt = 1;
      while (idx < 1_000) {
        for (int i = 0; i < cnt && idx < 1_000; i++)
          arr[idx++] = cnt;
        cnt++;
      }

      long sum = 0;
      for (int i = a; i <= b; i++)
        sum += arr[i];
      Console.WriteLine(sum);
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>
#define MAX 1'000

using namespace std;
typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int arr[MAX];
  int idx = 0, cnt = 1;
  while (idx < MAX) {
    for (int i = 0; i < cnt && idx < MAX; i++)
      arr[idx++] = cnt;
    cnt++;
  }

  int a, b; cin >> a >> b;

  a--; b--;

  ll sum = 0;
  for (int i = a; i <= b; i++)
    sum += arr[i];
  cout << sum << "\n";

  return 0;
}
```
