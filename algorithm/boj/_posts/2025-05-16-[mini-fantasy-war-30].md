---
layout: single
title: "[백준 12790] Mini Fantasy War (C#, C++) - soo:bak"
date: "2025-05-16 21:01:00 +0900"
description: 기본 능력치와 장비 보정을 합산하여 최종 전투력을 계산하는 백준 12790번 Mini Fantasy War 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[12790번 - Mini Fantasy War](https://www.acmicpc.net/problem/12790)

## 설명

**캐릭터의 기본 능력치와 장비 효과를 반영해 전투력을 계산하는 간단한 시뮬레이션 문제입니다.**

능력치는 총 `4가지`로 구성됩니다:

- `HP`
- `MP`
- `공격력`
- `방어력`

<br>
각 캐릭터는 기본 능력치에 장비로 인한 증감량이 더해져 **최종 능력치**를 갖습니다.

단, 아래와 같은 조건이 반드시 적용됩니다:

- `HP`, `MP`는 `1`보다 작을 수 없으며, `1`로 보정됩니다.
- `공격력`은 `0`보다 작을 수 없으며, `0`으로 보정됩니다.
- `방어력`은 음수여도 그대로 사용됩니다.

`전투력` 계산식은 다음과 같습니다:

$$
\text{전투력} = 1 \times HP + 5 \times MP + 2 \times 공격력 + 2 \times 방어력
$$

<br>

## 접근법

각 테스트 케이스마다 총 `8개`의 정수가 주어집니다:

- 기본 능력치 `4개`: `HP`, `MP`, `공격력`, `방어력`
- 장비 보정값 `4개`: `HP`, `MP`, `공격력`, `방어력`

이들을 각각 합산한 뒤, 조건에 맞게 보정하고 전투력을 계산합니다.

전체 흐름은 다음과 같습니다:

1. 입력된 `8개`의 수를 받아 각 능력치를 계산합니다.
2. `HP`, `MP`는 최소 `1`로, `공격력`은 최소 `0`으로 보정합니다.
3. 위에서 주어진 전투력 공식을 이용해 최종 값을 출력합니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var tokens = Console.ReadLine().Split();
      int hp = int.Parse(tokens[0]) + int.Parse(tokens[4]);
      int mp = int.Parse(tokens[1]) + int.Parse(tokens[5]);
      int atk = int.Parse(tokens[2]) + int.Parse(tokens[6]);
      int def = int.Parse(tokens[3]) + int.Parse(tokens[7]);

      hp = Math.Max(1, hp);
      mp = Math.Max(1, mp);
      atk = Math.Max(0, atk);

      int power = hp + 5 * mp + 2 * atk + 2 * def;
      Console.WriteLine(power);
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

  int t; cin >> t;
  while (t--) {
    int hp, mp, a, d; cin >> hp >> mp >> a >> d;
    int dh, dm, da, dd; cin >> dh >> dm >> da >> dd;
    hp = max(1, hp + dh);
    mp = max(1, mp + dm);
    a = max(0, a + da);
    cout << hp + 5 * mp + 2 * a + 2 * (d + dd) << "\n";
  }

  return 0;
}
```
