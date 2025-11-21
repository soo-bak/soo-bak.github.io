---
layout: single
title: "[백준 20499] Darius님 한타 안 함? (C#, C++) - soo:bak"
date: "2025-11-21 23:27:00 +0900"
description: KDA 문자열을 파싱해 조건에 따라 gosu/hasu를 출력하는 백준 20499번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[20499번 - Darius님 한타 안 함?](https://www.acmicpc.net/problem/20499)

## 설명

게임 기록이 `K/D/A` 형식으로 주어집니다. `K`는 킬, `D`는 데스, `A`는 어시스트 수입니다.<br>

주어진 기록을 평가하여 `"hasu"` 또는 `"gosu"`를 출력하는 문제입니다.<br>

<br>

## 접근법

입력 문자열을 `/` 기준으로 분리하여 `K`, `D`, `A` 값을 얻습니다.<br>

평가 조건은 두 가지입니다. `D`가 `0`이면 `"hasu"`를 출력합니다.

또한 `K + A < D`인 경우도 `"hasu"`를 출력합니다.

두 조건 모두 해당하지 않으면 `"gosu"`를 출력합니다.<br>

예를 들어 `3/5/2`가 입력되면 `K + A = 3 + 2 = 5`이고 `D = 5`이므로 `K + A < D`가 거짓이며 `D ≠ 0`이므로 `"gosu"`를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var kda = Console.ReadLine()!.Split('/');
      var k = int.Parse(kda[0]);
      var d = int.Parse(kda[1]);
      var a = int.Parse(kda[2]);

      Console.WriteLine((k + a < d || d == 0) ? "hasu" : "gosu");
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

  string s; cin >> s;

  int k, d, a;
  char slash;
  stringstream ss(s);
  ss >> k >> slash >> d >> slash >> a;

  if (k + a < d || d == 0) cout << "hasu\n";
  else cout << "gosu\n";

  return 0;
}
```

