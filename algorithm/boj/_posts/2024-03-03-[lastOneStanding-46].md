---
layout: single
title: "[백준 30569] Last One Standing (C#, C++) - soo:bak"
date: "2024-03-03 21:38:00 +0900"
description: 수학, 구현, 사칙연산, 시뮬레이션 등을 주제로 하는 백준 30569번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 30569
  - C#
  - C++
  - 알고리즘
keywords: "백준 30569, 백준 30569번, BOJ 30569, lastOneStanding, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [30569번 - Last One Standing](https://www.acmicpc.net/problem/30569)

## 설명
문제의 목표는 두 플레이어가 각각 하나의 유닛을 컨트롤하여 게임에서 싸우는 시나리오를 시뮬레이션 하는 것입니다.<br>
<br>
각 유닛은 `건강(h)`, `피해랑(d)`, `재장전 시간(t)` 을 속성으로 가지고 있습니다.<br>
<br>
또한, 미사일이 발사된 후 `0.5` 초가 지나야 상대방 유닛의 건강이 감소하며,<br>
<br>
같은 유닛이 연속해서 미사일을 발사할 수 있는 최소 시간 간격은 `t` 초여야 한다는 규칙이 존재합니다.<br>
<br>
<br>
- 각 유닛의 `다음 발사 가능 시간`, 그리고 `현재 시간` 을 `0` 으로 초기화 합니다.<br>
<br>
- 두 유닛의 건강이 모두 `0` 보다 클 동안, 즉, 두 유닛이 모두 파괴되지 않은 상태에서 게임을 시뮬레이션 합니다.<br>
<br>
- 각 유닛에 대해, `현재 시간` 이 해당 유닛의 `다음 발사 가능 시간` 보다 크거나 같다면,<br>
<br>
유닛은 미사일을 발사하고, 상대방의 `건강` 을 `피해량` 만큼 감소시킵니다.<br>
<br>
- 또한, 해당 유닛의 `다음 발사 가능 시간` 을 `현재시간` + `재장전 시간` 으로 갱신합니다.<br>
<br>
- 이후, 현재 시간을 `0.5` 초 씩 증가시킵니다.<br>
<br>
<br>

시뮬레이션을 진행하면서, 만약, 한 플레이어의 유닛만 건강이 `0` 이하가 된 경우,<br>
<br>
해당 유닛을 컨트롤하는 플레이어가 패배합니다.<br>
<br>
두 유닛이 동시에 파괴되었다면, 게임은 무승부로 끝납니다.<br>
<br>
게임의 종료 결과에 따라서, 문제에서 요구하는 문자열을 출력합니다.<br>
<br>
<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ').Select(int.Parse).ToArray();
      int h1 = input[0], d1 = input[1], t1 = input[2];
      input = Console.ReadLine()!.Split(' ').Select(int.Parse).ToArray();
      int h2 = input[0], d2 = input[1], t2 = input[2];

      double nextFire_1 = 0, nextFire_2 = 0;
      double time = 0;

      while(h1 > 0 && h2 > 0) {
        if (time >= nextFire_1) {
          nextFire_1 = time + t1;
          h2 -= d1;
        }

        if (time >= nextFire_2) {
          nextFire_2 = time + t2;
          h1 -= d2;
        }
        time += 0.5;
      }

      if (h1 > 0) Console.WriteLine("player one");
      else if (h2 > 0) Console.WriteLine("player two");
      else Console.WriteLine("draw");
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

  int h1, d1, t1, h2, d2, t2;
  cin >> h1 >> d1 >> t1 >> h2 >> d2 >> t2;

  double nextFire1 = 0, nextFire2 = 0;
  double time = 0;

  while (h1 > 0 && h2 > 0) {
    if (time >= nextFire1) {
      nextFire1 = time + t1;
      h2 -= d1;
    }
    if (time >= nextFire2) {
      nextFire2 = time + t2;
      h1 -= d2;
    }
    time += 0.5;
  }

  if (h1 > 0) cout << "player one\n";
  else if (h2 > 0) cout << "player two\n";
  else cout << "draw\n";

  return 0;
}
  ```
