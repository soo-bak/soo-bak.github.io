---
layout: single
title: "[백준 23348] 스트릿 코딩 파이터 (C#, C++) - soo:bak"
date: "2025-11-30 01:48:00 +0900"
description: 기술 난이도와 사용 횟수로 팀 점수를 계산해 최고 점수를 찾는 백준 23348번 스트릿 코딩 파이터 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 23348
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 23348, 백준 23348번, BOJ 23348, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23348번 - 스트릿 코딩 파이터](https://www.acmicpc.net/problem/23348)

## 설명

스트릿 코딩 파이터 대회가 열리는 상황에서, 세 가지 기술(한손 코딩, 노룩 코딩, 폰 코딩)의 난이도 A, B, C와 동아리 수 N, 그리고 각 동아리의 3명 참가자가 각 기술을 사용한 횟수가 주어질 때, 가장 높은 팀 점수를 구하는 문제입니다.

각 참가자의 점수는 (A × 한손 횟수) + (B × 노룩 횟수) + (C × 폰 횟수)로 계산되며, 팀 점수는 3명의 점수를 합한 값입니다. 동아리 수 N은 최대 100입니다.

<br>

## 접근법

각 동아리의 팀 점수를 계산하여 최댓값을 찾습니다.

먼저 세 가지 기술의 난이도를 입력받습니다. 각 동아리마다 3명의 참가자 정보를 읽어 개인 점수를 계산하고 합산하여 팀 점수를 구합니다.

모든 동아리를 순회하면서 현재까지의 최고 점수를 갱신합니다. 시간 복잡도는 O(N)입니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var difficulty = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
      var oneHand = difficulty[0];
      var noLook = difficulty[1];
      var phone = difficulty[2];

      var n = int.Parse(Console.ReadLine()!);
      var maxScore = 0;
      
      for (var i = 0; i < n; i++) {
        var teamScore = 0;
        
        for (var j = 0; j < 3; j++) {
          var participant = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
          var countOneHand = participant[0];
          var countNoLook = participant[1];
          var countPhone = participant[2];
          teamScore += oneHand * countOneHand + noLook * countNoLook + phone * countPhone;
        }
        
        maxScore = Math.Max(maxScore, teamScore);
      }
      
      Console.WriteLine(maxScore);
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

  int oneHand, noLook, phone;
  cin >> oneHand >> noLook >> phone;
  
  int n; cin >> n;
  int maxScore = 0;
  
  for (int i = 0; i < n; i++) {
    int teamScore = 0;
    
    for (int j = 0; j < 3; j++) {
      int countOneHand, countNoLook, countPhone;
      cin >> countOneHand >> countNoLook >> countPhone;
      teamScore += oneHand * countOneHand + noLook * countNoLook + phone * countPhone;
    }
    
    maxScore = max(maxScore, teamScore);
  }
  
  cout << maxScore << "\n";

  return 0;
}
```


