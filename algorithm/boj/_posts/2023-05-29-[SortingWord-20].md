---
layout: single
title: "[백준 1181] 단어 정렬 (C#, C++) - soo:bak"
date: "2023-05-29 09:11:00 +0900"
---

## 문제 링크
  [1181번 - 단어 정렬](https://www.acmicpc.net/problem/1181)

## 설명
입력으로 주어지는 단어들을 두 가지 기준으로 정렬하는 문제입니다. <br>

기준은 다음과 같습니다.<br>

1. 단어의 길이가 짧은 것이 앞 순서로<br>
2. 단어의 길이가 같다면 알파벳 사전 순으로 <br>

`C#` 에서는 `LINQ` 를 활용하여 `Orderby()` 와 `Thenby()` 를 통해 정렬합니다. <br>

`C++` 에서는 `sort()` 함수에서 사용할 <b>단어의 길이를 먼저 비교하고, 길이가 같다면 사전순으로 비교를 하는 비교 함수</b> 를 구현하여 정렬합니다. <br>

<br>
또한, 문제의 조건에 따라 중복 단어들은 하나만 남기고 제거해야 하는데, <br>

`C#` 에서는 `LINQ` 의 `Distinct()` 를 사용하여 중복 요소를 제거합니다. <br>

`C++` 에서는 `erase()` 함수와 `unique()` 함수를 통해 중복 요소를 제거합니다. <br>


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
