---
layout: single
title: "[백준 15814] 야바위 대장 (C#, C++) - soo:bak"
date: "2025-12-24 22:35:00 +0900"
description: 주어진 인덱스 쌍을 순서대로 swap하는 문자열 처리 문제
---

## 문제 링크
[15814번 - 야바위 대장](https://www.acmicpc.net/problem/15814)

## 설명
문자열에서 지정된 두 위치의 문자를 T번 교환한 뒤 결과를 출력하는 문제입니다.

<br>

## 접근법
문자열을 문자 배열로 바꾸고, 각 쿼리마다 두 인덱스의 문자를 swap 합니다.

모든 교환을 수행한 뒤 배열을 문자열로 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    var t = int.Parse(Console.ReadLine()!);
    var arr = s.ToCharArray();

    for (var i = 0; i < t; i++) {
      var parts = Console.ReadLine()!.Split();
      var a = int.Parse(parts[0]);
      var b = int.Parse(parts[1]);
      var tmp = arr[a];
      arr[a] = arr[b];
      arr[b] = tmp;
    }

    Console.WriteLine(new string(arr));
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

  string s; cin >> s;
  int t; cin >> t;
  for (int i = 0; i < t; i++) {
    int a, b; cin >> a >> b;
    swap(s[a], s[b]);
  }

  cout << s << "\n";

  return 0;
}
```
