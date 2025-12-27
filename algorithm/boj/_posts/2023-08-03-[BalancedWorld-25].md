---
layout: single
title: "[백준 4949] 균형잡힌 세상 (C#, C++) - soo:bak"
date: "2023-08-03 15:22:00 +0900"
description: 스택, 문자열, 구현 등을 주제로 하는 백준 4949번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 4949
  - C#
  - C++
  - 알고리즘
  - 자료구조
  - 문자열
  - 스택
keywords: "백준 4949, 백준 4949번, BOJ 4949, BalancedWorld, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [4949번 - 균형잡힌 세상](https://www.acmicpc.net/problem/4949)

## 설명
주어진 문자열이 균형잡힌 괄호를 가지고 있는지를 판별하는 문제입니다. <br>
<br>
주어진 규칙에 따라서 각 괄호는 적절하게 열리고 닫혀야 하며, 소괄호와 대괄호는 각각 짝을 이뤄야 합니다.<br>
<br>
이에 대한 판별을 위해 `스택` 자료구조를 사용합니다.<br>
<br>
풀이 과정은 다음과 같습니다.<br>
<br>
1. 먼저, 각 줄을 읽어들입니다. 마지막 줄은 항상 `'.'` 입니다.<br>
2. 각 문자열을 순회하며 괄호를 찾습니다.<br>
3. 여는 괄호를 발견하면 스택에 넣습니다.<br>
4. 닫는 괄호를 발견하면 스택에서 가장 최근에 추가된 여는 괄호를 꺼냅니다.<br>
5. 이 때, 여는 괄호가 스택에 존재하며, 현재의 닫는 괄호와 짝을 이룰 수 있다면 계속해서 진행합니다.<br>
6. 만약, 그렇지 않다면 이 문자열은 균형잡힌 괄호를 가지고 있지 않다는 것을 의미합니다.<br>
7. 문자열의 끝에 도달했을 때 스택이 비어있어야 합니다. 만약, 스택에 남아있는 괄호가 있다면 이 문자열은 균형잡힌 괄호를 가지고 있지 않습니다.<br>
8. 위의 과정을 모든 문자열에 대하여 반복합니다.<br>
<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      while (true) {
        var str = Console.ReadLine()!;

        if (str.Length == 1 && str[0] == '.') break ;

        bool isPaired = true;
        var stack = new Stack<char>();
        foreach (var c in str) {
          if (c == '(' || c == '[')
            stack.Push(c);

          if (c == ')') {
            if (stack.Count == 0 || stack.Peek() == '[')
              isPaired = false;
            else stack.Pop();
          }

          if (c == ']') {
            if (stack.Count == 0 || stack.Peek() == '(')
              isPaired = false;
            else stack.Pop();
          }
        }

        if (stack.Count == 0 && isPaired)
          Console.WriteLine("yes");
        else Console.WriteLine("no");
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

  while (true) {
    string str; getline(cin, str);

    if (str.length() == 1 && str[0] == '.') break ;

    bool isPaired = true;
    stack<char> s;
    for (size_t i = 0; i < str.length(); i++) {
      if (str[i] == '(' || str[i] == '[')
        s.push(str[i]);

      if (str[i] == ')') {
        if (s.empty() || s.top() == '[') isPaired = false;
        else s.pop();
      }

      if (str[i] == ']') {
        if (s.empty() || s.top() == '(') isPaired = false;
        else s.pop();
      }
    }
    if (s.empty() && isPaired) cout << "yes\n";
    else cout << "no\n";
  }

  return 0;
}
  ```
