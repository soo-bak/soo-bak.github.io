---
layout: single
title: "[백준 1032] 명령 프롬프트 (C#, C++) - soo:bak"
date: "2025-04-19 20:31:32 +0900"
description: 여러 파일 이름에서 공통된 패턴을 추출하여 와일드카드로 표현하는 백준 1032번 명령 프롬프트 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[1032번 - 명령 프롬프트](https://www.acmicpc.net/problem/1032)

## 설명
**여러 개의 파일 이름이 주어졌을 때, 모든 파일에서 공통적으로 나타나는 패턴을 추출하는 문제**입니다.<br>
<br>

- 각 파일 이름은 같은 길이를 가지며, 총 `N`개의 파일이 입력으로 주어집니다.<br>
- 각 파일 이름의 **같은 위치**에 있는 문자가 모두 동일하면 그 문자를 출력합니다.<br>
- 하나라도 다른 문자가 있다면, 해당 위치에는 **물음표(**`?`**)**를 출력합니다.<br>
- 즉, 공통된 접두어나 접미사를 찾는 것이 아니라, **각 인덱스별 문자 일치 여부**를 따져서 문자열을 만들어야 합니다.<br>

## 접근법
- 첫 번째 파일 이름을 기준 문자열로 사용합니다.<br>
- 두 번째 파일부터 하나씩 비교하면서, 같은 위치에 있는 문자가 서로 다르면 해당 위치를 `?`로 바꿉니다.<br>
- 이 과정을 반복하면 모든 파일에 대해 공통적으로 일치하는 문자만 남고, 나머지는 `?`가 됩니다.<br>
- 마지막으로 완성된 문자열을 출력하면 됩니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    string[] files = new string[n];
    for (int i = 0; i < n; i++)
      files[i] = Console.ReadLine();

    char[] result = files[0].ToCharArray();

    for (int i = 1; i < n; i++) {
      for (int j = 0; j < result.Length; j++) {
        if (result[j] != files[i][j])
          result[j] = '?';
      }
    }

    Console.WriteLine(new string(result));
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<string> vs;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntF; cin >> cntF;

  vs files(cntF);
  for (int i = 0; i < cntF; i++)
    cin >> files[i];

  string ans = files[0];
  for (int i = 1; i < cntF; i++) {
    for (size_t j = 0; j < ans.size(); j++) {
      if (ans[j] != files[i][j]) ans[j] = '?';
    }
  }

  cout << ans << "\n";

  return 0;
}
```
