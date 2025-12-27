---
layout: single
title: "[백준 9550] 아이들은 사탕을 좋아해 (C#, C++) - soo:bak"
date: "2025-04-21 00:21:00 +0900"
description: 사탕 묶음 수량과 최소 기준 수를 기준으로 몇 명에게 나누어 줄 수 있는지 계산하는 백준 9550번 아이들은 사탕을 좋아해 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9550
  - C#
  - C++
  - 알고리즘
keywords: "백준 9550, 백준 9550번, BOJ 9550, kidsLoveCandy, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9550번 - 아이들은 사탕을 좋아해](https://www.acmicpc.net/problem/9550)

## 설명
**각 아이에게 한 종류의 사탕을 최소 K개 이상 줘야 할 때, 최대 몇 명의 아이를 초대할 수 있는지를 구하는 문제입니다.**<br>
<br>

- 각 테스트케이스마다 다음과 같은 정보가 주어집니다:
  - 사탕의 종류 수 `N`
  - 아이 한 명에게 주기 위한 최소 사탕 개수 `K`
  - 각 종류별 사탕 보유 개수

- 아이는 반드시 한 종류의 사탕만 먹으며, 그 사탕을 최소 `K`개 이상 받아야 만족합니다.
- 한 종류의 사탕을 여러 명에게 나누어줄 수는 있지만,<br>
  **각 아이는 반드시** `K`**개를 받아야 하므로 부족한 사탕은 쓸 수 없습니다.**
- 따라서 **각 종류별 사탕 수를** `K`**로 나눈 몫만큼만 유효하게 사용할 수 있으며**,<br>
  나머지 사탕은 버려도 무방합니다.
  - 예를 들어, 사탕이 `17`개이고 `K`가 `5`이면, `5`개씩 `3`명에게만 줄 수 있고 `2`개는 쓸 수 없습니다.
- 위 조건들을 고려하여 참석 가능한 최대 인원을 출력합니다.


## 접근법

- 먼저 테스트케이스 수를 입력받습니다.
- 각 테스트케이스마다:
  - `전체 사탕 종류 개수`와 `한 명에게 필요한 최소 사탕 개수`를 입력받습니다.
  - 이후, 각 종류별 사탕 수를 순회하면서, `사탕 수 / 최소 개수`를 계산하여 총합을 누적합니다.
  - 이때, 각 종류의 사탕 수를 `K`로 나눈 몫만큼만 아이에게 나눠줄 수 있으므로,<br>
    나머지는 사용할 수 없으며 무시하여도 됩니다.
  - 모든 사탕 종류에 대해, 나눠줄 수 있는 사탕 개수를 합산하여 참석 가능한 최대 인원 수를 계산합니다.

- 반복문 내에서 단순한 정수 나눗셈만 이루어지므로 시간 복잡도는 `O(n)`입니다.

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var config = Console.ReadLine().Split().Select(int.Parse).ToArray();
      int kind = config[0], min = config[1];
      var candies = Console.ReadLine().Split().Select(int.Parse).ToArray();

      int total = candies.Sum(c => c / min);
      Console.WriteLine(total);
    }
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
  while (t--) {
    int kindC, minC; cin >> kindC >> minC;
    int maxC = 0;
    for (int i = 0; i < kindC; i++) {
      int cntCandy; cin >> cntCandy;
      maxC += cntCandy / minC;
    }
    cout << maxC << "\n";
  }

  return 0;
}
```
