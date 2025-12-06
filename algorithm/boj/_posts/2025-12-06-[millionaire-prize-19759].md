---
layout: single
title: "[백준 19759] <<Кто хочет стать миллионером?>> (C#, C++) - soo:bak"
date: "2025-12-06 17:52:00 +0900"
description: 상금 규칙에 따라 n개의 상금을 계산하는 백준 19759번 백만장자 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[19759번 - <<Кто хочет стать миллионером?>>](https://www.acmicpc.net/problem/19759)

## 설명
첫 번째 상금은 100입니다. 다음 상금은 이전 상금의 2배 이상이면서, 뒤에 붙은 0의 개수가 전체 자릿수의 절반 이상인 가장 작은 수입니다.

n개의 상금을 순서대로 출력하는 문제입니다.

<br>

## 접근법
먼저, 뒤에 0이 t개 붙은 수는 앞부분 × 10^t 형태입니다. 조건을 만족하려면 앞부분의 자릿수가 t 이하여야 합니다.

다음으로, 이전 상금의 2배 이상인 최소 수를 찾기 위해 t를 1부터 18까지 순회합니다. 각 t에 대해 앞부분을 계산하고, 자릿수 조건을 만족하면 후보로 저장합니다.

이후, 모든 후보 중 가장 작은 값을 다음 상금으로 선택합니다. 이 과정을 n번 반복하여 출력합니다.

<br>

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static int Digits(long x) {
      var cnt = 0;
      while (x > 0) {
        cnt++;
        x /= 10;
      }
      return cnt == 0 ? 1 : cnt;
    }

    static long NextPrize(long v) {
      var best = long.MaxValue;
      var pow = 1L;
      for (var t = 1; t <= 18; t++) {
        pow *= 10;
        var p = (v + pow - 1) / pow;
        if (Digits(p) <= t) {
          var cand = p * pow;
          if (cand < best) best = cand;
        }
      }
      return best;
    }

    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var cur = 100L;
      for (var i = 1; i <= n; i++) {
        Console.WriteLine(cur);
        if (i == n) break;
        cur = NextPrize(cur * 2);
      }
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int digits(ll x) {
  int cnt = 0;
  while (x > 0) {
    cnt++;
    x /= 10;
  }
  return cnt == 0 ? 1 : cnt;
}

ll nextPrize(ll v) {
  ll best = LLONG_MAX;
  ll pw = 1;
  for (int t = 1; t <= 18; t++) {
    pw *= 10;
    ll p = (v + pw - 1) / pw;
    if (digits(p) <= t) {
      ll cand = p * pw;
      best = min(best, cand);
    }
  }
  return best;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  ll cur = 100;
  for (int i = 1; i <= n; i++) {
    cout << cur << "\n";
    if (i == n) break;
    cur = nextPrize(cur * 2);
  }

  return 0;
}
```
