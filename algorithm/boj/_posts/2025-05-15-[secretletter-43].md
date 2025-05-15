---
layout: single
title: "[백준 5426] 비밀 편지 (C#, C++) - soo:bak"
date: "2025-05-15 04:23:00 +0900"
description: 정사각형 회전을 통한 암호문 해독 과정을 구현하는 백준 5426번 비밀 편지 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[5426번 - 비밀 편지](https://www.acmicpc.net/problem/5426)

## 설명

**정사각형으로 배열된 암호문을** `90도` **회전하여 원래의 문장을 복원하는 문제입니다.**

편지의 암호화 방식은 다음과 같은 절차를 따릅니다:

- 평문을 위에서 아래로, 왼쪽에서 오른쪽 순서로 정사각형에 채웁니다.
- 이후 이 정사각형을 시계방향으로 90도 회전합니다.
- 회전된 정사각형을 위에서 아래로, 왼쪽에서 오른쪽 순으로 읽은 문자열이 암호문이 됩니다.

이 과정을 반대로 수행하여, 주어진 암호문으로부터 원래 편지의 내용을 복원해야 합니다.

<br>

## 접근법

암호화 과정을 역으로 따라가면, 다음과 같은 방식으로 복호화를 구현할 수 있습니다:

- 암호문의 길이는 항상 정사각형이므로, 문자열의 길이 `L`에 대해 $$\sqrt{L} \times \sqrt{L}$$ 크기의 격자를 구성할 수 있습니다.
- 암호문을 위에서 아래로, 왼쪽에서 오른쪽 순서로 격자에 채워넣습니다.
- 이후 열을 기준으로 오른쪽에서 왼쪽으로, 위에서 아래로 읽으면 원래의 평문이 됩니다.

이 작업을 각 테스트케이스마다 반복하여 복원된 문자열을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      string s = Console.ReadLine();
      int n = (int)Math.Sqrt(s.Length);
      char[,] grid = new char[n, n];

      int k = 0;
      for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
          grid[i, j] = s[k++];

      var sb = new StringBuilder();
      for (int j = n - 1; j >= 0; j--)
        for (int i = 0; i < n; i++)
          sb.Append(grid[i, j]);

      Console.WriteLine(sb.ToString());
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<char> vc;
typedef vector<vc> vvc;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    string s; cin >> s;

    int n = sqrt(s.size());
    vvc grid(n, vc(n));
    for (int i = 0, k = 0; i < n; i++) {
      for (int j = 0; j < n; j++)
        grid[i][j] = s[k++];
    }

    for (int j = 0; j < n; j++) {
      for (int i = 0; i < n; i++)
        cout << grid[i][n-1-j];
    }
    cout << "\n";
  }

  return 0;
}
```
