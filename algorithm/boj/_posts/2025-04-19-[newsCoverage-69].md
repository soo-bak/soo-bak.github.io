---
layout: single
title: "[백준 2845] 파티가 끝나고 난 뒤 (C#, C++) - soo:bak"
date: "2025-04-19 21:48:00 +0900"
description: 면적당 사람 수를 기준으로 실제 인원 수를 계산하고, 기사 수치와의 차이를 구하는 백준 2845번 파티가 끝나고 난 뒤 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[2845번 - 파티가 끝나고 난 뒤](https://www.acmicpc.net/problem/2845)

## 설명
**단위 면적당 사람 수를 이용해 실제 인원 수를 계산하고, 보도된 기사 수치와의 차이를 구하는 구현 문제**입니다.<br>
<br>

- 한 평방미터당 사람 수와 전체 면적이 주어집니다.<br>
- 이후 `5`개의 숫자는 신문 기사에 보도된 예상 인원 수입니다.<br>
- 실제 인원 수는 `단위 인원 수 × 전체 면적`으로 계산할 수 있습니다.<br>
- 보도된 인원 수에서 실제 인원 수를 뺀 값을 차례대로 출력합니다.<br>

### 접근법
- 먼저, 두 값을 곱하여 **실제 총 인원 수**를 계산합니다:
  $$\text{총 인원 수} = p \times s$$<br>
- 이후, 기사에 적힌 각 수치에 대하여 위에서 구한 인원 수를 뺀 값을 구해 형식에 맞게 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    var p = int.Parse(input[0]);
    var s = int.Parse(input[1]);
    var total = p * s;

    var article = Console.ReadLine().Split();
    for (int i = 0; i < 5; i++) {
      var reported = int.Parse(article[i]);
      Console.Write(reported - total);
      if (i != 4) Console.Write(" ");
    }
    Console.WriteLine();
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

  int p, s; cin >> p >> s;
  for (int i = 0; i < 5; i++) {
    int num; cin >> num;
    cout << num - (p * s);
    if (i != 4) cout << " ";
  }
  cout << "\n";

  return 0;
}
```
