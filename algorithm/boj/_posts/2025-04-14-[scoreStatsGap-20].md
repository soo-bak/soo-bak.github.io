---
layout: single
title: "[백준 5800] 성적 통계 (C#, C++) - soo:bak"
date: "2025-04-14 02:20:00 +0900"
description: 학생 점수 중 최댓값, 최솟값, 최대 점수 간격을 계산하는 백준 5800번 성적 통계 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 5800
  - C#
  - C++
  - 알고리즘
  - 구현
  - 정렬
keywords: "백준 5800, 백준 5800번, BOJ 5800, scoreStatsGap, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5800번 - 성적 통계](https://www.acmicpc.net/problem/5800)

## 설명
여러 학급의 점수 데이터에 대해 **최댓값, 최솟값, 가장 큰 점수 차이**를 구하는 문제입니다.

입력은 여러 줄로 구성되며, 각 줄은 한 학급의 점수 데이터를 나타냅니다.  <br>

출력은 각 학급마다 `Class X` 라벨과 함께 **최댓값, 최솟값, 최대 점수 차이**를 순서대로 출력합니다.

---

## 접근법
- 각 테스트 케이스에서 점수를 벡터에 저장한 뒤 오름차순 정렬합니다.
- 정렬된 리스트에서:
  - 최댓값은 마지막 원소
  - 최솟값은 첫 번째 원소
  - 최대 점수 간격은 인접한 원소 간의 차이 중 최대값
- 각 학급에 대해 라벨링된 출력 포맷을 그대로 맞춰 출력합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      int numClass = int.Parse(Console.ReadLine()!);
      for (int classNum = 1; classNum <= numClass; classNum++) {
        var scores = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
        int numS = scores[0];

        var arr = scores.Skip(1).ToArray();
        Array.Sort(arr);

        int maxGap = 0;
        for (int i = 1; i < numS; i++)
          maxGap = Math.Max(maxGap, arr[i] - arr[i - 1]);

        Console.WriteLine("Class " + classNum);
        Console.WriteLine($"Max {arr[numS - 1]}, Min {arr[0]}, Largest gap {maxGap}");
      }
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

  int numClass; cin >> numClass;
  int cntClass = 1;
  while (numClass--) {
    int numS; cin >> numS;

    vi score(numS);
    for (int i = 0; i < numS; i++)
      cin >> score[i];

    sort(score.begin(), score.end());

    int maxGap = 0;
    for (int i = 0; i < numS - 1; i++) {
      int gap = score[i + 1] - score[i];
      if (gap > maxGap) maxGap = gap;
    }
    cout << "Class " << cntClass << "\n";
    cout << "Max " << score[numS - 1];
    cout << ", Min " << score[0];
    cout << ", Largest gap " << maxGap << "\n";
    cntClass++;
  }

  return 0;
}
```
