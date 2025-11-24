---
layout: single
title: "[백준 16439] 치킨치킨치킨 (C#, C++) - soo:bak"
date: "2025-11-23 04:25:00 +0900"
description: 최대 세 종류의 치킨을 선택해 각 회원이 갖는 최대 선호도의 합을 완전 탐색으로 구하는 백준 16439번 치킨치킨치킨 문제의 C# 및 C++ 풀이
---

## 문제 링크
[16439번 - 치킨치킨치킨](https://www.acmicpc.net/problem/16439)

## 설명

N명의 회원과 M종류의 치킨이 있고 각 회원별 치킨 선호도가 주어질 때,

최대 3종류의 치킨을 선택하여 모든 회원 만족도의 합을 최대로 만드는 문제입니다.

각 회원의 만족도는 선택한 치킨들 중 자신의 선호도가 가장 높은 것으로 결정되며, N과 M은 각각 30 이하입니다.

<br>

## 접근법

치킨 종류가 30 이하이므로 3종류를 고르는 모든 조합은 최대 4,060개로 완전 탐색이 가능합니다.

삼중 반복문으로 서로 다른 세 종류를 선택하며 중복 없이 진행합니다.

<br>
각 조합마다 모든 회원을 순회하며 선택된 세 치킨에 대한 각 회원의 선호도 중 최댓값을 합산합니다.

모든 조합 중 이 합이 최대인 값을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var first = Console.ReadLine()!.Split();
      var n = int.Parse(first[0]);
      var m = int.Parse(first[1]);

      var pref = new int[n][];

      for (var i = 0; i < n; i++) {
        var line = Console.ReadLine()!.Split();
        pref[i] = new int[m];
        for (var j = 0; j < m; j++) pref[i][j] = int.Parse(line[j]);
      }

      var answer = 0;

      for (var a = 0; a < m - 2; a++) {
        for (var b = a + 1; b < m - 1; b++) {
          for (var c = b + 1; c < m; c++) {
            var sum = 0;

            for (var person = 0; person < n; person++) {
              var best = pref[person][a];
              if (pref[person][b] > best) best = pref[person][b];
              if (pref[person][c] > best) best = pref[person][c];
              sum += best;
            }

            if (sum > answer) answer = sum;
          }
        }
      }

      Console.WriteLine(answer);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;
typedef vector<vi> vvi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;
  vvi pref(n, vi(m));

  for (int i = 0; i < n; i++)
    for (int j = 0; j < m; j++)
      cin >> pref[i][j];

  int answer = 0;

  for (int i = 0; i < m - 2; i++) {
    for (int j = i + 1; j < m - 1; j++) {
      for (int k = j + 1; k < m; k++) {
        int sum = 0;

        for (int p = 0; p < n; p++) {
          int best = max({pref[p][i], pref[p][j], pref[p][k]});
          sum += best;
        }

        if (sum > answer) answer = sum;
      }
    }
  }

  cout << answer << "\n";

  return 0;
}
```

