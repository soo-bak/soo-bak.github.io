---
layout: single
title: "[백준 28014] 첨탑 밀어서 부수기 (C#, C++) - soo:bak"
date: "2023-05-08 22:16:00 +0900"
description: 수학과 시뮬레이션을 주제로 하는 백준 28014번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [28014번 - 첨탑 밀어서 부수기](https://www.acmicpc.net/problem/28014)

## 설명
일직선상에 놓인 첨탑을 밀어 넘어뜨리기 위해 몇 번 밀어야 하는지 계산하는 문제입니다. <br>

첨탑의 높이가 다음 첩탑의 높이보다 높을 때만 그 다음 첨탑도 넘어집니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var input = Console.ReadLine()!.Split(' ');
      var lst = new List<int>();
      for (int i = 0; i < n; i++)
        lst.Add(int.Parse(input![i]));

      int cntPush = 0;
      for (int i = 0; i < n; i++) {
        while (i < n - 1 && lst[i] > lst[i + 1])
          i++;
        cntPush++;
      }

      Console.WriteLine(cntPush);

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

  vector<int> v(n);
  for (int i = 0; i < n; i++)
    cin >> v[i];

  int cntPush = 0;
  for (int i = 0; i < n; i++) {
    while (i < n - 1 && v[i] > v[i + 1])
      i++;
    cntPush++;
  }

  cout << cntPush << "\n";

  return 0;
}
  ```
