---
layout: single
title: "[백준 5157] Bailout Bonus (C#, C++) - soo:bak"
date: "2023-05-28 07:03:00 +0900"
description: 수학과 게산을 주제로 하는 백준 5157번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [5157번 - Bailout Bonus](https://www.acmicpc.net/problem/5157)

## 설명
구제금액을 받은 기업들 중 각 임원이 받은 보너스에 대한 세금을 계산하여, 정부가 회수할 수 있는 총 금액을 계산하는 문제입니다. <br>

따라서, `구제금액을 받은 회사인지에 대한 판별` 과 `각 임원들이 속한 회사가 구제금액을 받은 회사인지에 대한 판별` 을 해야 합니다. <br>

만약, 어떠한 임원이 속한 회사가 구제금액을 받은 회사라면, 그 임원의 보너스에 문제에서 제시한 세율을 적용하여 세금을 계산합니다. <br>

이후 각 `Data Set` 마다 계산된 세금 총액을 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var cntDataSets = int.Parse(Console.ReadLine()!);
      for (int i = 1; i <= cntDataSets; i++) {
        var input = Console.ReadLine()!.Split(' ');
        var cntComp = int.Parse(input[0]);
        var cntBailedOut = int.Parse(input[1]);
        var cntExecutive = int.Parse(input[2]);
        var taxRate = int.Parse(input[3]);

        HashSet<int> bailedOutComp = new HashSet<int>();
        input = Console.ReadLine()!.Split(' ');
        for (int j = 0; j < cntBailedOut; j++) {
          var idxComp = int.Parse(input[j]);
          bailedOutComp.Add(idxComp);
        }

        long totalTax = 0;
        for (int j = 0; j < cntExecutive; j++) {
          input = Console.ReadLine()!.Split();
          var idxComp = int.Parse(input[0]);
          var bonus = int.Parse(input[1]);

          if (bailedOutComp.Contains(idxComp))
            totalTax += (long)bonus * taxRate / 100;
        }

        Console.WriteLine($"Data Set {i}:");
        Console.WriteLine(totalTax);
        if (i != cntDataSets) Console.WriteLine();
      }

    }
  }
}
  ```
<br><br>
<b>[ C++ ] </b>
<br>

  ```c++
#include <bits/stdc++.h>

using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntDataSets; cin >> cntDataSets;
  for (int i = 1; i <= cntDataSets; i++) {
    int cntComp, cntBailedOut, cntExecutive, taxRate;
    cin >> cntComp >> cntBailedOut>> cntExecutive >> taxRate;

    set<int> baildOutComp;
    for (int i = 0; i < cntBailedOut; i++) {
      int idxComp; cin >> idxComp;
      baildOutComp.insert(idxComp);
    }

    ll totalTax = 0;
    for (int i = 0; i < cntExecutive; i++) {
      int idxComp, bonus; cin >> idxComp >> bonus;

      if (baildOutComp.find(idxComp) != baildOutComp.end())
        totalTax += (ll)(bonus) * taxRate / 100;
    }

    cout << "Data Set " << i << ":\n";
    cout << totalTax << "\n";
    if (i != cntBailedOut) cout << "\n";
  }

  return 0;
}
  ```
