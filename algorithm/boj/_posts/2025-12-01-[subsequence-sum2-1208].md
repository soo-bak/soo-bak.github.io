---
layout: single
title: "[백준 1208] 부분수열의 합 2 (C#, C++) - soo:bak"
date: "2025-12-01 19:03:00 +0900"
description: N≤40 부분수열 합을 meet-in-the-middle로 쪼개 두 집합 합을 투포인터로 세는 백준 1208번 부분수열의 합 2 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[1208번 - 부분수열의 합 2](https://www.acmicpc.net/problem/1208)

## 설명

크기 N (1 ≤ N ≤ 40)의 정수 수열과 목표값 S가 주어지는 상황에서, 합이 S가 되는 공집합이 아닌 부분수열의 개수를 구하는 문제입니다.

N이 최대 40이므로 모든 부분수열을 확인하면 2^40으로 시간 초과가 발생합니다. Meet-in-the-middle 기법을 사용하여 2^20 × 2로 줄여야 합니다.

<br>

## 접근법

Meet-in-the-middle 기법과 투 포인터를 활용하여 효율적으로 개수를 셉니다.

<br>
먼저 수열을 절반으로 나누어 앞쪽과 뒤쪽으로 분리합니다. 각 부분에서 만들 수 있는 모든 부분합을 비트마스크로 생성합니다. 이렇게 하면 각각 최대 2^20개의 부분합을 얻게 됩니다.

다음으로 앞쪽 부분합은 오름차순으로, 뒤쪽 부분합은 내림차순으로 정렬합니다. 투 포인터를 사용하여 두 부분합의 합이 S가 되는 경우를 찾습니다.

이후 동일한 값이 연속되는 구간을 카운트하여 조합의 개수를 곱셈으로 계산합니다. S가 0인 경우 공집합 조합이 포함되므로 1을 빼줍니다.

<br>
시간 복잡도는 O(2^(N/2) log 2^(N/2))입니다.

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
      var first = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
      var n = first[0];
      var target = first[1];
      var nums = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);

      var mid = n / 2;
      var leftN = n - mid;
      var rightN = mid;

      var leftSize = 1 << leftN;
      var rightSize = 1 << rightN;
      var left = new int[leftSize];
      var right = new int[rightSize];

      for (var mask = 0; mask < leftSize; mask++) {
        var sum = 0;
        for (var i = 0; i < leftN; i++)
          if ((mask & (1 << i)) != 0)
            sum += nums[i];
        left[mask] = sum;
      }

      for (var mask = 0; mask < rightSize; mask++) {
        var sum = 0;
        for (var i = 0; i < rightN; i++)
          if ((mask & (1 << i)) != 0)
            sum += nums[leftN + i];
        right[mask] = sum;
      }

      Array.Sort(left);
      Array.Sort(right, (a, b) => b.CompareTo(a));

      var ans = 0L;
      var li = 0;
      var ri = 0;
      while (li < leftSize && ri < rightSize) {
        var cur = left[li] + right[ri];
        if (cur == target) {
          var lv = left[li];
          var rv = right[ri];
          var lc = 0L;
          var rc = 0L;
          while (li < leftSize && left[li] == lv) { lc++; li++; }
          while (ri < rightSize && right[ri] == rv) { rc++; ri++; }
          ans += lc * rc;
        } else if (cur < target) li++;
        else ri++;
      }

      if (target == 0)
        ans--;

      Console.WriteLine(ans);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, S; cin >> n >> S;
  vi a(n);
  for (int i = 0; i < n; i++)
    cin >> a[i];

  int mid = n / 2;
  int leftN = n - mid, rightN = mid;
  int leftSize = 1 << leftN, rightSize = 1 << rightN;
  vi left(leftSize), right(rightSize);

  for (int mask = 0; mask < leftSize; mask++) {
    int sum = 0;
    for (int i = 0; i < leftN; i++)
      if (mask & (1 << i))
        sum += a[i];
    left[mask] = sum;
  }
  for (int mask = 0; mask < rightSize; mask++) {
    int sum = 0;
    for (int i = 0; i < rightN; i++)
      if (mask & (1 << i))
        sum += a[leftN + i];
    right[mask] = sum;
  }

  sort(left.begin(), left.end());
  sort(right.begin(), right.end(), greater<int>());

  int li = 0, ri = 0;
  ll ans = 0;
  while (li < leftSize && ri < rightSize) {
    int cur = left[li] + right[ri];
    if (cur == S) {
      int lv = left[li], rv = right[ri];
      ll lc = 0, rc = 0;
      while (li < leftSize && left[li] == lv) { lc++; li++; }
      while (ri < rightSize && right[ri] == rv) { rc++; ri++; }
      ans += lc * rc;
    } else if (cur < S) li++;
    else ri++;
  }

  if (S == 0) ans--;

  cout << ans << "\n";
  return 0;
}
```
