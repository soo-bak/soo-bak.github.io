---
layout: single
title: "[백준 14697] 방 배정하기 (C#, C++) - soo:bak"
date: "2025-12-09 12:45:00 +0900"
description: 세 방 크기 조합을 완전탐색해 학생 수와 정확히 일치하는지 확인하는 백준 14697번 방 배정하기 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 14697
  - C#
  - C++
  - 알고리즘
  - 브루트포스
keywords: "백준 14697, 백준 14697번, BOJ 14697, RoomAssignment, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14697번 - 방 배정하기](https://www.acmicpc.net/problem/14697)

## 설명
방 정원 A, B, C가 주어질 때, 이 방들을 원하는 개수만큼 사용해 빈 침대 없이 정확히 N명을 배정할 수 있는지 묻습니다. 세 종류 중 일부만 써도 됩니다.

<br>

## 접근법
N이 300 이하이므로 완전탐색으로 충분합니다.

각 방 종류를 몇 개씩 사용할지 삼중 반복문으로 모든 조합을 시도합니다. 세 방의 인원 합이 정확히 N이 되는 조합이 하나라도 있으면 1을, 없으면 0을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var a = int.Parse(parts[0]);
    var b = int.Parse(parts[1]);
    var c = int.Parse(parts[2]);
    var n = int.Parse(parts[3]);

    for (var i = 0; i <= n; i++) {
      for (var j = 0; j <= n; j++) {
        for (var k = 0; k <= n; k++) {
          if (a * i + b * j + c * k == n) {
            Console.WriteLine(1);
            return;
          }
        }
      }
    }

    Console.WriteLine(0);
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

  int a, b, c, n; cin >> a >> b >> c >> n;
  for (int i = 0; i <= n; i++) {
    for (int j = 0; j <= n; j++) {
      for (int k = 0; k <= n; k++) {
        if (a * i + b * j + c * k == n) {
          cout << 1 << "\n";
          return 0;
        }
      }
    }
  }

  cout << 0 << "\n";

  return 0;
}
```
