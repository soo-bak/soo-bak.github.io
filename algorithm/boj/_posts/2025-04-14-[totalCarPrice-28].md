---
layout: single
title: "[백준 9325] 얼마? (C#, C++) - soo:bak"
date: "2025-04-14 21:10:53 +0900"
description: 자동차 기본 가격과 옵션 가격을 계산하여 최종 가격을 출력하는 백준 9325번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[9325번 - 얼마?](https://www.acmicpc.net/problem/9325)

## 설명
자동차의 **기본 가격**과 **옵션 수와 각 옵션의 수량 및 단가**가 주어졌을 때,  
최종 차량 가격을 계산하는 간단한 누적 합산 문제입니다.

---

## 접근법
- 테스트할 차량 수가 주어집니다.
- 각 차량에 대해:
  - 기본 차량 가격을 입력받고,
  - 옵션 개수를 입력받은 뒤, 각 옵션마다 수량과 단가를 입력받습니다.
  - 각 옵션 가격은 `수량 × 단가`이며, 이들의 합을 기본 가격에 더합니다.
- 차량별로 최종 가격을 출력합니다.

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
        long cost = long.Parse(Console.ReadLine()!);
        int cntOpt = int.Parse(Console.ReadLine()!);
        for (int i = 0; i < cntOpt; i++) {
          var input = Console.ReadLine()!.Split();
          int qty = int.Parse(input[0]);
          int price = int.Parse(input[1]);
          cost += qty * price;
        }
        Console.WriteLine(cost);
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
typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    ll cost, cntOpt; cin >> cost >> cntOpt;
    while (cntOpt--) {
      int nbOpt, costOpt; cin >> nbOpt >> costOpt;
      cost += nbOpt * costOpt;
    }

    cout << cost << "\n";
  }

  return 0;
}
```
