---
layout: single
title: "[백준 10984] 내 학점을 구해줘 (C#, C++) - soo:bak"
date: "2025-04-14 21:07:53 +0900"
description: 이수 학점과 성적에 따라 총 학점과 평점을 계산하는 백준 10984번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 10984
  - C#
  - C++
  - 알고리즘
keywords: "백준 10984, 백준 10984번, BOJ 10984, gradeCalculator, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10984번 - 내 학점을 구해줘](https://www.acmicpc.net/problem/10984)

## 설명
**여러 과목의 학점과 성적**이 주어졌을 때,  <br>

그 학기의 **총 이수 학점**과 **평점(GPA)**을 계산하는 문제입니다.

---

## 접근법
- 먼저 테스트할 학기 수가 주어집니다.
- 각 학기에 대해:
  - 수강한 과목의 개수를 입력받습니다.
  - 이후 과목 수만큼 반복하면서 각 과목의 `학점`과 `성적(평점)`을 입력받습니다.
  - 학점의 총합과, `학점 × 평점`의 누적 합계를 계산합니다.
- 모든 과목 정보를 다 받은 후에는:
  - 평균 평점은 누적된 `(학점 × 평점)`의 총합을 **총 학점으로 나눈 값**입니다.
- 결과는 학기의 총 이수 학점과 평균 평점을 소수점 1자리까지 출력합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      int t = int.Parse(Console.ReadLine()!);
      while (t-- > 0) {
        int cntC = int.Parse(Console.ReadLine()!);
        int sumCredit = 0;
        double sumScore = 0;

        for (int i = 0; i < cntC; i++) {
          var input = Console.ReadLine()!.Split();
          int credit = int.Parse(input[0]);
          double score = double.Parse(input[1]);
          sumCredit += credit;
          sumScore += credit * score;
        }

        Console.WriteLine($"{sumCredit} {sumScore / sumCredit:F1}");
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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int cntC; cin >> cntC;

    double sumScore = 0; int sumCredit = 0;
    for (int i = 0; i < cntC; i++) {
      int credit; double score; cin >> credit >> score;
      sumCredit += credit;
      sumScore += credit * score;
    }

    cout.setf(ios::fixed); cout.precision(1);
    cout << sumCredit << " " << sumScore / sumCredit << "\n";
  }

  return 0;
}
```
