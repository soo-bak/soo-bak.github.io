---
layout: single
title: "[백준 8974] 희주의 수학시험 (C#, C++) - soo:bak"
date: "2025-05-02 19:46:00 +0900"
description: 숫자를 일정 규칙으로 나열한 수열에서 주어진 범위의 부분합을 구하는 백준 8974번 희주의 수학시험 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[8974번 - 희주의 수학시험](https://www.acmicpc.net/problem/8974)

## 설명
수열을 다음 규칙에 따라 구성합니다:

- `1`이 한 번, `2`가 두 번, `3`이 세 번, `4`가 네 번, `...` <br>
  즉, 정수 `k`는 수열에서 정확히 `k`번 연속으로 등장합니다.

이렇게 생성된 수열에서 정수 `A`, `B`가 주어졌을 때, `A`번째부터 `B`번째까지 등장하는 숫자의 합을 구하는 문제입니다.

<br>

## 접근법

- `1`부터 시작하여, 같은 숫자를 해당 숫자만큼 반복해서 수열을 미리 생성합니다.
- 수열의 최대 길이는 문제의 조건상 `1000`까지만 만들면 충분합니다.
- 이후, 주어진 범위에 해당하는 위치의 값들을 순회하며 합을 계산합니다.

<br>

## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split().Select(int.Parse).ToArray();
    int a = input[0], b = input[1];

    var seq = new List<int>();
    for (int num = 1; seq.Count < 1000; num++)
      for (int i = 0; i < num && seq.Count < 1000; i++)
        seq.Add(num);

    int sum = 0;
    for (int i = a - 1; i < b; i++)
      sum += seq[i];

    Console.WriteLine(sum);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vi seq(1000);
  int ele = 1, cnt = 0;
  for (int i = 0; i < 1000; i++) {
    seq[i] = ele;
    if (++cnt == ele) {
      cnt = 0;
      ele++;
    }
  }

  int a, b; cin >> a >> b;

  int sum = 0;
  for (int i = a - 1; i < b; i++)
    sum += seq[i];

  cout << sum << "\n";

  return 0;
}
```
