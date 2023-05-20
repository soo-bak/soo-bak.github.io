---
layout: single
title: "[백준 4459] Always Follow the Rules in Zombieland (C#, C++) - soo:bak"
date: "2023-05-20 08:56:00 +0900"
---

## 문제 링크
  [4459번 - Always Follow the Rules in Zombieland](https://www.acmicpc.net/problem/4459)

## 설명
문제에서 제시한 규칙에 따라서, 범위 내의 규칙 번호에 해당하는 문장을 출력하는 문제입니다. <br>

범위 외의 규칙 번호에 대해서는 `"No such rule"` 을 출력합니다. <br>

<br>
`C++` 에서는 `cin` 과 `getline()` 을 함께 사용하였는데, <br>

`cin` 은 공백, 탭, 개행 문자 등을 구분자로 사용하여 입력을 받고, 구분자는 버퍼에 남겨두게 됩니다. <br>

따라서, `cin.ignore()` 을 통해 버퍼를 지워주지 않으면, `getline()` 함수는 버퍼에 남아있는 개행 문자를 읽어들여 바로 종료되어 버립니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var q = int.Parse(Console.ReadLine()!);

      var quotes = new List<string>();
      for (int i = 0; i < q; i++)
        quotes.Add(Console.ReadLine()!);

      var r = int.Parse(Console.ReadLine()!);
      for (int i = 0; i < r; i++) {
        var ruleNum = int.Parse(Console.ReadLine()!);
        if (ruleNum > 0 && ruleNum <= q)
          Console.WriteLine($"Rule {ruleNum}: {quotes[ruleNum - 1]}");
        else Console.WriteLine($"Rule {ruleNum}: No such rule");
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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int q; cin >> q;
  cin.ignore();

  vector<string> quotes(q);
  for (int i = 0; i < q; i++)
    getline(cin, quotes[i]);

  int r; cin >> r;
  for (int i = 0; i < r; i++) {
    int ruleNum; cin >> ruleNum;
    if (ruleNum > 0 && ruleNum <= q)
      cout << "Rule " << ruleNum << ": " << quotes[ruleNum - 1] << "\n";
    else cout << "Rule " << ruleNum << ": No such rule\n";
  }

  return 0;
}
  ```
