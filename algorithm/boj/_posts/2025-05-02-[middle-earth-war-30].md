---
layout: single
title: "[백준 4435] 중간계 전쟁 (C#, C++) - soo:bak"
date: "2025-05-02 20:10:11 +0900"
description: 각 종족의 가중치를 반영한 총합을 비교하여 승패를 판단하는 시뮬레이션 문제 백준 4435번 중간계 전쟁 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 4435
  - C#
  - C++
  - 알고리즘
keywords: "백준 4435, 백준 4435번, BOJ 4435, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4435번 - 중간계 전쟁](https://www.acmicpc.net/problem/4435)

## 설명
각 종족의 수가 주어졌을 때, 고정된 전투력 점수를 기준으로 양 진영의 총 전투력을 계산한 뒤,

그 결과에 따라 전투의 승패를 판별하여 출력하는 문제입니다.

<br>

## 접근법

각 진영의 종족별 전투력 점수는 문제에서 고정되어 주어지므로, 이를 미리 배열에 저장해 둡니다.

그 후, 입력으로 주어지는 종족 수를 차례대로 입력받아 해당 종족의 점수와 곱해가며 두 진영의 총 전투력을 각각 계산합니다.

계산이 끝나면 두 진영의 총합을 비교하여 다음 조건에 따라 전투 결과를 판별하여 알맞은 문장을 출력합니다:
- 간달프 진영의 점수가 더 크면 `"Good triumphs over Evil"`
- 사우론 진영의 점수가 더 크면 `"Evil eradicates all trace of Good"`
- 두 진영의 점수가 같다면 `"No victor on this battle field"`

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var powerG = new[] {1, 2, 3, 3, 4, 10};
    var powerS = new[] {1, 2, 2, 2, 3, 5, 10};

    int t = int.Parse(Console.ReadLine());
    for (int b = 1; b <= t; b++) {
      var g = Console.ReadLine().Split().Select(int.Parse).ToArray();
      var s = Console.ReadLine().Split().Select(int.Parse).ToArray();

      long sumG = 0, sumS = 0;
      for (int i = 0; i < g.Length; i++) sumG += g[i] * powerG[i];
      for (int i = 0; i < s.Length; i++) sumS += s[i] * powerS[i];

      Console.Write($"Battle {b}: ");
      if (sumG > sumS) Console.WriteLine("Good triumphs over Evil");
      else if (sumG < sumS) Console.WriteLine("Evil eradicates all trace of Good");
      else Console.WriteLine("No victor on this battle field");
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

  vi powerG = {1, 2, 3, 3, 4, 10};
  vi powerS = {1, 2, 2, 2, 3, 5, 10};

  int t; cin >> t;
  for (int b = 1; b <= t; ++b) {
    ll sumG = 0, sumS = 0;

    for (int i = 0; i < 6; ++i) {
      ll numCorp; cin >> numCorp;
      sumG += numCorp * powerG[i];
    }

    for (int i = 0; i < 7; ++i) {
      ll numCorp; cin >> numCorp;
      sumS += numCorp * powerS[i];
    }

    cout << "Battle " << b << ": ";
    if (sumG > sumS) cout << "Good triumphs over Evil\n";
    else if (sumG < sumS) cout << "Evil eradicates all trace of Good\n";
    else cout << "No victor on this battle field\n";
  }

  return 0;
}
```
