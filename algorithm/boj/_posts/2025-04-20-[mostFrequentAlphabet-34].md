---
layout: single
title: "[백준 1371] 가장 많은 글자 (C#, C++) - soo:bak"
date: "2025-04-20 22:15:00 +0900"
description: 여러 줄의 입력에서 가장 많이 등장한 소문자를 계산하여 출력하는 백준 1371번 가장 많은 글자 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[1371번 - 가장 많은 글자](https://www.acmicpc.net/problem/1371)

## 설명
여러 줄로 구성된 텍스트가 입력으로 주어질 때, 전체에서 **가장 많이 등장한 알파벳 소문자**를 구하는 문제입니다.<br>

- 알파벳은 대소문자를 구분하지 않으며, 모두 소문자로 간주합니다.
- 공백은 글자 수에 포함되지 않으며 무시합니다.
- 가장 많이 등장한 문자가 여러 개일 경우 **사전 순으로 나열하여 모두 출력**합니다.

## 접근법

- 알파벳 소문자 개수를 세기 위해 크기 `26`의 정수 배열을 선언합니다.
- 표준 입력에서 한 줄씩 읽어오며, 공백이 아닌 문자가 나타날 경우 문자를 소문자로 바꾼 뒤 해당 문자의 카운트 수를 증가시킵니다.
- 모든 입력이 끝난 뒤 배열에서 가장 큰 값을 찾아 해당 값과 일치하는 알파벳들을 사전 순으로 출력합니다.


## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int[] freq = new int[26];
    string line;
    while ((line = Console.ReadLine()) != null) {
      foreach (char c in line) {
        if (c != ' ' && char.IsLetter(c)) {
          freq[char.ToLower(c) - 'a']++;
        }
      }
    }

    int max = freq.Max();
    for (int i = 0; i < 26; i++) {
      if (freq[i] == max)
        Console.Write((char)(i + 'a'));
    }
    Console.WriteLine();
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntAlpha[26] = {0, };
  string line;
  while (getline(cin, line)) {
    for (char c : line) {
      if (c != ' ') cntAlpha[tolower(c) - 'a']++;
    }
  }

  int maxAlpha = *max_element(cntAlpha, cntAlpha + 26);
  for (int i = 0; i < 26; i++) {
    if (cntAlpha[i] == maxAlpha) cout << (char)(i + 'a');
  }
  cout << "\n";

  return 0;
}
```
