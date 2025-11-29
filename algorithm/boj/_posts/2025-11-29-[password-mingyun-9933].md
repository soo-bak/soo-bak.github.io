---
layout: single
title: "[백준 9933] 민균이의 비밀번호 (C#, C++) - soo:bak"
date: "2025-11-29 22:00:00 +0900"
description: 단어 목록에서 어떤 단어와 그 역순이 함께 존재하는 쌍을 찾아 길이와 가운데 문자를 출력하는 백준 9933번 민균이의 비밀번호 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[9933번 - 민균이의 비밀번호](https://www.acmicpc.net/problem/9933)

## 설명

여러 개의 단어가 주어지는 상황에서, N (2 ≤ N ≤ 100)개의 단어(길이 2~13의 홀수, 알파벳 소문자)가 주어질 때, 어떤 단어와 그 역순 단어가 모두 목록에 존재하는 경우 그 단어의 길이와 가운데 글자를 출력하는 문제입니다.

비밀번호는 자기 자신을 뒤집은 단어도 목록에 있는 단어이며, 답은 항상 유일하게 존재합니다. 예를 들어 "was"와 "saw"가 모두 목록에 있다면 둘 중 하나가 비밀번호입니다.

<br>

## 접근법

모든 단어를 집합(Set)에 저장하여 빠른 검색이 가능하도록 합니다.

각 단어에 대해 그 단어를 뒤집은 문자열을 만들고, 뒤집은 문자열이 집합에 존재하는지 확인합니다.

뒤집은 문자열이 집합에 있다면 그것이 비밀번호이므로, 해당 단어의 길이와 가운데 문자(길이가 홀수이므로 정확히 중앙에 위치)를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var words = new HashSet<string>();
      
      for (var i = 0; i < n; i++)
        words.Add(Console.ReadLine()!);

      foreach (var word in words) {
        var chars = word.ToCharArray();
        Array.Reverse(chars);
        var reversed = new string(chars);
        
        if (words.Contains(reversed)) {
          Console.WriteLine($"{word.Length} {word[word.Length / 2]}");
          return;
        }
      }
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

  int n; cin >> n;
  set<string> words;
  
  for (int i = 0; i < n; i++) {
    string word; cin >> word;
    words.insert(word);
  }

  for (const auto& word : words) {
    string reversed = word;
    reverse(reversed.begin(), reversed.end());
    
    if (words.find(reversed) != words.end()) {
      cout << word.length() << " " << word[word.length() / 2] << "\n";
      break;
    }
  }
  
  return 0;
}
```


