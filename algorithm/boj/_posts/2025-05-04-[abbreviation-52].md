---
layout: single
title: "[백준 3181] 줄임말 만들기 (C#, C++) - soo:bak"
date: "2025-05-04 17:31:00 +0900"
description: 의미 없는 단어를 제외하고 각 단어의 앞글자만 따서 줄임말을 만드는 백준 3181번 줄임말 만들기 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[3181번 - 줄임말 만들기](https://www.acmicpc.net/problem/3181)

## 설명
주어진 문장에서 각 단어의 첫 글자를 따서 **줄임말**을 만드는 문제입니다.

다만, 일부 단어들은 의미 없는 단어로 간주되어 줄임말에서 제외해야 하며,

**첫 번째 단어**는 의미 없는 단어더라도 반드시 포함해야 합니다.

<br>

다음의 단어들은 무시해야 할 의미 없는 단어입니다:

```
i, pa, te, ni, niti, a, ali, nego, no, ili
```

이 단어들이 문장의 **두 번째 이후**에 등장하면 무시하고,

그 외 단어는 첫 글자를 따서 모두 대문자로 만들어 연결합니다.

<br>

## 접근법
- 먼저 문장을 문자열로 입력받고, 공백 기준으로 나누어 단어 리스트를 만듭니다.
- 각 단어를 순서대로 확인하면서:
  - 첫 번째 단어는 무조건 줄임말에 포함시키고,
  - 나머지 단어는 무시 목록에 포함되지 않은 경우에만 줄임말에 포함시킵니다.
- 줄임말은 각 단어의 첫 글자를 대문자로 변환해 이어 연결합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var useless = new[] { "i", "pa", "te", "ni", "niti",
                          "a", "ali", "nego", "no", "ili" };
    var input = Console.ReadLine().Split(' ');

    var result = "";
    for (int i = 0; i < input.Length; i++) {
      if (i == 0 || !useless.Contains(input[i]))
        result += char.ToUpper(input[i][0]);
    }

    Console.WriteLine(result);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

bool isUseless(const string& s) {
  static const string useless[] = {"i", "pa", "te", "ni", "niti",
                                   "a", "ali", "nego", "no", "ili"};
  for (const string& u : useless)
    if (s == u) return true;
  return false;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string s; getline(cin, s);
  string ans;

  int cnt = 0;
  size_t i = 0;
  while (i < s.size()) {
    size_t j = s.find(' ', i);
    if (j == string::npos) j = s.size();
    string w = s.substr(i, j - i);
    if (++cnt == 1 || !isUseless(w)) ans += toupper(w[0]);
    i = j + 1;
  }
  cout << ans << "\n";

  return 0;
}
```
