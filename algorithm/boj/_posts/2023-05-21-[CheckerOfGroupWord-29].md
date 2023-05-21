---
layout: single
title: "[백준 1316] 그룹 단어 체커 (C#, C++) - soo:bak"
date: "2023-05-21 16:13:00 +0900"
---

## 문제 링크
  [1316번 - 그룹 단어 체커](https://www.acmicpc.net/problem/1316)

## 설명
문제에의 조건에 따른 `그룹 단어` 를 세는 문제입니다. <br>

단어에 존재하는 모든 문자에 대해서 각 문자가 연속해서 나타날 떄, 해당 단어는 `그룹 단어` 입니다. <br>

따라서, 각 단어를 순회하며 현재 문자가 이전 문자와 같지 않고, 이미 나타난 적이 있는 문자라면 해당 단어는 그룹 단어가 아니게 됩니다. <br>

위 조건을 이용하여 각 단어에 대해 `그룹 단어` 인지 판별한 후, `그룹 단어` 의 숫자를 세어 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      int cntGroupWords = 0;
      for (int i = 0; i < n; i++) {
        var word = Console.ReadLine()!;

        var isAppeared = new bool[26];
        char lastChar = word[0];
        isAppeared[lastChar - 'a'] = true;

        bool isGroupWord = true;
        for (int j = 1; j < word.Length; j++) {
          if (lastChar != word[j]) {
            if (isAppeared[word[j] - 'a']) {
              isGroupWord = false; break ;
            }
            isAppeared[word[j] - 'a'] = true;
            lastChar = word[j];
          }
        }

        if (isGroupWord) cntGroupWords++;
      }

      Console.WriteLine(cntGroupWords);

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

  int n; cin >> n;

  int cntGroupWords = 0;
  for (int i = 0; i < n; i++) {
    string word; cin >> word;

    bool isAppeard[26] = {false, };
    char lastChar = word[0];
    isAppeard[lastChar - 'a'] = true;

    bool isGroupWord = true;
    for (size_t j = 1; j < word.length(); j++) {
      if (lastChar != word[j]) {
        if (isAppeard[word[j] - 'a']) {
          isGroupWord = false; break ;
        }
        isAppeard[word[j] - 'a'] = true;
        lastChar = word[j];
      }
    }

    if (isGroupWord) cntGroupWords++;
  }

  cout << cntGroupWords << "\n";

  return 0;
}
  ```
