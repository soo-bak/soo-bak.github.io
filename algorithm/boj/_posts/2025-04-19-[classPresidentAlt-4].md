---
layout: single
title: "[백준 2456] 나는 학급회장이다 (C#, C++) - soo:bak"
date: "2025-04-19 00:05:00 +0900"
description: 투표 점수와 점수 종류 우선순위에 따른 조건 비교를 통해 학급 회장을 판별하는 백준 2456번 나는 학급회장이다 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2456
  - C#
  - C++
  - 알고리즘
  - 구현
  - 케이스분류
keywords: "백준 2456, 백준 2456번, BOJ 2456, classPresidentAlt, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2456번 - 나는 학급회장이다](https://www.acmicpc.net/problem/2456)

## 설명
**각 후보에게 부여된 점수를 바탕으로 총합과 우선 점수 개수 비교를 통해 회장을 결정하는 구현 문제**입니다.<br>
<br>

- 각 학생은 세 명의 후보에게 각각 1, 2, 3점 중 하나를 부여합니다.<br>
- 각 후보의 총점을 계산하고, 가장 높은 총점을 받은 후보가 회장이 됩니다.<br>
- 동점일 경우 `3점`이 더 많은 후보가 우선이며,<br>
  그래도 같다면 `2점`이 더 많은 후보가 우선입니다.<br>
- 모두 같다면 **무승부**로 간주하고 `0`을 출력합니다.<br>

### 접근법
- 세 후보 각각에 대해 총점, 3점 횟수, 2점 횟수를 별도로 저장합니다.<br>
- 총점이 높은 후보를 우선 선택하고, 동점이면 3점 수, 그 다음 2점 수 순으로 우선순위를 결정합니다.<br>
- 최종 결과는 회장 번호(1~3)와 해당 총점을 출력하며, 무승부 시에는 `0`과 점수를 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    int[] total = new int[3], threes = new int[3], twos = new int[3];

    for (int i = 0; i < n; i++) {
      var line = Console.ReadLine().Split().Select(int.Parse).ToArray();
      for (int j = 0; j < 3; j++) {
        total[j] += line[j];
        if (line[j] == 3) threes[j]++;
        else if (line[j] == 2) twos[j]++;
      }
    }

    int winner = 0;
    bool isDraw = false;
    for (int i = 1; i < 3; i++) {
      if (total[i] > total[winner]) {
        winner = i;
        isDraw = false;
      } else if (total[i] == total[winner]) {
        if (threes[i] > threes[winner]) {
          winner = i;
          isDraw = false;
        } else if (threes[i] == threes[winner]) {
          if (twos[i] > twos[winner]) {
            winner = i;
            isDraw = false;
          } else if (twos[i] == twos[winner]) {
            isDraw = true;
          }
        }
      }
    }

    if (isDraw)
      Console.WriteLine($"0 {total[winner]}");
    else
      Console.WriteLine($"{winner + 1} {total[winner]}");
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  int total[3] = {0, }, threes[3] = {0, }, twos[3] = {0, };
  
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < 3; j++) {
      int score; cin >> score;
      total[j] += score;
      if (score == 3) threes[j]++;
      else if (score == 2) twos[j]++;
    }
  }
  
  int winner = 0;
  bool isDraw = false;
  for (int i = 1; i < 3; i++) {
    if (total[i] > total[winner]) {
      winner = i;
      isDraw = false;
    } else if (total[i] == total[winner]) {
      if (threes[i] > threes[winner]) {
        winner = i;
        isDraw = false;
      } else if (threes[i] == threes[winner]) {
        if (twos[i] > twos[winner]) {
          winner = i;
          isDraw = false;
        } else if (twos[i] == twos[winner])
          isDraw = true;
      }
    }
  }
  
  if (isDraw) cout << "0 " << total[winner] << "\n";
  else cout << winner + 1 << " " << total[winner] << "\n";

  return 0;
}
```
