---
layout: single
title: "[백준 2884] 알람 시계 (C#, C++) - soo:bak"
date: "2023-05-16 14:29:00 +0900"
description: 수학과 시간 계산을 주제로 하는 백준 2884번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [2884번 - 알람 시계](https://www.acmicpc.net/problem/2884)

## 설명
알람 시간의 조정과 관련된 문제입니다.<br>

문제의 목표는 `45` 분 앞서는 시간으로 알람 시간을 조정하는 것입니다. <br>

따라서, 현재 설정된 알람 시간에서 `45` 분을 뺀 결과에 따라서 시간과 분에 대한 계산 처리를 해줍니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ');
      var hour = int.Parse(input[0]);
      var min = int.Parse(input[1]);

      min -= 45;
      if (min < 0) {
        min += 60;
        hour--;
        if (hour < 0)
          hour = 23;
      }

      Console.WriteLine($"{hour} {min}");

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

  int hour, min; cin >> hour >> min;

  min -= 45;
  if (min < 0) {
    min += 60;
    hour--;
    if (hour < 0)
      hour = 23;
  }

  cout << hour << " " << min << "\n";

  return 0;
}
  ```
