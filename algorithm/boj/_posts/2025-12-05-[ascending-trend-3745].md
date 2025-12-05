---
layout: single
title: "[백준 3745] 오름세 (C#, C++) - soo:bak"
date: "2025-12-05 23:27:00 +0900"
description: 여러 테스트케이스에 대해 O(N log N) LIS 길이만 계산해 가장 긴 오름세를 찾는 백준 3745번 오름세 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[3745번 - 오름세](https://www.acmicpc.net/problem/3745)

## 설명

주가 수열에서 가장 긴 오름세를 찾는 문제입니다. 이는 가장 긴 증가하는 부분 수열(LIS)의 길이를 구하는 것과 같습니다.

<br>

## 접근법

이분 탐색 기반 LIS 알고리즘을 활용하여 가장 긴 증가하는 부분 수열의 길이를 구합니다.

<br>
먼저 lis 배열을 준비합니다. lis[i]는 길이가 i+1인 증가 부분 수열 중 가장 작은 마지막 값을 저장합니다.

다음으로 각 값 x에 대해 이분 탐색으로 lis 배열에서 x 이상인 첫 위치를 찾습니다. 해당 위치에 x를 넣고, 만약 배열 끝에 추가되는 경우라면 LIS 길이를 1 증가시킵니다.

이후 모든 원소를 처리하면 최종 길이가 가장 긴 오름세가 됩니다.

<br>
시간 복잡도는 O(N log N)입니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      string? line;
      while ((line = Console.ReadLine()) != null) {
        line = line.Trim();
        if (line.Length == 0)
          continue;
        var n = int.Parse(line);

        var nums = new List<int>();
        while (nums.Count < n) {
          var parts = Console.ReadLine()!.Split(new char[] {' ', '\t'}, StringSplitOptions.RemoveEmptyEntries);
          foreach (var p in parts)
            nums.Add(int.Parse(p));
        }

        var lis = new int[n];
        var len = 0;
        for (var i = 0; i < n; i++) {
          var x = nums[i];
          var idx = Array.BinarySearch(lis, 0, len, x);
          if (idx < 0)
            idx = ~idx;
          lis[idx] = x;
          if (idx == len)
            len++;
        }
        Console.WriteLine(len);
      }
    }
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

  int n;
  while (cin >> n) {
    vi a(n);
    for (int i = 0; i < n; i++)
      cin >> a[i];

    vi lis(n);
    int len = 0;
    for (int x : a) {
      auto it = lower_bound(lis.begin(), lis.begin() + len, x);
      *it = x;
      if (it == lis.begin() + len)
        len++;
    }

    cout << len << "\n";
  }

  return 0;
}
```
