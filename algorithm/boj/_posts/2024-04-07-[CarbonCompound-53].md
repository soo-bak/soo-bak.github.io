---
layout: single
title: "[백준 1907] 탄소 화합물 (C#, C++) - soo:bak"
date: "2024-04-07 23:11:00 +0900"
description: 구현, 문자열, 완전 탐색, 브루트포스 알고리즘, 파싱 등을 주제로 하는 백준 1907번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [1907번 - 탄소 화합물](https://www.acmicpc.net/problem/1907)

## 설명
탄소(C), 수소(H), 산소(O) 세 가지 종류의 원자로만 이루어진 화합물에 대한 화학 반응식의 <b>균형</b>을 맞추는 문제입니다.<br>
<br>
화학 반응식은 `분자 + 분자 = 분자` 의 형태로 주어지며,<br>
<br>
각 분자는 원자 다음에 그 원자의 개수를 나타내는 숫자가 붙는 형식입니다.<br>
<br>
위 형식을 고려하여, 반응식의 양쪽이 균형을 이루도록 하는 각 분자의 계수를 탐색합니다.<br>
<br>
<br>
먼저, 주어진 화학 반응식에서 각 분자를 파싱하여, C, H, O 원자의 개수를 계산합니다.<br>
<br>
이후, 가능한 모든 계수 조합(문제의 조건에 따라, `1` 이상 `10` 이하의 자연수)을 대입하여 반응식의 양쪽에서 각 원자의 총 개수가 같아지는 조합을 탐색합니다.<br>
<br>
마지막으로, 균형을 맞출 수 있는 계수를 찾았다면, 해당 계수를 출력합니다.<br>
<br>
이 때, 여러 해가 있는 경우 사전순으로 가장 앞선 해를 먼저 출력해야 한다는 점에 주의합니다.<br>

<br>
<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    static List<int> ParseMolecule(string formula) {
      var cnt_C_H_O = new List<int> {0, 0, 0};
      var lastAtom = ' ';

      foreach (var atom in formula) {
        if (atom == 'C' || atom == 'H' || atom == 'O')  {
          lastAtom = atom;
          cnt_C_H_O[lastAtom == 'C' ? 0 : lastAtom == 'H' ? 1 : 2]++;
        } else cnt_C_H_O[lastAtom == 'C' ? 0 : lastAtom == 'H' ? 1 : 2] += atom - '1';
      }

      return cnt_C_H_O;
    }

    static void Main(string[] args) {

      var formula = Console.ReadLine()!;
      var plusPos = formula.IndexOf('+');
      var eqPos = formula.IndexOf('=');
      var m1 = formula[..plusPos];
      var m2 = formula[(plusPos +1) .. eqPos];
      var m3 = formula[(eqPos + 1)..];

      var cntM1 = ParseMolecule(m1);
      var cntM2 = ParseMolecule(m2);
      var cntM3 = ParseMolecule(m3);

      for (int x1 = 1; x1 <= 10; x1++) {
        for (int x2 = 1; x2 <= 10; x2++) {
          for (int x3 = 1; x3 <= 10; x3++) {
            if (x1 * cntM1[0] + x2 * cntM2[0] == x3 * cntM3[0] &&
                x1 * cntM1[1] + x2 * cntM2[1] == x3 * cntM3[1] &&
                x1 * cntM1[2] + x2 * cntM2[2] == x3 * cntM3[2]) {
              Console.WriteLine($"{x1} {x2} {x3}");
              return ;
            }
          }
        }
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

vector<int> parseMolecule(const string& formula) {
  vector<int> cnt(3, 0);
  char lastAtom = ' ';
  int n = formula.size();
  for (int i = 0; i < n; i++) {
    if (formula[i] == 'C' || formula[i] == 'H' || formula[i] == 'O') {
      lastAtom = formula[i];
      cnt[lastAtom == 'C' ? 0 : lastAtom == 'H' ? 1 : 2]++;
    } else cnt[lastAtom == 'C' ? 0 : lastAtom == 'H' ? 1 : 2] += formula[i] - '1';
  }

  return cnt;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string formula; cin >> formula;

  size_t plusPos = formula.find('+');
  size_t eqPos = formula.find('=');
  string m1 = formula.substr(0, plusPos),
         m2 = formula.substr(plusPos + 1, eqPos - plusPos - 1),
         m3 = formula.substr(eqPos + 1);

  vector<int> cntM1 = parseMolecule(m1),
              cntM2 = parseMolecule(m2),
              cntM3 = parseMolecule(m3);

  for (int x1 = 1; x1 <= 10; x1++) {
    for (int x2 = 1; x2 <= 10; x2++) {
      for (int x3 = 1; x3 <= 10; x3++) {
        if (x1 * cntM1[0] + x2 * cntM2[0] == x3 * cntM3[0] &&
            x1 * cntM1[1] + x2 * cntM2[1] == x3 * cntM3[1] &&
            x1 * cntM1[2] + x2 * cntM2[2] == x3 * cntM3[2]) {
          cout << x1 << " " << x2 << " " << x3 << "\n";
          return 0;
        }
      }
    }
  }

  return 0;
}
  ```
