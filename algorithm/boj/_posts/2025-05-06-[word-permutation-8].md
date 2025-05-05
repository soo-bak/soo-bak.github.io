---
layout: single
title: "[백준 9081] 단어 맞추기 (C#, C++) - soo:bak"
date: "2025-05-06 08:00:00 +0900"
description: 주어진 단어의 다음 사전순 순열을 구하는 백준 9081번 단어 맞추기 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[9081번 - 단어 맞추기](https://www.acmicpc.net/problem/9081)

## 설명
단어가 주어졌을 때, **해당 단어의 알파벳들을 재배열하여 사전순으로 바로 다음에 오는 단어를 출력하는 문제**입니다.

<br>
예를 들어 `"BEER"`의 경우, 재조합하여 사전순으로 다음에 올 수 있는 단어는 `"BERE"`입니다.

만약 현재 단어가 마지막 사전순 조합이라면, **그대로 출력**합니다.

<br>

## 접근법
- 주어진 단어를 **다음 순열(next permutation)**로 바꾸는 문제입니다.
- 이를 위해 문자열에 대해 다음과 같은 과정을 진행합니다:
  1. **뒤에서부터** 현재 문자가 다음 문자보다 작아지는 지점을 찾습니다.
  2. 그 문자를 기준으로, **뒤쪽에서 가장 작은 큰 문자**를 찾아 교환합니다.
  3. 이후 **뒤쪽 문자열을 오름차순으로 정렬**합니다.
- 만약 위 조건을 만족하는 지점이 없다면, 해당 단어는 **사전순으로 가장 마지막 조합**이므로 변경 없이 그대로 출력합니다.

<br>
전형적인 **다음 순열을 구하기**문제입니다.

<br>
> 관련 문제: [[백준 10972] 다음 순열 (C#, C++) - soo:bak](https://soo-bak.github.io/algorithm/boj/next-permutation-41)
> 관련 문제: [[백준 10973] 이전 순열 (C#, C++) - soo:bak](https://soo-bak.github.io/algorithm/boj/prev-permutation-55)

<br>

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var s = Console.ReadLine().ToCharArray();
      int i = s.Length - 2;

      while (i >= 0 && s[i] >= s[i + 1])
        i--;

      if (i >= 0) {
        int j = s.Length - 1;
        while (s[j] <= s[i])
          j--;
        (s[i], s[j]) = (s[j], s[i]);
        Array.Reverse(s, i + 1, s.Length - i - 1);
      }

      Console.WriteLine(new string(s));
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

void nextPermutation(string& s) {
  int i = s.size() - 2;
  while (i >= 0 && s[i] >= s[i + 1])
    i--;
  if (i >= 0) {
    int j = s.size() - 1;
    while (s[j] <= s[i])
      j--;
    swap(s[i], s[j]);
    reverse(s.begin() + i + 1, s.end());
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    string s; cin >> s;
    nextPermutation(s);
    cout << s << "\n";
  }

  return 0;
}
```
