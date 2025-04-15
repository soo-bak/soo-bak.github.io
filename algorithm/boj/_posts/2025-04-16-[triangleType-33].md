---
layout: single
title: "[백준 5073] 삼각형과 세 변 (C#, C++) - soo:bak"
date: "2025-04-16 01:57:00 +0900"
description: 세 변의 길이를 통해 삼각형의 성립 여부와 종류를 판별하는 백준 5073번 삼각형과 세 변 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[5073번 - 삼각형과 세 변](https://www.acmicpc.net/problem/5073)

## 설명
**세 변의 길이를 통해 삼각형이 가능한지 판별하고, 그에 따라 삼각형의 종류를 판단하는 조건 분기 문제**입니다.<br>
<br>

- 세 변의 길이를 입력받아, 삼각형이 될 수 있는 조건을 만족하는지 확인해야 합니다.<br>
- 삼각형이 되기 위해서는 가장 긴 변의 길이가 나머지 두 변의 합보다 작아야 합니다.<br>
- 삼각형이 될 수 있다면, 변의 길이에 따라 세 가지 중 하나로 분류합니다:<br>
  - 세 변이 모두 같으면 `Equilateral`<br>
  - 두 변만 같으면 `Isosceles`<br>
  - 모두 다르면 `Scalene`<br>
- 세 변이 모두 0인 경우 입력이 종료됩니다.<br>

### 접근법
- `3`개의 정수를 입력받아 리스트 형태로 저장하고, 오름차순 정렬합니다.<br>
- 가장 긴 변이 다른 두 변의 합보다 크거나 같으면 삼각형이 될 수 없으므로 `"Invalid"`를 출력합니다.<br>
- 그렇지 않은 경우 변들의 동일 개수를 세어 삼각형의 종류를 판단합니다.<br>
- 이 과정을 입력이 `0 0 0`이 나올 때까지 반복합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    while (true) {
      var tri = Console.ReadLine().Split().Select(int.Parse).ToArray();
      if (tri.All(x => x == 0)) break;

      Array.Sort(tri);

      if (tri[2] >= tri[0] + tri[1]) {
        Console.WriteLine("Invalid");
        continue;
      }

      var distinctCount = tri.Distinct().Count();
      if (distinctCount == 1)
        Console.WriteLine("Equilateral");
      else if (distinctCount == 2)
        Console.WriteLine("Isosceles");
      else
        Console.WriteLine("Scalene");
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
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  while (true) {
    vi tri(3);
    for (int i = 0; i < 3; i++)
      cin >> tri[i];
    if (!tri[0] && !tri[1] && !tri[2]) break ;

    sort(tri.begin(), tri.end());

    int cnt = 0;
    for (int i = 1; i < 3; i++)
      if (tri[i] == tri[i - 1]) cnt++;

    if (tri[2] >= tri[0] + tri[1]) cout << "Invalid\n";
    else {
      if (!cnt) cout << "Scalene\n";
      else if (cnt == 1) cout << "Isosceles\n";
      else if (cnt == 2) cout << "Equilateral\n";
    }
  }

  return 0;
}
```
