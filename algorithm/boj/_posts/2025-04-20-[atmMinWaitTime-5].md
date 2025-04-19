---
layout: single
title: "[백준 11399] ATM (C#, C++) - soo:bak"
date: "2025-04-20 04:21:00 +0900"
description: 사람들의 인출 시간을 오름차순으로 정렬해 전체 대기 시간의 합을 최소화하는 백준 11399번 ATM 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[11399번 - ATM](https://www.acmicpc.net/problem/11399)

## 설명
**여러 명의 사람이 ATM에서 돈을 인출할 때, 대기 시간의 총합을 최소화하기 위한 인출 순서를 구하는 문제입니다.**
<br>

- 각 사람은 ATM을 이용할 때 일정 시간이 소요되며, 앞사람이 끝날 때까지 기다려야 합니다.
- 전체 대기 시간의 총합을 최소로 만들기 위해서는 **인출 시간이 짧은 사람부터 앞에 배치**해야 합니다.
- 정렬을 기반으로 한 탐욕법(그리디 알고리듬) 접근 방식이 핵심입니다.


## 접근법

1. 전체 사람의 수와 각 사람의 인출 시간을 입력받습니다.
2. 인출 시간이 짧은 사람일수록 더 앞에 배치되도록, 전체 시간을 **오름차순으로 정렬**합니다.
3. 정렬된 순서대로 앞에서부터 누적하여 각 사람의 대기 시간을 더해갑니다.
   - 각 사람의 대기 시간은 자신 이전의 모든 사람들의 인출 시간의 합이므로 누적합으로 구할 수 있습니다.
4. 이 과정을 반복하여 최적의 전체 대기 시간을 계산합니다.

- 이 문제는 `정렬을 한 번 수행`하면 그 이후의 계산은 `O(n)`으로 가능하므로 전체 시간 복잡도는 `O(n log n)`입니다.

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int count = int.Parse(Console.ReadLine());
    var times = Console.ReadLine()
      .Split()
      .Select(int.Parse)
      .OrderBy(x => x)
      .ToArray();

    int total = 0, accum = 0;
    foreach (var t in times) {
      accum += t;
      total += accum;
    }
    Console.WriteLine(total);
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

  int cntP; cin >> cntP;
  vi time(cntP);
  for (int i = 0; i < cntP; i++)
    cin >> time[i];

  sort(time.begin(), time.end());

  int sum = 0, wating = 0;
  for (auto i : time) {
    wating += i;
    sum += wating;
  }

  cout << sum << "\n";

  return 0;
}
```
