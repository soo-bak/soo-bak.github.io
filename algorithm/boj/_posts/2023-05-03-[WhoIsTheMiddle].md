---
layout: single
title: "[백준 6840] Who is in the middle? (C#, C++) - soo:bak"
date: "2023-05-03 19:11:00 +0900"
description: 배열과 정렬, 탐색을 주제로 하는 백준 6840번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 6840
  - C#
  - C++
  - 알고리즘
keywords: "백준 6840, 백준 6840번, BOJ 6840, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [6840번 - Who is in the middle?](https://www.acmicpc.net/problem/6840)

## 설명
배열의 정렬을 주제로한 기초 문제입니다. <br>

문제의 목표는 입력으로 주어지는 `3` 개의 값 중에서 중간값을 구하는 것입니다. <br>

배열의 원소가 적으므로 조건문을 직접 활용해서 중간값을 구할 수도 있지만, 편의상 표준 라이브러리의 정렬함수를 사용했습니다. <br>

입력으로 주어지는 숫자들을 정렬한 후, 중간 원소를 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var arr = new int[3];
      for (int i = 0; i < 3; i++)
        arr[i] = int.Parse(Console.ReadLine()!);

      Array.Sort(arr);
      Console.WriteLine(arr[1]);

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

  vector<int> v(3);
  for (int i = 0; i < 3; i++)
    cin >> v[i];

  sort(v.begin(), v.end());
  cout << v[1] << "\n";

  return 0;
}
  ```
