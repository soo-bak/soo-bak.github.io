---
layout: single
title: "[백준 1919] 애너그램 만들기 (C#, C++) - soo:bak"
date: "2025-05-18 02:18:59 +0900"
description: 두 문자열을 애너그램으로 만들기 위한 문자 제거 최소 횟수를 계산하는 백준 1919번 애너그램 만들기 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[1919번 - 애너그램 만들기](https://www.acmicpc.net/problem/1919)

## 설명

**두 단어가 애너그램 관계가 되도록 만들기 위해 삭제해야 하는 최소 문자의 수를 계산하는 문제입니다.**

애너그램이란, 두 단어가 **같은 문자 구성**을 가지되 **순서만 다른 상태**를 의미합니다.

예를 들어 `listen`과 `silent`, `triangle`과 `integral`은 서로 애너그램입니다.

<br>

주어진 두 문자열을 대상으로, 두 단어가 **동일한 문자 빈도수**를 가지도록 만들기 위해

각 문자열에서 **몇 개의 문자를 삭제해야 하는지**를 계산합니다.

---

## 접근법

이 문제의 핵심은 **문자의 개수 차이만큼 삭제하면 된다**는 점입니다.

- 알파벳 소문자는 `26개`이므로, 각 문자열에 대해 **알파벳 빈도수 배열**을 만듭니다.
- 같은 알파벳에 대해, 두 문자열의 빈도수 차이를 구합니다.
- 이 차이들의 총합이 바로, **삭제해야 할 문자의 총 수**가 됩니다.

<br>

구체적인 과정은 다음과 같습니다:

1. 각 문자열에 대해 알파벳 빈도 수를 배열에 저장합니다.
2. 인덱스 `0`부터 `25`까지 순회하면서 각 알파벳에 대해 등장 횟수 차이를 구합니다.
3. 이 차이값들을 모두 더하면, 두 문자열을 애너그램으로 만들기 위해 필요한 **삭제 횟수의 최소값**이 됩니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string s1 = Console.ReadLine();
    string s2 = Console.ReadLine();

    int[] count1 = new int[26];
    int[] count2 = new int[26];

    foreach (char c in s1) count1[c - 'a']++;
    foreach (char c in s2) count2[c - 'a']++;

    int ans = 0;
    for (int i = 0; i < 26; i++)
      ans += Math.Abs(count1[i] - count2[i]);

    Console.WriteLine(ans);
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

  string s1, s2; cin >> s1 >> s2;
  int count1[26] = {}, count2[26] = {};
  for (char c : s1) ++count1[c - 'a'];
  for (char c : s2) ++count2[c - 'a'];

  int ans = 0;
  for (int i = 0; i < 26; ++i)
    ans += abs(count1[i] - count2[i]);

  cout << ans << "\n";

  return 0;
}
```
