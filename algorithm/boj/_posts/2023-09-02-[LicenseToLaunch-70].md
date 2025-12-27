---
layout: single
title: "[백준 17912] License To Launch (C#, C++) - soo:bak"
date: "2023-09-02 23:59:00 +0900"
description: 수학, 정렬, 구현 등을 주제로 하는 백준 17912번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 17912
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 17912, 백준 17912번, BOJ 17912, LicenseToLaunch, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [17912번 - License To Launch](https://www.acmicpc.net/problem/17912)

## 설명
`n` 일 동안의 우주 쓰레기의 양이 주어졌을 때, 우주 쓰레기의 양이 가장 적은 날을 찾아 로켓 발사가 가능한 날짜를 구하는 문제입니다. <br>
<br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var spaceJunk = new int[n];

      var input = Console.ReadLine()!.Split(' ');
      for (int i = 0; i < n; i++)
        spaceJunk[i] = int.Parse(input[i]);

      var minJunk = spaceJunk.Min();
      var launchDay = Array.IndexOf(spaceJunk, minJunk);

      Console.WriteLine(launchDay);

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

  vector<int> spaceJunk(n);
  for (int i = 0; i < n; i++)
    cin >> spaceJunk[i];

  int minJunk = *min_element(spaceJunk.begin(), spaceJunk.end());
  auto launchDay = find(spaceJunk.begin(), spaceJunk.end(), minJunk) - spaceJunk.begin();

  cout << launchDay << "\n";

  return 0;
}
  ```
