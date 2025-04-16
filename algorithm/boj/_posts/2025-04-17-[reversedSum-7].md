---
layout: single
title: "[백준 1357] 뒤집힌 덧셈 (C#, C++) - soo:bak"
date: "2025-04-17 01:06:35 +0900"
description: 숫자를 뒤집어서 더한 후 다시 뒤집는 연산을 수행하는 백준 1357번 뒤집힌 덧셈 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[1357번 - 뒤집힌 덧셈](https://www.acmicpc.net/problem/1357)

## 설명
**두 수를 뒤집어서 더한 후, 그 결과도 다시 뒤집어 출력하는 문자열 기반의 연산 문제**입니다.<br>
<br>

- 입력으로 두 수가 주어지며, 각 수는 문자열 형태로 처리해 뒤집습니다.<br>
- 뒤집힌 두 수를 정수로 변환해 더한 뒤, 그 합도 다시 문자열로 바꾸어 뒤집고 출력합니다.<br>
- 중간에 0이 앞에 오는 경우도 있으므로, 숫자와 문자열 변환을 적절히 활용해야 합니다.<br>

### 접근법
- 정수를 문자열로 변환한 후 `reverse()` 함수를 이용하여 뒤집는 보조 함수를 작성합니다.<br>
- 입력받은 두 수를 각각 뒤집어 더한 후, 그 결과를 다시 뒤집어 출력합니다.<br>
- 문자열과 정수 간 변환을 유연하게 활용하는 것이 핵심입니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static int Rev(int num) {
    char[] chars = num.ToString().ToCharArray();
    Array.Reverse(chars);
    return int.Parse(new string(chars));
  }

  static void Main() {
    var input = Console.ReadLine().Split();
    int x = int.Parse(input[0]);
    int y = int.Parse(input[1]);

    int result = Rev(Rev(x) + Rev(y));
    Console.WriteLine(result);
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

int rev(int num) {
  string str = to_string(num);
  reverse(str.begin(), str.end());
  return stoi(str);
}

int main() {
  int x, y; cin >> x >> y;

  int result = rev(rev(x) + rev(y));
  cout << result << "\n";

  return 0;
}
```
