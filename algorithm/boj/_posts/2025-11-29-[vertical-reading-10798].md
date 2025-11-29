---
layout: single
title: "[백준 10798] 세로읽기 (C#, C++) - soo:bak"
date: "2025-11-29 22:00:00 +0900"
description: 다섯 줄의 단어를 세로로 읽어 존재하는 문자만 차례로 이어붙이는 백준 10798번 세로읽기 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[10798번 - 세로읽기](https://www.acmicpc.net/problem/10798)

## 설명

다섯 줄의 단어가 주어지는 상황에서, 각 줄의 단어(길이 1~15, 알파벳 대소문자와 숫자로만 구성)가 주어질 때, 세로로 읽은 결과를 출력하는 문제입니다.

세로로 읽는다는 것은 첫 번째 열부터 마지막 열까지 순서대로, 각 열의 문자들을 위에서 아래로 읽는 것을 의미합니다. 해당 위치에 문자가 없으면 건너뛰고 다음 문자를 읽습니다.

<br>

## 접근법

다섯 줄의 단어를 2차원 배열에 저장합니다. 각 줄의 길이가 다를 수 있으므로 최대 길이 15까지 저장할 수 있는 공간을 확보합니다.

열 순서대로 순회하면서 각 열에 대해 행을 위에서 아래로 확인합니다.

해당 위치에 문자가 존재하면 결과 문자열에 추가하고, 없으면 건너뜁니다. 이렇게 모든 열을 순회한 후 최종 문자열을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Text;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var grid = new char[5, 15];
      for (var r = 0; r < 5; r++) {
        var line = Console.ReadLine()!;
        for (var c = 0; c < line.Length; c++)
          grid[r, c] = line[c];
      }

      var result = new StringBuilder();
      for (var c = 0; c < 15; c++) {
        for (var r = 0; r < 5; r++) {
          if (grid[r, c] != '\0')
            result.Append(grid[r, c]);
        }
      }

      Console.WriteLine(result.ToString());
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<char> vc;
typedef vector<vc> vvc;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vvc grid(5, vc(15, '\0'));
  for (int r = 0; r < 5; r++) {
    string word; cin >> word;
    for (size_t c = 0; c < word.length(); c++)
      grid[r][c] = word[c];
  }

  for (int c = 0; c < 15; c++) {
    for (int r = 0; r < 5; r++) {
      if (grid[r][c] != '\0')
        cout << grid[r][c];
    }
  }
  cout << "\n";
  
  return 0;
}
```


