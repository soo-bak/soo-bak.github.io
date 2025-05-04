---
layout: single
title: "[백준 1181] 단어 정렬 (C#, C++) - soo:bak"
date: "2023-05-29 09:11:00 +0900"
description: 문자열 정렬과 탐색 등을 주제로 하는 백준 1181번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [1181번 - 단어 정렬](https://www.acmicpc.net/problem/1181)

## 설명
입력으로 주어지는 단어들을 두 가지 기준으로 정렬하는 문제입니다. <br>

기준은 다음과 같습니다.<br>

1. 단어의 길이가 짧은 것이 앞 순서로<br>
2. 단어의 길이가 같다면 알파벳 사전 순으로 <br>

<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var words = new string[n];
      for (int i = 0; i < n; i++)
        words[i] = Console.ReadLine()!;

      words = words
            .Distinct()
            .OrderBy(w => w.Length)
            .ThenBy(w => w)
            .ToArray();

      foreach (var word in words)
        Console.WriteLine(word);

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

bool comp(const string& a, const string& b) {
  if (a.size() != b.size())
    return a.size() < b.size();
  return a < b;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  vector<string> words(n);
  for (int i = 0; i < n; i++)
    cin >> words[i];

  sort(words.begin(), words.end(), comp);

  words.erase(unique(words.begin(), words.end()), words.end());

  for (const auto& word : words)
    cout << word << "\n";

  return 0;
}
  ```
