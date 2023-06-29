---
layout: single
title: "[백준 4922] Walk Like an Egyptian (C#, C++) - soo:bak"
date: "2023-06-25 11:04:00 +0900"
description: 수학, 반복문, 탐색 등을 주제로 하는 백준 4922번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [4922번 - Walk Like an Egyptian](https://www.acmicpc.net/problem/4922)

## 설명
사하라 사막의 유목 부족 아이들이 즐겨한다는 <b>Walk Like an Egyptian</b> 게임에 대한 문제입니다. <br>

게임에 대한 설명은 다음과 같습니다. <br>

- `n` 명의 플레이어를 위해 `n`<sup>2</sup> 개의 돌을 준비하며, 각각의 돌들은 고유의 번호를 갖는다. <br>
- 해당 돌들을 `n` * `n` 격자에 배치하며, 배치의 순서는 문제의 그림 `a` 와 같이 배치된다. <br>
- 배치를 진행하면서, 오른쪽 상단에 위치한 돌의 주인이 해당 라운드에서 패배하게 된다. <br>
- 이러한 과정을 총 `n - 1` 번 진행하면서 최종 승자를 결정한다. <br>

문제에서 설명되는 돌의 배치 규칙을 살펴보면, 오른쪽 상단에 위치한 돌의 번호의 일반항은 `n`<sup>2</sup> - `n` + `1` 이 됩니다. <br>

위 일반항에 따라서, 입력으로 주어지는 `n` 에 대하여 오른쪽 상단에 위치한 돌의 번호를 계산하여 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      while (true) {
        var n = int.Parse(Console.ReadLine()!);
        if (n == 0) break ;

        Console.WriteLine($"{n} => {n * n - n + 1}");
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

  int n;
  while (cin >> n) {
    if (n == 0) break ;

    cout << n << " => " << n * n - n + 1 << "\n";
  }

  return 0;
}
  ```
