---
layout: single
title: "[백준 5218] 알파벳 거리 (C#, C++) - soo:bak"
date: "2025-04-19 00:14:10 +0900"
description: 두 문자열의 각 문자 간 알파벳 거리 차이를 계산하여 출력하는 백준 5218번 알파벳 거리 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[5218번 - 알파벳 거리](https://www.acmicpc.net/problem/5218)

## 설명
**두 문자열이 주어졌을 때, 각 자리의 문자 간 알파벳 거리 차이를 계산하여 출력하는 구현 문제**입니다.<br>
<br>

- 입력으로 두 개의 소문자 문자열이 주어집니다. 두 문자열의 길이는 항상 같습니다.<br>
- 각 자리에서 첫 번째 문자열의 문자가 두 번째 문자열의 문자로 바뀌기 위해 몇 글자를 지나야 하는지를 계산합니다.<br>
- 알파벳이 원형으로 이어진다고 가정하여, 두 번째 문자가 첫 번째 문자보다 앞에 있는 경우에는 `26`을 더해 거리 차이를 계산합니다.<br>

### 접근법
- 문자열을 끝까지 순회하며 각 자리 문자 쌍의 알파벳 순서 차이를 계산합니다.<br>
- 차이가 음수인 경우에는 원형 순서를 고려해 `26`을 더해 계산합니다.<br>
- 결과는 `"Distances: "` 다음에 각 위치별 거리 값을 공백으로 구분하여 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var input = Console.ReadLine().Split();
      string first = input[0], second = input[1];

      Console.Write("Distances: ");
      for (int i = 0; i < first.Length; i++) {
        int distance = second[i] - first[i];
        if (distance < 0) distance += 26;
        Console.Write(distance);
        if (i != first.Length - 1) Console.Write(" ");
      }
      Console.WriteLine();
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

  int t; cin >> t;
  while (t--) {
    string first, second; cin >> first >> second;
    cout << "Distances: ";
    for (size_t i = 0; i < first.size(); i++) {
      int distance;
      if (second[i] >= first[i])
        distance = second[i] - first[i];
      else
        distance = second[i] + 26 - first[i];
      cout << distance;
      if (i != first.size() - 1) cout << " ";
      else cout << "\n";
    }
  }

  return 0;
}
```
