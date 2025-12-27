---
layout: single
title: "[백준 27475] Cancel the Trains (C#, C++) - soo:bak"
date: "2023-03-29 16:04:00 +0900"
description: 탐색과 구현을 주제로 하는 백준 27475번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 27475
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
keywords: "백준 27475, 백준 27475번, BOJ 27475, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [27475번 - Cancel the Trains](https://www.acmicpc.net/problem/27475)

## 설명
구현과 탐색을 주제로 하는 문제입니다. <br>

문제의 목표는 같은 시간에 출발하는 `하단에서 상단으로 이동하는 기차` 와 `좌측에서 우측으로 이동하는 기차` 들 중 <br>

`충돌을 막기 위해 취소해야 하는 기차의 최소 개수` 를 찾는 것입니다.<br>

문제의 조건 중 입력으로 주어지는 기차의 번호는 <b>항상 오름차순으로 정렬</b> 이 되어 주어진다는 보장이 있으므로, <br>

`이진 탐색` 을 사용하여 중복되는 기차의 번호를 탐색할 수 있습니다. <br>

따라서, `하단 출발 기차` 에 대하여 반복문을 돌며, <br>

`좌측 출발 기차` 의 번호들 중 <u>하단 기차 번호와 동일한 기차가 있는지</u> 이진 탐색으로 확인합니다. <br>

이 때, 해당 `하단 출발 기차` 번호와 동일한 번호가 `좌측 출발 기차` 에 존재한다면, <b>해당 기차는 충돌이 발생할 수 있음</b> 을 의미합니다. <br>

위 과정을 통해 `충돌을 막기 위해 취소해야하는 기차의 최소 개수` 를 구한 후 문제의 조건에 맞게 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var cntCase = int.Parse(Console.ReadLine()!);

      while (cntCase-- > 0) {
        var input = Console.ReadLine()!.Split(' ');
        var n = int.Parse(input[0]);
        var m = int.Parse(input[1]);

        var bottom = new List<int>(n);
        var left = new List<int>(m);

        input = Console.ReadLine()!.Split(' ');
        for (var i = 0; i < n; i++)
          bottom.Add(int.Parse(input[i]));

        input = Console.ReadLine()!.Split(' ');
        for (var i = 0; i < m; i++)
          left.Add(int.Parse(input[i]));

        var ans = 0;
        for (var i = 0; i < n; i++) {
          if (left.BinarySearch(bottom[i]) >= 0)
            ans++;
        }

        Console.WriteLine(ans);
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

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntCase, n, m;
  cin >> cntCase;

  while (cntCase--) {
    cin >> n >> m;

    vi bottom(n), left(m);
    for (int i = 0; i < n; i++)
      cin >> bottom[i];

    for (int i = 0; i < m; i++)
      cin >> left[i];

    int ans = 0;
    for (int i = 0; i < n; i++) {
      if (binary_search(left.begin(), left.end(), bottom[i]))
        ans++;
    }

    cout << ans << "\n";
  }

  return 0;
}
  ```
