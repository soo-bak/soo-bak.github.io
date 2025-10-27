---
layout: single
title: "[백준 1541] 잃어버린 괄호 (C#, C++) - soo:bak"
date: "2025-10-26 00:10:00 +0900"
description: 첫 번째 마이너스 이후 모든 수를 묶어 빼서 식의 값을 최소로 만드는 백준 1541번 잃어버린 괄호 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[1541번 - 잃어버린 괄호](https://www.acmicpc.net/problem/1541)

## 설명

`+`, `-`만 등장하는 수식에서 괄호를 모두 지운 상태가 주어집니다.<br>

여기에 다시 괄호를 배치해 **식의 값을 가능한 한 작게** 만들어야 합니다.<br>

식의 길이는 `50` 이하이고, 숫자는 최대 `5`자리까지 이어질 수 있으며 `0`으로 시작하더라도 그대로 계산하면 됩니다.<br>

<br>

## 접근법

최솟값을 만들기 위해서는 **첫 번째 `-` 이후의 모든 수를 한꺼번에 빼는 전략**이 최적입니다.<br>

이를 위해 `-`를 기준으로 식을 나누고, 첫 구간은 모두 더한 뒤 이후 구간은 각각의 합을 계산해 차례로 빼줍니다.

- 식을 `-`로 분할한 뒤, 첫 구간은 `+`로 나누어 모두 더합니다.
- 이후 구간 역시 `+`로 분해해 합을 구한 뒤, 누적 합에서 순서대로 뺍니다.
- 이렇게 하면 첫 `-` 이후 구간이 전부 괄호로 묶인 효과가 나서 최솟값을 보장합니다.

<br>
각 구간의 누적 합만 다루므로, **파싱 과정에서의 자릿수 처리와 빼기 순서**만 주의하면 됩니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var expression = Console.ReadLine()!;
    var blocks = expression.Split('-');

    var ans = blocks[0].Split('+').Select(int.Parse).Sum();
    foreach (var block in blocks.Skip(1)) {
      var value = block.Split('+').Select(int.Parse).Sum();
      ans -= value;
    }

    Console.WriteLine(ans);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<string> vs;

int sumBlock(const string& block) {
  int sum = 0; string number;
  for (char ch : block) {
    if (ch == '+') {
      sum += stoi(number);
      number.clear();
    } else
      number.push_back(ch);
  }
  if (!number.empty())
    sum += stoi(number);

  return sum;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string expr; cin >> expr;

  vs blocks;
  string current;
  for (char ch : expr) {
    if (ch == '-') {
      blocks.push_back(current);
      current.clear();
    } else
      current.push_back(ch);
  }
  blocks.push_back(current);

  int ans = sumBlock(blocks.front());
  for (size_t i = 1; i < blocks.size(); ++i)
    ans -= sumBlock(blocks[i]);

  cout << ans << "\n";
  
  return 0;
}
```
