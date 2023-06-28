---
layout: single
title: "[백준 17588] Missing Numbers (C#, C++) - soo:bak"
date: "2023-06-29 07:50:00 +0900"
description: 탐색, 비교 등을 주제로 하는 백준 17588번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [17588번 - Missing Numbers](https://www.acmicpc.net/problem/17588)

## 설명
임의의 `n` 이라는 숫자가 주어졌을 때, 학생이 `1` 부터 `n` 까지 모든 숫자를 다 말했는지 판별하는 문제입니다. <br>

만약, 누락된 숫자들이 있다면 누락된 숫자들을 출력하고, 모든 숫자를 말했다면 `"good job"`을 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var nums = new int[n];
      for (int i = 0; i < n; i++)
        nums[i] = int.Parse(Console.ReadLine()!);

      bool isAllCounted = true;
      int cur = 1;
      for (int i = 0; i < n; i++) {
        while (cur < nums[i]) {
          Console.WriteLine(cur);
          cur++;
          isAllCounted = false;
        }
        cur++;
      }

      if (isAllCounted) Console.WriteLine("good job");

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

  vector<int> nums(n);
  for (int i = 0; i < n; i++)
    cin >> nums[i];

  bool isAllCounted = true;
  int cur = 1;
  for (int i = 0; i < n; i++) {
    while (cur < nums[i]) {
      cout << cur << "\n";
      cur++;
      isAllCounted = false;
    }
    cur++;
  }

  if (isAllCounted) cout << "good job\n";

  return 0;
}
  ```
