---
layout: single
title: "[백준 26432] Walktober (C#, C++) - soo:bak"
date: "2023-03-21 18:16:00 +0900"
---

## 문제 링크
  [26432번 - Walktober](https://www.acmicpc.net/problem/26432)

## 설명
  간단한 구현 문제입니다. <br>

  문제의 설명은 다음과 같습니다. <br>

  문제의 주인공 John 은 'Walktober' 라는 걷기 대회에에 참여하는데, 해당 대회는 총 `n` 일 동안 진행됩니다.<br>

  이 때, 대회에 참여한 모든 참가자들의 수는 `m` 명 이며, 각각 `1` 부터 `m` 까지의 고유한 번호를 할당받습니다.<br>

  또한, 대회에서는 매년 &nbsp;<b>'모든 참가자들의 일일 걸음 수'</b> 를 기록합니다.<br>

  문제의 목표는 입력으로 주어지는 작년 대회의 기록표를 바탕으로, <br>

  매일 최대로 많이 걸었던 다른 참가자의 걸음 수에 도달하기 위한 &nbsp;<b>John 의 최소 추가 걸음 수</b> 를 계산하는 것 입니다.<br>

  입력으로 주어지는 t, m, n, p, s<sub>{i, j}</sub> 들의 관계와, 다차원 배열을 다루는 부분만 유의한다면 쉽게 풀이할 수 있는 문제입니다.<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var sb = new System.Text.StringBuilder();

      var cntCase = int.Parse(Console.ReadLine()!);
      for (int c = 1; c <= cntCase; c++) {
        var inputs = Console.ReadLine()?.Split(' ').Select(int.Parse).ToArray();
        var m = inputs![0];
        var n = inputs![1];
        var p = inputs![2];

        var steps = new int[m][];
        for (int i = 0; i < m; i++)
          steps[i] = Console.ReadLine()!.Split(' ').Select(int.Parse).ToArray();

        var totalAdditionalSteps = 0;
        for (int day = 0; day < n; day++) {
          var maxSteps = 0;
          for (int participant = 0; participant < m; participant++) {
            if (participant != p - 1)
              maxSteps = Math.Max(maxSteps, steps[participant][day]);
          }
          totalAdditionalSteps += Math.Max(maxSteps - steps[p - 1][day], 0);
        }

        sb.AppendLine($"Case #{c}: {totalAdditionalSteps}");
      }

      Console.Write(sb.ToString());

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

  int cntCase; cin >> cntCase;
  for (int c = 1; c <= cntCase; c++) {
    int m, n, p; cin >> m >> n >> p;

    vector<vi> steps(m, vi(n));
    for (int i = 0; i < m; i++) {
      for (int j = 0; j < n; j++)
        cin >> steps[i][j];
    }

    int totalAdditionalSteps = 0;
    for (int day = 0; day < n; ++day) {
      int maxSteps = 0;
      for (int participant = 0; participant < m; participant++) {
        if (participant != p - 1)
            maxSteps = max(maxSteps, steps[participant][day]);
      }
      totalAdditionalSteps += max(0, maxSteps - steps[p - 1][day]);
    }

    cout << "Case #" << c << ": " << totalAdditionalSteps << "\n";
  }

  return 0;
}
  ```
