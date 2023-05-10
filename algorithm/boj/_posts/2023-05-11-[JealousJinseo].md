---
layout: single
title: "[백준 15784] 질투진서 (C#, C++) - soo:bak"
date: "2023-05-11 06:47:00 +0900"
---

## 문제 링크
  [15784번 - 질투진서](https://www.acmicpc.net/problem/15784)

## 설명
강의실에 앉아 있는 사람들의 매력지수를 비교하여, <br>

진서가 자기보다 잘생긴 사람을 볼 수 있는지 확인하는 문제입니다. <br>

진서는 <b>같은 행</b> 또는 <b>같은 열</b>에 있는 사람만을 볼 수 있다는 점을 이용하여 문제를 풀이합니다. <br>

강의실의 모든 사람들의 매력지수를 입력받은 후, <br>

모든 행과 열을 순회하며 진서의 매력지수와 비교하는 완전 탐색 방법으로 풀이하였습니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ');
      var n = int.Parse(input[0]);
      var a = int.Parse(input[1]);
      var b = int.Parse(input[2]);

      var lstScrs = new List<List<int>>(n);
      for (int x = 0; x < n; x++) {
        input = Console.ReadLine()!.Split(' ');
        var lstCols  = new List<int>(n);
        for (int y = 0; y < n; y++)
          lstCols.Add(int.Parse(input[y]));
        lstScrs.Add(lstCols);
      }

      var scrJin = lstScrs[a - 1][b - 1];

      for (int x = 0; x < n; x++) {
        if (x != a - 1 && lstScrs[x][b - 1] > scrJin) {
          Console.WriteLine("ANGRY"); return ;
        }
      }

      for (int y = 0; y < n; y++) {
        if (y != b - 1 && lstScrs[a - 1][y] > scrJin) {
          Console.WriteLine("ANGRY"); return ;
        }
      }

      Console.WriteLine("HAPPY");

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

  int n, a, b; cin >> n >> a >> b;

  vector<vi> vScrs(n, vi(n));
  for (int x = 0; x < n; x++) {
    for (int y = 0; y < n; y++)
      cin >> vScrs[x][y];
  }

  int scrJin = v[a - 1][b - 1];

  for (int x = 0; x < n; x++) {
    if (x != a - 1 && vScrs[x][b - 1] > scrJin) {
      cout << "ANGRY\n"; return 0;
    }
  }

  for (int y = 0; y < n; y++) {
    if (y != b - 1 && vScrs[a - 1][y] > scrJin) {
      cout << "ANGRY\n"; return 0;
    }
  }

  cout << "HAPPY\n";

  return 0;
}
  ```
