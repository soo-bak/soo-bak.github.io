---
layout: single
title: "[백준 10886] 0 = not cute / 1 = cute (C#, C++) - soo:bak"
date: "2025-11-15 00:45:00 +0900"
description: 설문 결과에서 0과 1의 개수를 비교해 메시지를 출력하는 백준 10886번 0 = not cute / 1 = cute 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[10886번 - 0 = not cute / 1 = cute](https://www.acmicpc.net/problem/10886)

## 설명

`N`명의 사람들이 준희가 귀여운지 투표한 결과를 받아 판정하는 문제입니다.<br>

`1`은 귀엽다는 의견이고, `0`은 귀엽지 않다는 의견입니다.<br>

더 많은 표를 받은 쪽에 따라 결과 메시지를 출력합니다.<br>

`N`은 홀수이므로 동점은 발생하지 않습니다.<br>

<br>

## 접근법

카운팅을 사용하여 해결합니다.

`N`개의 투표 결과를 입력받으면서 `1`의 개수와 `0`의 개수를 각각 카운트합니다.

모든 입력을 받은 후, `1`의 개수가 더 많으면 `"Junhee is cute!"`를, `0`의 개수가 더 많으면 `"Junhee is not cute!"`를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var cute = 0;
      var notCute = 0;
      for (var i = 0; i < n; i++) {
        if (int.Parse(Console.ReadLine()!) == 1) cute++;
        else notCute++;
      }

      Console.WriteLine(cute > notCute ? "Junhee is cute!" : "Junhee is not cute!");
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
  int cute = 0, notCute = 0;
  while (n--) {
    int vote; cin >> vote;
    if (vote) ++cute;
    else ++notCute;
  }

  if (cute > notCute) cout << "Junhee is cute!\n";
  else cout << "Junhee is not cute!\n";

  return 0;
}
```

