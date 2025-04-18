---
layout: single
title: "[백준 10808] 알파벳 개수 (C#, C++) - soo:bak"
date: "2025-04-19 00:14:10 +0900"
description: 입력된 문자열에서 소문자 알파벳의 개수를 각각 세어 출력하는 백준 10808번 알파벳 개수 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10808번 - 알파벳 개수](https://www.acmicpc.net/problem/10808)

## 설명
**입력된 문자열에 포함된 알파벳 소문자의 개수를 세어 알파벳 순서대로 출력하는 구현 문제**입니다.<br>
<br>

- 입력 문자열은 모두 소문자 알파벳으로만 구성되어 있습니다.<br>
- 알파벳 `'a'`부터 `'z'`까지 각각 몇 번 등장했는지를 `0`부터 시작하는 순서로 출력해야 합니다.<br>
- 공백으로 구분하여 `26`개의 정수를 출력합니다.<br>

### 접근법
- 알파벳의 아스키 코드를 이용해 각 알파벳을 고유한 인덱스로 변환합니다.<br>
- 각 인덱스 위치에 해당 알파벳의 개수를 저장할 배열을 선언하여 빈도수를 누적합니다.<br>
- 문자열을 끝까지 순회하며 등장한 각 문자의 개수를 모두 센 후, 알파벳 순서대로 차례로 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    var counts = new int[26];
    var input = Console.ReadLine();

    foreach (char c in input)
      counts[c - 'a']++;

    Console.WriteLine(string.Join(" ", counts));
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int sieve[26] = {0};
  string str; cin >> str;
  for (size_t i = 0; i < str.size(); i++)
    sieve[str[i] - 'a']++;
  for (int i = 0; i < 26; i++)
    cout << sieve[i] << " ";
  cout << "\n";

  return 0;
}
```
