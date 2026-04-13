---
layout: single
title: "[백준 15177] Kiwis vs Kangaroos (C#, C++) - soo:bak"
date: "2026-04-13 22:07:00 +0900"
description: "백준 15177번 C#, C++ 풀이 - 비밀 문구의 각 문자가 두 키워드에 몇 번 들어 있는지 더해 승자를 정하는 문제"
tags:
  - 백준
  - BOJ
  - 15177
  - C#
  - C++
  - 알고리즘
  - 문자열
  - 구현
keywords: "백준 15177, 백준 15177번, BOJ 15177, Kiwis vs Kangaroos, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15177번 - Kiwis vs Kangaroos](https://www.acmicpc.net/problem/15177)

## 설명
비밀 문구가 주어질 때, 각 문자가 `KANGAROO`와 `KIWIBIRD`에 몇 번 들어 있는지를 점수로 더해서 어느 쪽 점수가 더 큰지 구하는 문제입니다.

<br>

## 접근법
먼저 `KANGAROO`와 `KIWIBIRD`에 각 알파벳이 몇 번 들어 있는지 미리 셉니다.

그 다음 비밀 문구를 한 글자씩 보면서, 해당 문자가 두 단어에 등장하는 횟수를 각각 점수에 더하면 됩니다. 대소문자는 구분하지 않으므로 한쪽 형태로 바꿔서 처리하면 됩니다.

마지막에 두 점수를 비교해 `Kangaroos`, `Kiwis`, `Feud continues` 중 하나를 출력하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string phrase = Console.ReadLine()!.ToLower();

    int[] kangaroo = new int[26];
    int[] kiwi = new int[26];

    CountLetters("kangaroo", kangaroo);
    CountLetters("kiwibird", kiwi);

    int kangarooScore = 0;
    int kiwiScore = 0;

    foreach (char ch in phrase) {
      int idx = ch - 'a';
      kangarooScore += kangaroo[idx];
      kiwiScore += kiwi[idx];
    }

    if (kangarooScore > kiwiScore)
      Console.WriteLine("Kangaroos");
    else if (kiwiScore > kangarooScore)
      Console.WriteLine("Kiwis");
    else
      Console.WriteLine("Feud continues");
  }

  static void CountLetters(string word, int[] count) {
    foreach (char ch in word) {
      count[ch - 'a']++;
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

void countLetters(const string& word, vector<int>& count) {
  for (char ch : word) {
    count[ch - 'a']++;
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string phrase;
  cin >> phrase;

  for (char& ch : phrase) {
    ch = (char)tolower(ch);
  }

  vector<int> kangaroo(26, 0), kiwi(26, 0);
  countLetters("kangaroo", kangaroo);
  countLetters("kiwibird", kiwi);

  int kangarooScore = 0;
  int kiwiScore = 0;

  for (char ch : phrase) {
    int idx = ch - 'a';
    kangarooScore += kangaroo[idx];
    kiwiScore += kiwi[idx];
  }

  if (kangarooScore > kiwiScore)
    cout << "Kangaroos\n";
  else if (kiwiScore > kangarooScore)
    cout << "Kiwis\n";
  else
    cout << "Feud continues\n";

  return 0;
}
```
