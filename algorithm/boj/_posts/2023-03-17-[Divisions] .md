---
layout: single
title: "[백준 27227] Дивизионы (C#, C++) - soo:bak"
date: "2023-03-17 16:42:00 +0900"
description: 구현과 수학을을 주제로 하는 백준 27227번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [27227번 - Дивизионы](https://www.acmicpc.net/problem/27227)

## 설명
  간단한 구현 문제입니다. <br>

  문제의 설명에 따르면 대회의 참가자들은 점수에 따라서 참가할 수 있는 <b>기본적인 경기 구역</b> 이 정해져있습니다.<br>
  점수에 따른 구역은 다음과 같이 정해집니다.
  - `0` <= `점수` <= `1600` : &nbsp;`3` 구역에 배정
  - `1601` <= `점수` <= `1900` : &nbsp;`2` 구역에 배정
  - `1901` < `점수` : &nbsp;`1` 구역에 배정

  <b>문제의 목표는 참가자의 `점수` 에 따라서 참가할 수 있는</b> `경기 구역` <b>을 구하는 것입니다.</b><br>

  <b>참가할 수 있는 </b>`경기 구역` <b>에 대한 조건은 다음과 같습니다.</b><br>
  1. 만약, 입장 가능한 구역중 자신이 배정된 구역이 있다면, 반드시 그 구역에만 입장해야 한다.
  2. 만약, 입장 가능한 구역중 자신이 배정된 구역이 없다면 다른 구역에 참가할 수 있다.
  3. 자신이 배정된 구역과 다른 구역에 참가하는 경우 중, 낮은 등급의 구역에는 `번외`로만 참가할 수 있다.

  위 조건들에 맞추어, 참가자가 참가할 수 있는 대회 구역을 구한 후 조건에 맞게 출력합니다.<br>
  - `번외` 로 참가하는 경기 구역에 대해서는 경기 구역 번호 뒤에 `*` 을 붙여야 합니다.

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var rating = int.Parse(Console.ReadLine()!);
      var divisions = Console.ReadLine();

      char defaultDivision = '1';
      if (rating <= 1600) defaultDivision = '3';
      else if (rating <= 1900) defaultDivision = '2';

      if (divisions!.Contains(defaultDivision)) {
        Console.WriteLine(defaultDivision);
        return ;
      }

      foreach (char division in divisions) {
        if (defaultDivision > division)
          Console.WriteLine(division);
        else if (defaultDivision < division)
          Console.WriteLine($"{division}*");
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

  int rating; cin >> rating;
  string divisions; cin >> divisions;

  char defaultDivision = '1';
  if (rating <= 1600) defaultDivision = '3';
  else if (rating <= 1900) defaultDivision = '2';

  if (divisions.find(defaultDivision) != string::npos) {
    cout << defaultDivision << "\n";
    return 0;
  }

  for (char c : divisions) {
    char division = c;
    if (defaultDivision > division)
      cout << division << "\n";
    else if (defaultDivision < division)
      cout << division << "*\n";
  }

  return 0;
}
  ```
