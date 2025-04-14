---
layout: single
title: "[백준 10569] 다면체 (C#, C++) - soo:bak"
date: "2025-04-14 20:25:24 +0900"
description: 오일러의 정리를 활용하여 면의 개수를 계산하는 백준 10569번 다면체 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[10569번 - 다면체](https://www.acmicpc.net/problem/10569)

## 설명
이 문제는 **오일러의 정리(Euler's formula)**를 이용하여,  <br>
주어진 정점과 간선 개수로부터 **면(Face)의 개수를 계산하는 문제**입니다.

오일러의 정리에 따르면:

$$
V - E + F = 2
$$

여기서 `V`는 정점(Vertex), `E`는 간선(Edge), `F`는 면(Face)입니다. <br>
따라서 다음과 같이 유도할 수 있습니다:

$$
F = 2 - V + E
$$

---

## 접근법
- 테스트 케이스마다 `V`와 `E`를 입력받고,
- 위 식에 따라 `F = 2 - V + E`를 계산하여 출력합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      int t = int.Parse(Console.ReadLine()!);
      while (t-- > 0) {
        var parts = Console.ReadLine()!.Split();
        int v = int.Parse(parts[0]);
        int e = int.Parse(parts[1]);
        Console.WriteLine(2 - v + e);
      }
    }
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

  int n; cin >> n;
  while (n--) {
    int vertex, edge; cin >> vertex >> edge;
    cout << 2 + edge - vertex << "\n";
  }

  return 0;
}
```
