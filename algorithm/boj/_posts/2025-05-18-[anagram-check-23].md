---
layout: single
title: "[백준 6996] 애너그램 (C#, C++) - soo:bak"
date: "2025-05-18 02:21:21 +0900"
description: 주어진 두 단어가 알파벳 구성으로 애너그램인지 판단하는 백준 6996번 애너그램 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[6996번 - 애너그램](https://www.acmicpc.net/problem/6996)

## 설명

**두 단어가 서로 애너그램 관계인지 판별하는 문제입니다.**

애너그램이란, **같은 문자 구성**을 가지되 **순서만 다른** 두 단어를 말합니다.

예를 들어 `listen`과 `silent`, `triangle`과 `integral`은 애너그램입니다.

<br>
각 테스트케이스마다 두 단어가 주어졌을 때, 두 단어의 알파벳 구성만을 기준으로

애너그램인지 여부를 출력 형식에 맞추어 판별합니다.

---

## 접근법

문자열의 알파벳 빈도만 같으면 애너그램이므로, 다음과 같은 방식으로 확인합니다:

- 알파벳 소문자만 등장하므로 `a`부터 `z`까지 `26개`의 문자를 대상으로<br>
  **각 단어에 등장하는 알파벳 빈도 수 배열**을 각각 구성합니다.
- 두 배열을 비교하여 모든 문자의 등장 횟수가 같다면 애너그램입니다.
- 순서는 중요하지 않기 때문에 **정렬은 필요하지 않으며**,<br>
  **등장 횟수 기반의 비교만으로 충분히 판별할 수 있습니다.**

<br>

출력 형식은 다음과 같이 구성됩니다:

```
s1 & s2 are anagrams.
```

또는

```
s1 & s2 are NOT anagrams.
```

이때 `s1`, `s2`는 입력된 문자열 그대로 출력에 사용됩니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var parts = Console.ReadLine().Split();
      string s1 = parts[0], s2 = parts[1];
      int[] count1 = new int[26], count2 = new int[26];

      foreach (char c in s1) count1[c - 'a']++;
      foreach (char c in s2) count2[c - 'a']++;

      bool isAnagram = true;
      for (int i = 0; i < 26; i++) {
        if (count1[i] != count2[i]) {
          isAnagram = false;
          break;
        }
      }

      Console.WriteLine($"{s1} & {s2} are {(isAnagram ? "" : "NOT ")}anagrams.");
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

  int t; cin >> t;
  while (t--) {
    string s1, s2; cin >> s1 >> s2;

    int count1[26] = {}, count2[26] = {};
    for (char c : s1) ++count1[c - 'a'];
    for (char c : s2) ++count2[c - 'a'];

    bool isAnagram = true;
    for (int i = 0; i < 26; ++i) {
      if (count1[i] != count2[i]) {
        isAnagram = false;
        break;
      }
    }

    cout << s1 << " & " << s2 << " are " << (isAnagram ? "" : "NOT ") << "anagrams.\n";
  }

  return 0;
}
```
