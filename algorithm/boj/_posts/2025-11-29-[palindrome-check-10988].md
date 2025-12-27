---
layout: single
title: "[백준 10988] 팰린드롬인지 확인하기 (C#, C++) - soo:bak"
date: "2025-11-29 22:00:00 +0900"
description: 주어진 소문자 문자열이 앞뒤가 같은 팰린드롬인지 확인해 1 또는 0을 출력하는 백준 10988번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 10988
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 10988, 백준 10988번, BOJ 10988, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10988번 - 팰린드롬인지 확인하기](https://www.acmicpc.net/problem/10988)

## 설명

소문자로만 이루어진 단어가 주어지는 상황에서, 단어(길이 1~100)가 주어질 때, 그 단어가 팰린드롬이면 1을, 아니면 0을 출력하는 문제입니다.

팰린드롬은 앞에서 읽으나 뒤에서 읽으나 같은 단어를 의미합니다. 예를 들어 "level", "noon", "a" 등이 팰린드롬입니다.

<br>

## 접근법

문자열의 양 끝에서 시작하여 중앙으로 이동하면서 대칭 위치의 문자들을 비교합니다.

첫 번째 문자와 마지막 문자, 두 번째 문자와 마지막에서 두 번째 문자를 비교하는 식으로 진행합니다.

한 번이라도 다른 문자가 발견되면 팰린드롬이 아니며, 중앙까지 모두 같으면 팰린드롬입니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var word = Console.ReadLine()!;
      var isPalindrome = true;
      
      for (var i = 0; i < word.Length / 2; i++) {
        if (word[i] != word[word.Length - i - 1]) {
          isPalindrome = false;
          break;
        }
      }
      
      Console.WriteLine(isPalindrome ? 1 : 0);
    }
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

  string word; cin >> word;

  bool isPalindrome = true;
  for (size_t i = 0; i < word.length() / 2; i++) {
    if (word[i] != word[word.length() - i - 1]) {
      isPalindrome = false;
      break;
    }
  }
  
  cout << (isPalindrome ? 1 : 0) << "\n";
  
  return 0;
}
```


