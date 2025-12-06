---
layout: single
title: "[백준 12400] Speaking in Tongues (Small) (C#, C++) - soo:bak"
date: "2025-12-06 22:55:00 +0900"
description: 고정된 Googlerese 치환 표를 이용해 소문자 알파벳을 복호화하는 백준 12400번 Speaking in Tongues (Small) 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[12400번 - Speaking in Tongues (Small)](https://www.acmicpc.net/problem/12400)

## 설명
Googlerese로 변환된 문자열이 주어집니다. 고정된 일대일 대응 치환표를 사용해 영어 소문자로 복원합니다.

공백은 그대로 두고, 각 테스트케이스는 지정된 형식으로 출력합니다.

<br>

## 접근법
먼저, 치환 문자열을 준비합니다. 입력 문자의 인덱스를 구해 대응하는 문자를 얻습니다.

다음으로, 알파벳이 아닌 공백은 그대로 둡니다. 테스트케이스 순서대로 결과를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var map = "yhesocvxduiglbkrztnwjpfmaq";
      var T = int.Parse(Console.ReadLine()!);
      for (var tc = 1; tc <= T; tc++) {
        var line = Console.ReadLine()!;
        var arr = line.ToCharArray();
        for (var i = 0; i < arr.Length; i++) {
          if (char.IsLetter(arr[i]))
            arr[i] = map[arr[i] - 'a'];
        }
        Console.WriteLine($"Case #{tc}: {new string(arr)}");
      }
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

  string mp = "yhesocvxduiglbkrztnwjpfmaq";
  int T; cin >> T;
  cin.ignore();
  for (int tc = 1; tc <= T; tc++) {
    string s; getline(cin, s);
    for (char& ch : s) {
      if (isalpha(ch))
        ch = mp[ch - 'a'];
    }
    cout << "Case #" << tc << ": " << s << "\n";
  }

  return 0;
}
```
