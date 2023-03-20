---
layout: single
title: "[백준 16088] Finding Your Coach (C#, C++) - soo:bak"
date: "2023-03-20 12:25:00 +0900"
---

## 문제 링크
  [16088번 - Finding Your Coach](https://www.acmicpc.net/problem/16088)

## 설명
  기차의 탑승과 관련된 시뮬레이션 문제입니다. <br>
  <br>
  문제의 설명에 따르면, 기차의 객차 번호는 `연속되는 양의 정수` 로 이루어진다는 것만 알 수 있으며,<br>
  `어느 방향` 인지는 알 수가 없습니다.<br>
  <br>
  따라서, 가능한 경우의 수에 Laurie 의 행동을 직접 시뮬레이션 한 후 출력합니다. <br>
  <br>
  <b>문제의 조건에 따르면, Laurie 가 가능한 행동은 다음과 같습니다.</b>
  1. Laurie 가 현재 올바른 객차 앞에 서있다면, `G`를 출력합니다.
  2. Laurie 의 객차가 반드시 주어진 객차의 왼쪽에 있는 것으로 판별된다면, `L` 을 출력합니다.
  3. Laurie 의 객차가 반드시 주어진 객차의 오른쪽에 있는 것으로 판별된다면, `R` 을 출력합니다.
  4. Laurie 의 객차에 대한 판단을 할 수 없는 경우, `E` 를 출력합니다.

  <br>
  <b>입력으로 주어지는 정보는 다음과 같습니다.</b>
  1. `l` : Laurie 의 왼쪽에 있는 객차의 수
  2. `r` : Laurie 의 오른쪽에 있는 객차의 수
  3. `n` : Laurie 의 앞에 있는 객차의 번호
  4. `m` : Laurie 가 찾고 있는 객차의 번호

  입력으로 주어지는 정보를 바탕으로, Laurie 가 가능한 행동을 문제의 조건에 맞추어 출력합니다.<br>

  > <b>참고</b> <br>
  `cpp` 와 다르게, `C#` 에서는 반복문 안에서 직접 `Console.Writeline()` 메서드를 호출 시 시간 초과가됩니다. <br>
  따라서, `System.Text` 네임스페이스 안에 있는 `StringBuilder()` 메서드를 통해 매 반복문마다 결과값만 계산한 후 출력을 준비하고, <br>
  모든 시뮬레이션이 종료된 뒤, 한 번에 출력을 하도록 구현하였습니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var cntCase = int.Parse(Console.ReadLine()!);
      var output = new System.Text.StringBuilder();

      for (int i = 0; i < cntCase; i++) {
        var input = Console.ReadLine()?.Split();
        var l = int.Parse(input![0]);
        var r = int.Parse(input![1]);
        var n = int.Parse(input![2]);
        var m = int.Parse(input![3]);

        string ans = "";
        if (n == m) ans = "G";
        else {
          int cntWay = 0;
          if (Math.Abs(n - m) <= l) {
            ans = "L";
            cntWay++;
          }
          if (Math.Abs(n - m) <= r) {
            ans = "R";
            cntWay++;
          }

          bool enableToFigure = true;
          if (cntWay > 1) enableToFigure = false;

          if (!enableToFigure) ans = "E";
        }
        output.AppendLine(ans);
      }
      Console.Write(output);
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

  int cntCase; cin >> cntCase;

  while (cntCase--) {
    int l, r, n, m; cin >> l >> r >> n >> m;

    string ans = "";
    if (n == m) ans = "G";
    else {
      int cntWay = 0;
      if (abs(n - m) <= l) {
        ans = "L";
        cntWay++;
      }
      if (abs(n - m) <= r) {
        ans = "R";
        cntWay++;
      }

      bool enableToFigure = true;
      if (cntWay > 1) enableToFigure = false;

      if (!enableToFigure) ans = "E";
    }
    cout << ans << "\n";
  }

  return 0;
}
  ```
