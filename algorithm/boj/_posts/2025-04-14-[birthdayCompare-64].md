---
layout: single
title: "[백준 5635] 생일 (C#, C++) - soo:bak"
date: "2025-04-14 05:59:25 +0900"
description: 생년월일 비교를 통해 가장 어린 사람과 가장 나이 많은 사람을 구하는 백준 5635번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[5635번 - 생일](https://www.acmicpc.net/problem/5635)

## 설명
이 문제는 여러 명의 이름과 생년월일이 주어졌을 때,
**가장 어린 사람**과 **가장 나이 많은 사람**의 이름을 각각 출력하는 문제입니다.

---

## 접근법
- 생년월일은 `일, 월, 년` 순으로 주어지므로, 비교를 위해 `년 → 월 → 일` 순서대로 조건을 평가합니다.
- 처음 입력된 사람을 기준으로 초기화한 뒤, 이후 사람들과 생일을 비교하여 가장 나이 많은 사람과 어린 사람을 갱신합니다.
- 조건은 날짜가 **더 크면 더 어리다**, **더 작으면 더 나이가 많다**는 기준으로 구현합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    int numS = int.Parse(Console.ReadLine()!);

    string? youngestName = null, oldestName = null;
    int youngestY = 0, youngestM = 0, youngestD = 0,
        oldestY = 0, oldestM = 0, oldestD = 0;

    for (int i = 0; i < numS; i++) {
      var input = Console.ReadLine()!.Split();
      string name = input[0];
      int d = int.Parse(input[1]),
          m = int.Parse(input[2]),
          y = int.Parse(input[3]);

      if (i == 0) {
        youngestName = oldestName = name;
        youngestY = oldestY = y;
        youngestM = oldestM = m;
        youngestD = oldestD = d;
      } else {
        if (y > youngestY || (y == youngestY && m > youngestM) ||
            (y == youngestY && m == youngestM && d > youngestD)) {
          youngestName = name;
          youngestY = y;
          youngestM = m;
          youngestD = d;
        }
        if (y < oldestY || (y == oldestY && m < oldestM) ||
            (y == oldestY && m == oldestM && d < oldestD)) {
          oldestName = name;
          oldestY = y;
          oldestM = m;
          oldestD = d;
        }
      }
    }

    Console.WriteLine($"{youngestName}\n{oldestName}");
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

  int numS; cin >> numS;

  string youngestName, oldest_name;
  int youngestY = 0, youngestM = 0, youngestD = 0;
  int oldestY = 0, oldestM = 0, oldestD = 0;

  for (int i = 0; i < numS; i++) {
    string name; int d, m, y; cin >> name >> d >> m >> y;

    if (i == 0) {
      youngestName = oldest_name = name;
      youngestY = oldestY = y;
      youngestM = oldestM = m;
      youngestD = oldestD = d;
    } else {
      if (y > youngestY || (y == youngestY && m > youngestM) ||
          (y == youngestY && m == youngestM && d > youngestD)) {
        youngestName = name;
        youngestY = y;
        youngestM = m;
        youngestD = d;
      }
      if (y < oldestY || (y == oldestY && m < oldestM) ||
          (y == oldestY && m == oldestM && d < oldestD)) {
        oldest_name = name;
        oldestY = y;
        oldestM = m;
        oldestD = d;
      }
    }
  }

  cout << youngestName << "\n" << oldest_name << "\n";

  return 0;
}
```
