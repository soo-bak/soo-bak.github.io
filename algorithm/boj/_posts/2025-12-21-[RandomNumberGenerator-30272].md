---
layout: single
title: "[백준 30272] Atsitiktinių skaičių generatorius (C#, C++) - soo:bak"
date: "2025-12-21 20:42:00 +0900"
description: 8×9 픽셀로 주어진 숫자 패턴을 사전 매핑으로 복원해 생성된 수를 출력하는 문제
---

## 문제 링크
[30272번 - Atsitiktinių skaičių generatorius](https://www.acmicpc.net/problem/30272)

## 설명
8줄×9열의 픽셀 패턴으로 표현된 숫자들을 해독해 원래 수를 복원하는 문제입니다.

<br>

## 접근법
0부터 9까지의 픽셀 패턴을 미리 저장해둡니다. 입력을 8줄씩 읽어서 하나의 문자열로 합친 뒤, 저장해둔 패턴과 비교해 어떤 숫자인지 찾습니다. 모든 자릿수를 순서대로 해독하면 원래 수를 복원할 수 있습니다.

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static readonly string[] digit0 = {"..#####..",".##...##.","##.....##","##.....##","##.....##",".##...##.","..#####..","........."};
  static readonly string[] digit1 = {"....##...","..####...","....##...","....##...","....##...","....##...","..######.","........."};
  static readonly string[] digit2 = {".#######.","##.....##",".......##",".#######.","##.......","##.......","#########","........."};
  static readonly string[] digit3 = {".#######.","##.....##",".......##",".#######.",".......##","##.....##",".#######.","........."};
  static readonly string[] digit4 = {"##.......","##....##.","##....##.","##....##.","#########","......##.","......##.","........."};
  static readonly string[] digit5 = {".########",".##......",".##......",".#######.",".......##",".##....##","..######.","........."};
  static readonly string[] digit6 = {".#######.","##.....##","##.......","########.","##.....##","##.....##",".#######.","........."};
  static readonly string[] digit7 = {".########",".##....##",".....##..","....##...","...##....","...##....","...##....","........."};
  static readonly string[] digit8 = {".#######.","##.....##","##.....##",".#######.","##.....##","##.....##",".#######.","........."};
  static readonly string[] digit9 = {".#######.","##.....##","##.....##",".########",".......##","##.....##",".#######.","........."};

  static readonly Dictionary<string, char> digitMap = new() {
    {string.Join("\n", digit0), '0'}, {string.Join("\n", digit1), '1'},
    {string.Join("\n", digit2), '2'}, {string.Join("\n", digit3), '3'},
    {string.Join("\n", digit4), '4'}, {string.Join("\n", digit5), '5'},
    {string.Join("\n", digit6), '6'}, {string.Join("\n", digit7), '7'},
    {string.Join("\n", digit8), '8'}, {string.Join("\n", digit9), '9'}
  };

  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var res = "";

    var lines = new string[8];
    for (var i = 0; i < n; i++) {
      for (var j = 0; j < 8; j++)
        lines[j] = Console.ReadLine()!;
      res += digitMap[string.Join("\n", lines)];
    }

    Console.WriteLine(res);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<string> vs;
typedef map<vs, char> mvsc;

const vs digit0 = {"..#####..",".##...##.","##.....##","##.....##","##.....##",".##...##.","..#####..","........."};
const vs digit1 = {"....##...","..####...","....##...","....##...","....##...","....##...","..######.","........."};
const vs digit2 = {".#######.","##.....##",".......##",".#######.","##.......","##.......","#########","........."};
const vs digit3 = {".#######.","##.....##",".......##",".#######.",".......##","##.....##",".#######.","........."};
const vs digit4 = {"##.......","##....##.","##....##.","##....##.","#########","......##.","......##.","........."};
const vs digit5 = {".########",".##......",".##......",".#######.",".......##",".##....##","..######.","........."};
const vs digit6 = {".#######.","##.....##","##.......","########.","##.....##","##.....##",".#######.","........."};
const vs digit7 = {".########",".##....##",".....##..","....##...","...##....","...##....","...##....","........."};
const vs digit8 = {".#######.","##.....##","##.....##",".#######.","##.....##","##.....##",".#######.","........."};
const vs digit9 = {".#######.","##.....##","##.....##",".########",".......##","##.....##",".#######.","........."};

mvsc digitMap = {
  {digit0, '0'}, {digit1, '1'}, {digit2, '2'}, {digit3, '3'}, {digit4, '4'},
  {digit5, '5'}, {digit6, '6'}, {digit7, '7'}, {digit8, '8'}, {digit9, '9'}
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  cin.ignore();

  string res;
  vs lines(8);

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < 8; j++)
      getline(cin, lines[j]);
    res += digitMap[lines];
  }

  cout << res << "\n";

  return 0;
}
```
