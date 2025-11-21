---
layout: single
title: "[백준 5598] 카이사르 암호 (C#, C++) - soo:bak"
date: "2025-04-19 20:08:01 +0900"
description: 알파벳을 세 글자 뒤로 이동하는 방식의 카이사르 암호를 복호화하는 백준 5598번 카이사르 암호 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[5598번 - 카이사르 암호](https://www.acmicpc.net/problem/5598)

## 설명
**카이사르 암호 방식을 사용하여 암호화된 문자열을 복호화하는 문제**입니다.<br>
<br>

- 입력은 모두 대문자로 이루어진 알파벳 문자열입니다.<br>
- 카이사르 암호 방식은 원래의 알파벳에서 **세 칸 뒤의 문자**를 암호문으로 사용했다고 설명되어 있습니다.<br>
- 예를 들어, `'D'` → `'A'`, `'E'` → `'B'`와 같은 방식입니다.<br>
- 알파벳은 순환되며, `'A'`에서 `1`만큼 앞으로 이동하면 `'Z'`가 됩니다.<br>

### 접근법
- 입력된 문자열을 한 글자씩 순회합니다.<br>
- 각 문자를 `-3` 이동시키되, `'A'`보다 작아지면 알파벳 순환을 고려해 `+26`을 더해줍니다.<br>
- 최종 복호화된 문자열을 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    string input = Console.ReadLine();
    char[] decrypted = new char[input.Length];

    for (int i = 0; i < input.Length; i++) {
      decrypted[i] = (char)(input[i] - 3);
      if (decrypted[i] < 'A')
        decrypted[i] = (char)(decrypted[i] + 26);
    }

    Console.WriteLine(new string(decrypted));
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

  string str; cin >> str;
  for (size_t i = 0; i < str.size(); i++) {
    str[i] -= 3;
    if (str[i] < 'A') str[i] += 26;
  }

  cout << str << "\n";

  return 0;
}
```
