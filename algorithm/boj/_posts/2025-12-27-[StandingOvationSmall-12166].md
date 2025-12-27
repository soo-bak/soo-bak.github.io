---
layout: single
title: "[백준 12166] Standing Ovation (Small) (C#, C++) - soo:bak"
date: "2025-12-27 06:35:00 +0900"
description: "백준 12166번 C#, C++ 풀이 - 최소한의 친구를 초대해 관객 모두가 기립박수하도록 만드는 문제"
tags:
  - 백준
  - BOJ
  - 12166
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 12166, 백준 12166번, BOJ 12166, StandingOvationSmall, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[12166번 - Standing Ovation (Small)](https://www.acmicpc.net/problem/12166)

## 설명
시작 시 모두 앉아 있고, 각 관객은 부끄러움 수치 k 이상 사람이 서 있으면 일어납니다. 필요한 경우 친구를 초대해 관객 모두가 일어서게 만들 때, 최소 초대 인원을 구하는 문제입니다.

입력은 여러 테스트 케이스로 주어지며, 각 케이스마다 최대 부끄러움 Smax와 각 수치별 인원 문자열이 주어집니다.

<br>

## 접근법
왼쪽부터 부끄러움 수치를 순회하며 현재까지 서 있는 사람 수(초대한 친구 포함)가 수치보다 작으면 부족분만큼 친구를 초대합니다.

이후 해당 수치의 관객 수를 더하며 진행하고, 누적 초대 인원의 최솟값을 답으로 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split((char[])null, StringSplitOptions.RemoveEmptyEntries);
    var idx = 0;
    var t = int.Parse(parts[idx++]);
    var sb = new StringBuilder();

    for (var cs = 1; cs <= t; cs++) {
      var smax = int.Parse(parts[idx++]);
      var s = parts[idx++];

      var standing = 0;
      var added = 0;
      for (var i = 0; i <= smax; i++) {
        var cnt = s[i] - '0';
        if (standing < i) {
          var need = i - standing;
          added += need;
          standing += need;
        }
        standing += cnt;
      }

      sb.AppendLine($"Case #{cs}: {added}");
    }

    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  for (int cs = 1; cs <= t; cs++) {
    int smax; string s;
    cin >> smax >> s;

    int standing = 0, added = 0;
    for (int i = 0; i <= smax; i++) {
      int cnt = s[i] - '0';
      if (standing < i) {
        int need = i - standing;
        added += need;
        standing += need;
      }
      standing += cnt;
    }

    cout << "Case #" << cs << ": " << added << "\n";
  }
  return 0;
}
```
