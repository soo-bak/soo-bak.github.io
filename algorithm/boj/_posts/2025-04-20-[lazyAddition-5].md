---
layout: single
title: "[백준 8949] 대충 더해 (C#, C++) - soo:bak"
date: "2025-04-20 04:15:00 +0900"
description: 두 수를 자리수별로 더하여 각 자릿수마다 결과를 이어붙이는 방식으로 처리하는 백준 8949번 대충 더해 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[8949번 - 대충 더해](https://www.acmicpc.net/problem/8949)

## 설명
**두 개의 숫자를 같은 자리끼리 더해 그 결과를 이어붙이는 방식으로 새로운 수를 만드는 문제입니다.**
<br>

- 입력으로 두 수가 주어집니다.
- 각 자릿수를 일대일로 대응해 **자릿수끼리만 더한 값들을 그대로 이어붙인 문자열**을 출력합니다.
- 두 수의 길이가 다를 경우, 긴 수의 앞쪽 자릿수는 그대로 유지합니다.


## 접근법

1. 문자열로 입력된 두 수 중 길이가 더 긴 수를 기준으로 앞쪽 자릿수 차이를 계산합니다.
2. 길이 차이만큼 긴 수의 앞부분을 그대로 출력합니다.
3. 이후 남은 자릿수들은 각 수의 자릿수끼리 더한 값을 이어서 출력합니다.
4. 문자를 숫자로 바꾸기 위해 각 자리의 문자를 정수로 변환한 후 덧셈을 수행합니다.

- 문자열 인덱스를 정확히 맞추는 것이 중요합니다.
- 자리올림은 고려하지 않고 각 자릿수별 결과만 출력하면 됩니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    string l = input[0];
    string r = input[1];

    if (l.Length < r.Length) {
      var temp = l;
      l = r;
      r = temp;
    }

    int diff = l.Length - r.Length;
    Console.Write(l.Substring(0, diff));

    for (int i = 0; i < r.Length; i++) {
      int sum = (l[diff + i] - '0') + (r[i] - '0');
      Console.Write(sum);
    }
    Console.WriteLine();
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

  string l, r; cin >> l >> r;

  if (l.size() < r.size()) swap(l, r);

  size_t diff = l.size() - r.size();

  cout << l.substr(0, diff);

  for (size_t i = diff; i < l.size(); i++)
    cout << (l[i] - '0' + r[i - diff] - '0');
  cout << "\n";

  return 0;
}
```
