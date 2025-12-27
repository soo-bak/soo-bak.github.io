---
layout: single
title: "[백준 9012] 괄호 (C#, C++) - soo:bak"
date: "2024-12-13 01:03:00 +0900"
description: 자료구조, 문자열, 스택을 활용한 백준 9012번 문제를 C#과 C++로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9012
  - C#
  - C++
  - 알고리즘
  - 자료구조
  - 문자열
  - 스택
keywords: "백준 9012, 백준 9012번, BOJ 9012, RoundBracket, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [9012번 - 괄호](https://www.acmicpc.net/problem/9012)

## 설명
괄호 문자열이 올바른지 확인하는 문제입니다.<br>
<br>
문자열은 `(` 와 `)` 만으로 구성되며, 괄호의 짝이 맞으면 올바른 괄호 문자열(VPS) 이라고 합니다.<br>
<br>

### 올바른 괄호 문자열(VPS)의 조건
1. 여는 괄호 `(` 가 닫는 괄호 `)`보다 먼저 나와야 합니다.<br>
2. 모든 괄호가 짝이 맞아야 합니다.<br>
3. 중간에 닫는 괄호가 여는 괄호보다 많아지면 VPS가 아닙니다.<br>
<br>
예를 들어:<br>
<br>
`(()())` → YES (올바른 VPS)<br>
<br>
`())(` → NO (짝이 맞지 않음)<br>
<br>
`((()` → NO (여는 괄호가 남음)<br>
<br>

### 접근법
문제 해결을 위해 **스택(Stack)** 자료구조를 사용합니다.<br>
<br>

1. 문자열을 한 글자씩 확인합니다.<br>
2. 여는 괄호 (를 만나면 스택에 저장합니다.<br>
3. 닫는 괄호 )를 만나면 스택에서 하나를 꺼냅니다.<br>
4. 닫는 괄호가 나왔는데 스택이 비어있으면 VPS가 아닙니다.<br>
5. 문자열을 모두 확인한 후 스택이 비어있으면 VPS입니다.<br>
<br>

### 풀이과정 예시
문자열: `"(())()"`<br>
- `(` → 스택: `[()]`<br>
- `(` → 스택: `[(, ()]`<br>
- `)` → 스택에서 `( 제거 → [()]`<br>
- `)` → 스택에서 `(` 제거 → 스택: `[]`<br>
- `(` → 스택: `[()]`<br>
- `)` → 스택에서 `(` 제거 → 스택: `[]`<br>
<br>
최종적으로 스택이 비어 있으므로 VPS입니다. (`YES`)

<br>
<br>
<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Solution {
  class Program {

    static void Main(string[] args) {

      var sb = new StringBuilder();
      var t = int.Parse(Console.ReadLine()!);

      Enumerable.Range(0, t).ToList()
        .ForEach(_ => {
          var str = Console.ReadLine()!;
          var stack = new Stack<char>();
          var isValid = true;

          foreach (char ch in str) {
            if (ch == '(') stack.Push(ch);
            if (ch == ')') {
              if (stack.Count == 0) { isValid = false; break; }
              else stack.Pop();
            }
          }

          sb.AppendLine(isValid && stack.Count == 0 ? "YES" : "NO");
        });

      Console.Write(sb);
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
typedef stack<char> stc;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    string str; cin >> str;

    stc s;
    bool isValid = true;
    for (size_t i = 0; i < str.length(); i++) {
      if (str[i] == '(') s.push(str[i]);
      if (str[i] == ')') {
        if (s.empty()) isValid = false;
        else s.pop();
      }
    }
    if (isValid && s.empty()) cout << "YES\n";
    else cout << "NO\n";
  }

  return 0;
}
  ```
