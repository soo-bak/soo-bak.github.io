---
layout: single
title: "[백준 11575] Affine Cipher (C#, C++) - soo:bak"
date: "2025-04-19 22:51:00 +0900"
description: "아핀 암호 공식을 이용하여 입력된 문자열을 암호화하는 방식의 구현 문제인 백준 11575번 Affine Cipher 문제의 C# 및 C++ 풀이 및 해설"
tags:
  - 백준
  - BOJ
  - 11575
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 11575, 백준 11575번, BOJ 11575, affineCipher, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11575번 - Affine Cipher](https://www.acmicpc.net/problem/11575)

## 설명
**주어진 두 정수** `a`**,** `b`**와 알파벳 대문자로만 구성된 문자열에 대해**<br>
<br>
**아핀 암호 방식으로 암호문을 생성하는 문자열 변환 문제**입니다.<br>

<br>
<br>
암호화 공식은 다음과 같습니다:<br>

$$
E(x) = (a \times x + b) \bmod 26
$$
<br>
(`x`는 0부터 25까지의 정수, `'A'`를 0으로 매핑한 문자 인덱스를 의미)<br>

<br>
암호화된 정수는 다시 `0 → 'A', 1 → 'B', ..., 25 → 'Z'`로 변환됩니다.<br>

## 접근법

1. 테스트케이스 수 `T`를 입력받습니다.<br>
2. 각 테스트케이스마다 두 정수 `a`, `b`를 입력받고, 암호화할 문자열을 입력받습니다.<br>
3. 문자열의 각 문자를 다음 방식으로 변환합니다:<br>
  - 문자는 내부적으로 아스키(ASCII) 코드 값으로 처리되며, `'A'`의 아스키 값은 `65`입니다.
  - 각 문자는 `'A'`를 기준으로 정수값으로 변환합니다.
    (예: `'C'` - `'A'` 에서, `'C'`의 아스키 값은 `67`이므로 `67` - `65` = `2`)
  - 위의 암호화 공식을 적용한 후, 결과에 다시 `'A'`의 아스키 값을 더합니다.
  - 이때 `% 26` 연산을 통해 변환된 값이 알파벳 범위(0~25)를 넘지 않도록 조정합니다.
    이는 알파벳이 총 26글자이기 때문에 적용되는 모듈로 연산입니다.
  - 최종적으로 0 → 'A', 1 → 'B', ..., 25 → 'Z'와 같은 방식으로 다시 문자로 변환합니다.
4. 변환된 문자열을 출력합니다.<br>


## Code

[ C# ]

```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var tokens = Console.ReadLine().Split();
      int a = int.Parse(tokens[0]), b = int.Parse(tokens[1]);
      string str = Console.ReadLine();
      char[] arr = str.ToCharArray();

      for (int i = 0; i < arr.Length; i++)
        arr[i] = (char)((a * (arr[i] - 'A') + b) % 26 + 'A');

      Console.WriteLine(new string(arr));
    }
  }
}
```

[ C++ ]

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int a, b; cin >> a >> b;
    string str; cin >> str;

    for (size_t i = 0; i < str.size(); i++)
      str[i] = (a * (str[i] - 65) + b) % 26 + 65;
    cout << str << "\n";
  }

  return 0;
}
```
