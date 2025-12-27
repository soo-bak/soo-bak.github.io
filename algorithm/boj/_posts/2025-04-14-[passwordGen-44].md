---
layout: single
title: "[백준 1759] 암호 만들기 (C#, C++) - soo:bak"
date: "2025-04-14 04:40:20 +0900"
description: 최소 조건을 만족하는 조합을 사전 순으로 출력하는 백준 1759번 암호 만들기 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1759
  - C#
  - C++
  - 알고리즘
  - 수학
  - 브루트포스
  - 조합론
  - 백트래킹
keywords: "백준 1759, 백준 1759번, BOJ 1759, passwordGen, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1759번 - 암호 만들기](https://www.acmicpc.net/problem/1759)

## 설명
이 문제는 주어진 알파벳 중에서 `L`개의 문자를 선택하여,  <br>
**최소 1개의 모음**과 **최소 2개의 자음**을 포함하고  <br>
**사전 순으로 증가하는 암호**들을 전부 출력하는 문제입니다.

---

## 접근법
- 백트래킹(DFS)을 사용하여 가능한 조합을 모두 탐색합니다.
- 현재 선택된 문자 수가 `L`과 같아지면, 모음과 자음 개수를 검사합니다.
- 조건을 만족하는 조합만 출력하며, 사전 순 출력을 위해 알파벳을 정렬한 후 탐색을 시작합니다.
- 각 단계에서는 `현재 인덱스보다 큰 인덱스만 탐색`하여 중복 없이 증가하는 순서를 유지합니다.

<br>
> 참고 : [백트래킹(Backtracking)의 개념과 구조적 사고 - soo:bak](https://soo-bak.github.io/algorithm/theory/backTracking/)

<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

namespace Solution {
  class Program {
    static int l, c;
    static List<char> alpha = new();
    static readonly HashSet<char> vowels = new() { 'a', 'e', 'i', 'o', 'u' };

    static void Main(string[] args) {
      var input = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
      l = input[0]; c = input[1];

      alpha = Console.ReadLine()!.Split().Select(char.Parse).ToList();
      alpha.Sort();

      for (int i = 0; i <= c - l; i++)
        Dfs(alpha[i].ToString(), i, 1);
    }

    static void Dfs(string pwd, int idx, int depth) {
      if (depth == l) {
        int cntV = pwd.Count(ch => vowels.Contains(ch));
        int cntC = pwd.Length - cntV;
        if (cntV >= 1 && cntC >= 2)
          Console.WriteLine(pwd);
        return;
      }

      for (int i = idx + 1; i <= c - (l - depth); i++)
        Dfs(pwd + alpha[i], i, depth + 1);
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

int lenPwd, numApb;
vector<char> alpha;

bool isVowel(const char& c) {
  if (c == 'a' || c == 'e' || c == 'i' || c == 'o' ||
      c == 'u') return true;
  return false;
}

void dfs(string pwd, int now, int depth) {
  if (depth == lenPwd) {
    int cntV = 0, cntC = 0;
    for (int i = 0; i < lenPwd; i++) {
      if (isVowel(pwd[i])) cntV++;
      else cntC++;
    }
    if (cntV >= 1 && cntC >= 2) cout << pwd + "\n";
    return ;
  }

  for (int i = now + 1; i <= numApb - lenPwd + depth; i++)
    dfs(pwd + alpha[i], i, depth + 1);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  cin >> lenPwd >> numApb;
  for (int i = 0; i < numApb; i++) {
    char input; cin >> input;
    alpha.push_back(input);
  }

  sort(alpha.begin(), alpha.end());

  string pwd = "";
  for (int i = 0; i <= numApb - lenPwd; i++)
    dfs(pwd + alpha[i], i, 1);

  return 0;
}
```
