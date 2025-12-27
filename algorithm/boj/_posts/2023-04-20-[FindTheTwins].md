---
layout: single
title: "[백준 25932] Find the Twins (C#, C++) - soo:bak"
date: "2023-04-20 15:53:00 +0900"
description: 구현과 탐색을 주제로 하는 백준 25932번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 25932
  - C#
  - C++
  - 알고리즘
keywords: "백준 25932, 백준 25932번, BOJ 25932, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [25932번 - Find the Twins](https://www.acmicpc.net/problem/25932)

## 설명
간단한 구현 문제입니다. <br>

문제의 목표는 `Dr.Orooji` 의 쌍둥이 `Zack` 과 `Mack` 이 주어진 축구 선수들의 리스트에 있는지 확인하는 것입니다. <br>

`Zack` 은 `17` 번, `Mack` 은 `18` 번 유니폼을 입고 있으므로, <br>

입력으로 주어지는 축구 선수들의 유니폼 번호 리스트에서 해당 번호의 유무를 탐색합니다. <br>

탐색 완료 후, 문제의 출력 조건에 따라 결과를 적절히 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      for (int i = 0; i < n; i++) {
        var uniformNums = new List<int>(10);
        var input = Console.ReadLine()?.Split(' ');
        for (int j = 0; j < 10; j++)
          uniformNums.Add(int.Parse(input![j]));

        bool isZackFound = false, isMackFound = false;
        for (int j = 0; j < 10; j++) {
          Console.Write($"{uniformNums[j]} ");
          if (uniformNums[j] == 17) isZackFound = true;
          if (uniformNums[j] == 18) isMackFound = true;
        }
        Console.WriteLine();

        if (isZackFound && isMackFound) Console.WriteLine("both");
        else if (isZackFound) Console.WriteLine("zack");
        else if (isMackFound) Console.WriteLine("mack");
        else Console.WriteLine("none");

        if (i != n - 1) Console.WriteLine();
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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  for (int i = 0; i < n; i++) {
    vector<int> uniformNums(10);
    for (int j = 0; j < 10; j++)
      cin >> uniformNums[j];

    bool isZackFound = false, isMackFound = false;
    for (int j = 0; j < 10; j++) {
      cout << uniformNums[j] << " ";
      if (uniformNums[j] == 17) isZackFound = true;
      if (uniformNums[j] == 18) isMackFound = true;
    }
    cout << "\n";

    if (isZackFound && isMackFound) cout << "both\n";
    else if (isZackFound) cout << "zack\n";
    else if (isMackFound) cout << "mack\n";
    else cout << "none\n";

    if (i != n - 1) cout << "\n";
  }

  return 0;
}
  ```
