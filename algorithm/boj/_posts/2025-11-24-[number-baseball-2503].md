---
layout: single
title: "[백준 2503] 숫자 야구 (C#, C++) - soo:bak"
date: "2025-11-24 23:35:00 +0900"
description: 1~9 서로 다른 세 자리 후보를 모두 완전 탐색하며 스트라이크·볼 조건을 통과하는 개수를 세는 백준 2503번 숫자 야구 문제의 C# 및 C++ 풀이
tags:
  - 백준
  - BOJ
  - 2503
  - C#
  - C++
  - 알고리즘
keywords: "백준 2503, 백준 2503번, BOJ 2503, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2503번 - 숫자 야구](https://www.acmicpc.net/problem/2503)

## 설명

1부터 9까지의 서로 다른 세 숫자로 이루어진 세 자리 수를 맞추는 숫자 야구 게임이 있습니다.

여러 번의 질문과 각 질문에 대한 스트라이크 및 볼 개수가 주어질 때, 모든 조건을 만족하는 가능한 답의 개수를 구하는 문제입니다.

스트라이크는 숫자와 위치가 모두 일치하는 경우이고, 볼은 숫자만 일치하고 위치가 다른 경우입니다.

<br>

## 접근법

가능한 모든 세 자리 수 후보를 완전 탐색합니다.

후보는 123부터 987까지이며, 각 자리수가 모두 달라야 하고 0을 포함하지 않아야 합니다.

이러한 조건을 만족하는 후보는 최대 504개(9×8×7)이므로 모두 확인해도 시간 제약 내에 충분합니다.

<br>
각 후보에 대해 주어진 모든 질문을 검증합니다.

후보와 질문 숫자를 비교하여, 같은 위치에 같은 숫자가 있으면 스트라이크를 증가시키고, 다른 위치에 같은 숫자가 있으면 볼을 증가시킵니다.

예를 들어, 후보가 123이고 질문이 132일 때, 1은 같은 위치(스트라이크 1개), 2와 3은 다른 위치(볼 2개)이므로 스트라이크 1, 볼 2입니다.

<br>
계산된 스트라이크와 볼 개수가 질문의 결과와 일치하지 않으면 해당 후보를 제외합니다.

모든 질문을 통과한 후보의 개수를 세어 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static (int s, int b) CountSB(string cand, string guess) {
      var s = 0;
      var b = 0;

      for (var i = 0; i < 3; i++) {
        for (var j = 0; j < 3; j++) {
          if (cand[i] != guess[j]) continue;

          if (i == j) s++;
          else b++;
        }
      }

      return (s, b);
    }

    static bool ValidDigits(int n) {
      var a = n / 100;
      var b = (n / 10) % 10;
      var c = n % 10;

      if (a == 0 || b == 0 || c == 0) return false;

      return a != b && a != c && b != c;
    }

    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var queries = new (string num, int s, int b)[n];

      for (var i = 0; i < n; i++) {
        var parts = Console.ReadLine()!.Split();
        queries[i] = (parts[0], int.Parse(parts[1]), int.Parse(parts[2]));
      }

      var answer = 0;

      for (var cand = 123; cand <= 987; cand++) {
        if (!ValidDigits(cand)) continue;

        var candStr = cand.ToString();
        var ok = true;

        foreach (var q in queries) {
          var (s, b) = CountSB(candStr, q.num);

          if (s != q.s || b != q.b) {
            ok = false;
            break;
          }
        }

        if (ok) answer++;
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

pair<int, int> countSB(const string& cand, const string& guess) {
  int s = 0, b = 0;

  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      if (cand[i] != guess[j]) continue;

      if (i == j) ++s;
      else ++b;
    }
  }

  return {s, b};
}

bool validDigits(int n) {
  int a = n / 100, b = (n / 10) % 10, c = n % 10;

  if (a == 0 || b == 0 || c == 0) return false;

  return a != b && a != c && b != c;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vector<tuple<string, int, int>> queries(n);

  for (int i = 0; i < n; i++) {
    string num; int s, b;
    cin >> num >> s >> b;
    queries[i] = {num, s, b};
  }

  int answer = 0;

  for (int cand = 123; cand <= 987; cand++) {
    if (!validDigits(cand)) continue;

    string candStr = to_string(cand);
    bool ok = true;

    for (auto [num, sNeed, bNeed] : queries) {
      auto [s, b] = countSB(candStr, num);

      if (s != sNeed || b != bNeed) {
        ok = false;
        break;
      }
    }

    if (ok) ++answer;
  }

  cout << answer << "\n";

  return 0;
}
```

