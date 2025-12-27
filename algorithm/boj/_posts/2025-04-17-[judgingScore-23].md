---
layout: single
title: "[백준 9076] 점수 집계 (C#, C++) - soo:bak"
date: "2025-04-17 00:23:43 +0900"
description: 심사 점수 중 최고점과 최저점을 제외하고 중간 점수의 범위를 기준으로 유효 여부를 판단하는 백준 9076번 점수 집계 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9076
  - C#
  - C++
  - 알고리즘
  - 구현
  - 정렬
keywords: "백준 9076, 백준 9076번, BOJ 9076, judgingScore, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9076번 - 점수 집계](https://www.acmicpc.net/problem/9076)

## 설명
**다섯 명의 심사위원 점수 중 최고점과 최저점을 제외한 나머지 점수의 범위를 이용하여 결과를 출력하는 문제**입니다.<br>
<br>

- 한 줄에 `5`개의 점수가 주어집니다.<br>
- 이 중 **가장 큰 점수와 가장 작은 점수**를 제외하고 **중간 점수 3개**를 기준으로 계산합니다.<br>
- 중간 점수들 중 가장 큰 값과 가장 작은 값의 차이가 `4` 이상인 경우 **부정확한 점수**로 간주하여 `"KIN"`을 출력합니다.<br>
- 그렇지 않다면 **중간 점수 3개의 합**을 출력합니다.<br>

### 접근법
- 각 테스트케이스마다 다섯 개의 점수를 입력받아 정렬합니다.<br>
- 정렬된 점수 중 첫 번째와 마지막 값을 제외한 세 개의 점수를 추출합니다.<br>
- 이 세 점수 중 가장 큰 값과 가장 작은 값의 차이를 구해 `4` 이상인지 판단합니다.<br>
- 차이가 `4` 이상이면 `"KIN"`을, 아니면 세 점수의 합을 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int testCases = int.Parse(Console.ReadLine());
    for (int t = 0; t < testCases; t++) {
      var scores = Console.ReadLine().Split().Select(int.Parse).ToArray();
      Array.Sort(scores);
      int minMid = scores[1];
      int maxMid = scores[3];

      if (maxMid - minMid >= 4) Console.WriteLine("KIN");
      else Console.WriteLine(minMid + scores[2] + maxMid);
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    vi scores(5);
    for (int i = 0; i < 5; i++)
      cin >> scores[i];

    sort(scores.begin(), scores.end());

    int midMin = scores[1], midMax = scores[3];
    if (midMax - midMin >= 4) cout << "KIN\n";
    else cout << scores[1] + scores[2] + scores[3] << "\n";
  }

  return 0;
}
```
