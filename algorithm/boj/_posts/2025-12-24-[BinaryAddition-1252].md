---
layout: single
title: "[백준 1252] 이진수 덧셈 (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: 두 이진 문자열을 직접 더해 결과 이진수를 만드는 문제
---

## 문제 링크
[1252번 - 이진수 덧셈](https://www.acmicpc.net/problem/1252)

## 설명
길이가 최대 80인 두 이진수를 더해 결과를 출력하는 문제입니다.

<br>

## 접근법
두 문자열을 뒤에서부터 한 자리씩 더하며 올림을 관리합니다.

이후 남은 올림까지 처리하고, 앞쪽의 불필요한 0을 제거한 뒤 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var a = parts[0];
    var b = parts[1];

    var i = a.Length - 1;
    var j = b.Length - 1;
    var carry = 0;
    var sb = new StringBuilder();

    while (i >= 0 || j >= 0 || carry > 0) {
      var sum = carry;
      if (i >= 0) sum += a[i--] - '0';
      if (j >= 0) sum += b[j--] - '0';
      sb.Append((char)('0' + (sum % 2)));
      carry = sum / 2;
    }

    var res = sb.ToString().TrimEnd('0');
    if (res.Length == 0) Console.WriteLine("0");
    else {
      var arr = res.ToCharArray();
      Array.Reverse(arr);
      Console.WriteLine(new string(arr));
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

  string a, b; cin >> a >> b;
  int i = (int)a.size() - 1;
  int j = (int)b.size() - 1;
  int carry = 0;
  string res;

  while (i >= 0 || j >= 0 || carry > 0) {
    int sum = carry;
    if (i >= 0) sum += a[i--] - '0';
    if (j >= 0) sum += b[j--] - '0';
    res.push_back(char('0' + (sum % 2)));
    carry = sum / 2;
  }

  while (res.size() > 1 && res.back() == '0')
    res.pop_back();
  reverse(res.begin(), res.end());
  cout << res << "\n";

  return 0;
}
```
