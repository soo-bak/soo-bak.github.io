---
layout: single
title: "[백준 16462] '나교수' 교수님의 악필 (C#, C++) - soo:bak"
date: "2025-12-25 14:56:00 +0900"
description: 점수의 0, 6, 9를 9로 바꾸고 100점을 넘기면 100으로 처리한 뒤 평균을 반올림하는 문제
---

## 문제 링크
[16462번 - '나교수' 교수님의 악필](https://www.acmicpc.net/problem/16462)

## 설명
각 점수에서 0, 6, 9를 9로 바꾸고 100을 넘는 경우는 100으로 처리한 뒤 평균을 구하는 문제입니다.

<br>

## 접근법
각 점수를 문자열로 읽어 0, 6, 9를 9로 치환한 뒤 정수로 변환합니다.  

점수가 100을 넘으면 100으로 고정하고 합계를 구한 후, `sum / N`을 반올림해 출력합니다.  

반올림은 `remainder * 2 >= N`일 때 올려서 처리합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var sum = 0;

    for (var i = 0; i < n; i++) {
      var s = Console.ReadLine()!;
      var arr = s.ToCharArray();
      for (var j = 0; j < arr.Length; j++) {
        if (arr[j] == '0' || arr[j] == '6' || arr[j] == '9')
          arr[j] = '9';
      }

      var v = int.Parse(new string(arr));
      if (v > 100) v = 100;
      sum += v;
    }

    var avg = sum / n;
    if ((sum % n) * 2 >= n) avg++;
    Console.WriteLine(avg);
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
  int sum = 0;

  for (int i = 0; i < n; i++) {
    string s; cin >> s;
    for (char& ch : s) {
      if (ch == '0' || ch == '6' || ch == '9') ch = '9';
    }

    int v = stoi(s);
    if (v > 100) v = 100;
    sum += v;
  }

  int avg = sum / n;
  if ((sum % n) * 2 >= n) avg++;
  cout << avg << "\n";

  return 0;
}
```
