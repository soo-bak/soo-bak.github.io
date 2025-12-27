---
layout: single
title: "[백준 10570] Favorite Number (C#, C++) - soo:bak"
date: "2025-04-22 22:23:00 +0900"
description: 여러 숫자 중에서 가장 많이 등장한 수를 찾고, 동률일 경우 더 작은 수를 출력하는 백준 10570번 Favorite Number 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10570
  - C#
  - C++
  - 알고리즘
keywords: "백준 10570, 백준 10570번, BOJ 10570, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10570번 - Favorite Number](https://www.acmicpc.net/problem/10570)

## 설명
여러 개의 정수가 주어졌을 때, **가장 많이 등장한 수를 찾고**, 동률이 있을 경우에는 **더 작은 수를 출력**하는 문제입니다.<br><br>

여러 개의 테스트케이스가 주어지며, 각 테스트케이스는 정수의 개수 `m`과 `m`개의 정수로 이루어져 있습니다.<br>
<br>
각 정수는 문자열로 입력되며, 이를 정수로 변환하여 처리합니다.<br><br>

출력은 테스트케이스마다 한 줄씩, **가장 많이 등장한 수(빈도수 최대값 중 최솟값)**를 출력합니다.

## 접근법
- 문자열로 주어진 숫자를 키로 하여 등장 횟수를 딕셔너리에 저장합니다.
- 모든 숫자를 다 센 후, 등장 횟수가 가장 많은 값을 구하고,
- 그 등장 횟수와 같은 숫자들 중 **가장 작은 값**을 출력합니다.

숫자의 개수가 많아도 딕셔너리 탐색과 정렬 정도의 연산을 활용함으로 충분히 빠르게 처리할 수 있습니다.

## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      int m = int.Parse(Console.ReadLine());
      var freq = new Dictionary<string, int>();

      for (int i = 0; i < m; i++) {
        string s = Console.ReadLine();
        if (!freq.ContainsKey(s))
          freq[s] = 0;
        freq[s]++;
      }

      int max = freq.Values.Max();
      var candidates = freq.Where(p => p.Value == max)
        .Select(p => int.Parse(p.Key))
        .OrderBy(x => x)
        .ToList();

      Console.WriteLine(candidates[0]);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<int> vi;
typedef map<string, int> msi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int m; cin >> m;

    msi freq;
    while (m--) {
      string s; cin >> s;
      freq[s]++;
    }

    int max_freq = 0;
    for (auto& p : freq)
      max_freq = max(max_freq, p.second);

    vi ans;
    for (auto& p : freq) {
      if (p.second == max_freq)
        ans.push_back(stoi(p.first));
    }

    sort(ans.begin(), ans.end());

    cout << ans[0] << "\n";
  }

  return 0;
}
```
