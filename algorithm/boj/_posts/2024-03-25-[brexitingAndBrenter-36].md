---
layout: single
title: "[백준 25246] Brexiting and Brentering (C#, C++) - soo:bak"
date: "2024-03-25 23:27:00 +0900"
description: 구현, 문자열 등을 주제로 하는 백준 25246번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [25246번 - Brexiting and Brentering](https://www.acmicpc.net/problem/25246)

## 설명
입력으로 주어지는 사람, 조직, 나라 등의 주체가 '어딘가로 들어가는 행위'를 표준화된 명명 방식으로 명명하는 문제입니다.<br>
<br>
즉, 주어진 문자열을 특정 조건에 따라서 변환하는 문제입니다.<br>
<br>
변환 조건은, 주체 이름의 마지막 모음(`'a'`, `'e'`, `'i'`, `'o'`, `'u'`) 뒤의 모든 문자를 잘라내고, 대신 `"ntry"` 를 붙이는 것입니다.<br>
<br>
에를 들어, `"Britain"` 이 유럽 연합에 다시 들어간다면, 그 행위는 표준화된 명명 방식으로 `"Britaintry"` 라고 지어집니다.<br>

<br>
<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    static string FormEntryWord(string subject) {
      char[] vowels = { 'a', 'e', 'i', 'o', 'u'};

      var index = subject.Select((c, i) => new {Char = c, Index = i})
        .Where(x => vowels.Contains(x.Char))
        .Select(x => (int?)x.Index)
        .LastOrDefault();

      return index != null ? string.Concat(subject.AsSpan(0, index.Value + 1), "ntry") : "";
    }

    static void Main(string[] args) {

      var subject = Console.ReadLine()!;

      Console.WriteLine(FormEntryWord(subject));

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

string formEntryWord(const string& subject) {
  for (int i = subject.size() - 1; i >= 0; i--) {
    if (subject[i] == 'a' || subject[i] == 'e' || subject[i] == 'i' || subject[i] == 'o' || subject[i] == 'u')
      return subject.substr(0, i + 1) + "ntry";
  }
  return "";
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string subject; cin >> subject;

  cout << formEntryWord(subject) << "\n";

  return 0;
}
  ```
