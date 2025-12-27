---
layout: single
title: "[백준 2352] 반도체 설계 (C#, C++) - soo:bak"
date: "2025-12-03 01:03:00 +0900"
description: 연결이 꼬이지 않도록 최대 포트를 연결하는 문제를 LIS 길이 계산으로 해결하는 백준 2352번 반도체 설계 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2352
  - C#
  - C++
  - 알고리즘
  - 이분탐색
  - lis
keywords: "백준 2352, 백준 2352번, BOJ 2352, semiconductor, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2352번 - 반도체 설계](https://www.acmicpc.net/problem/2352)

## 설명

왼쪽 포트 1부터 n까지가 오른쪽 포트들과 매칭될 때, 선이 교차하지 않도록 연결할 수 있는 최대 개수를 구하는 문제입니다.

왼쪽 포트 순서를 고정하면, 오른쪽 포트 번호들의 가장 긴 증가하는 부분 수열(LIS) 길이가 곧 교차 없이 연결 가능한 최대 개수가 됩니다.

<br>

## 접근법

이분 탐색 기반 LIS 알고리즘을 활용하여 가장 긴 증가하는 부분 수열의 길이를 구합니다.

<br>
먼저 lis 배열을 준비합니다. lis[i]는 길이가 i+1인 증가 부분 수열 중 가장 작은 마지막 값을 저장합니다.

다음으로 각 값 x에 대해 이분 탐색으로 lis 배열에서 x 이상인 첫 위치를 찾습니다. 해당 위치에 x를 넣고, 만약 배열 끝에 추가되는 경우라면 LIS 길이를 1 증가시킵니다.

이후 모든 원소를 처리하면 최종 길이가 교차 없이 연결 가능한 최대 포트 개수가 됩니다.

<br>
시간 복잡도는 O(N log N)입니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var arr = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);

      var lis = new int[n];
      var len = 0;
      for (var i = 0; i < n; i++) {
        var x = arr[i];
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
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vi a(n);
  for (int i = 0; i < n; i++)
    cin >> a[i];

  vi lis(n);
  int len = 0;
  for (int i = 0; i < n; i++) {
    int x = a[i];
    auto it = lower_bound(lis.begin(), lis.begin() + len, x);
    *it = x;
    if (it == lis.begin() + len)
      len++;
  }

  cout << len << "\n";
  
  return 0;
}
```
