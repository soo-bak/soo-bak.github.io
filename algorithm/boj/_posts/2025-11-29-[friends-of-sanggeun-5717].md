---
layout: single
title: "[백준 5717] 상근이의 친구들 (C#, C++) - soo:bak"
date: "2025-11-29 22:00:00 +0900"
description: 여러 테스트 케이스에 대해 남자 친구 수와 여자 친구 수를 합산해 출력하는 백준 5717번 상근이의 친구들 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 5717
  - C#
  - C++
  - 알고리즘
keywords: "백준 5717, 백준 5717번, BOJ 5717, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5717번 - 상근이의 친구들](https://www.acmicpc.net/problem/5717)

## 설명

친구 정보가 여러 줄로 주어지는 상황에서, 각 줄마다 남자 친구의 수 M (0 ≤ M ≤ 5)과 여자 친구의 수 F (0 ≤ F ≤ 5)가 주어질 때, 전체 친구의 수를 출력하는 문제입니다.

입력은 0 0이 나올 때까지 계속되며, 0 0이 입력되면 프로그램을 종료합니다.

<br>

## 접근법

반복문을 사용하여 입력을 받고, 종료 조건을 확인합니다.

각 줄에서 두 수를 입력받아 합을 출력합니다. M과 F가 모두 0이면 반복을 종료합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      while (true) {
        var input = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
        var male = input[0];
        var female = input[1];
        
        if (male == 0 && female == 0) break;
        
        Console.WriteLine(male + female);
      }
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

  while (true) {
    int male, female;
    cin >> male >> female;
    
    if (male == 0 && female == 0) break;
    
    cout << male + female << "\n";
  }
  
  return 0;
}
```


