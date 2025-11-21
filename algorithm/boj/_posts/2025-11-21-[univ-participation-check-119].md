---
layout: single
title: "[백준 17388] 와글와글 숭고한 (C#, C++) - soo:bak"
date: "2025-11-21 23:27:00 +0900"
description: 세 대학 참여도 합이 100 이상이면 OK, 아니면 최소 참여 대학을 출력하는 백준 17388번 와글와글 숭고한 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[17388번 - 와글와글 숭고한](https://www.acmicpc.net/problem/17388)

## 설명

숭실, 고려, 한양 세 대학의 참여도 `S`, `K`, `H`가 주어집니다.<br>

세 참여도의 합이 `100` 이상이면 `"OK"`를 출력합니다. `100` 미만이면 참여도가 가장 낮은 대학 이름을 출력합니다.<br>

세 대학의 참여도는 모두 다른 값입니다.<br>

<br>

## 접근법

세 참여도의 합을 계산하여 `100` 이상이면 `"OK"`를 출력하고 종료합니다.<br>

합이 `100` 미만이면 세 값 중 최솟값을 찾아 해당하는 대학 이름을 출력합니다. 참여도가 모두 다르므로 최솟값은 유일합니다. `S`가 가장 작으면 `"Soongsil"`, `K`가 가장 작으면 `"Korea"`, `H`가 가장 작으면 `"Hanyang"`을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var tokens = Console.ReadLine()!.Split();
      var S = int.Parse(tokens[0]);
      var K = int.Parse(tokens[1]);
      var H = int.Parse(tokens[2]);

      var sum = S + K + H;
      if (sum >= 100) {
        Console.WriteLine("OK");
        return;
      }

      if (S < K && S < H) Console.WriteLine("Soongsil");
      else if (K < S && K < H) Console.WriteLine("Korea");
      else Console.WriteLine("Hanyang");
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

  int S, K, H; cin >> S >> K >> H;

  int sum = S + K + H;
  if (sum >= 100) {
    cout << "OK\n";
    return 0;
  }

  if (S < K && S < H) cout << "Soongsil\n";
  else if (K < S && K < H) cout << "Korea\n";
  else cout << "Hanyang\n";

  return 0;
}
```

