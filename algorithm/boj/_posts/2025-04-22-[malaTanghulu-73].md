---
layout: single
title: "[백준 31923] 마라탕후루 (C#, C++) - soo:bak"
date: "2025-04-22 00:42:00 +0900"
description: 두 수열의 항별 차이와 변화 조건을 바탕으로 목표 상태로 도달 가능한지 판단하는 백준 31923번 마라탕후루 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[31923번 - 마라탕후루](https://www.acmicpc.net/problem/31923)

## 설명
탕후루에 꽂힌 다양한 과일들(딸기, 샤인머스캣 등)을 통해 문제를 비유적으로 설명하고 있지만,<br>
<br>
결국, **현재 상태를 나타내는 수열과 목표 상태 수열이 주어졌을 때**,  <br>
<br>
각 항에 대해 `특정한 조건의 연산`을 반복하여 `목표 상태로 도달할 수 있는지`를 판별하는 문제입니다.  <br>
<br>
각 과일 조각은 `현재 상태`를 의미하고, 원하는 탕후루의 완성 모습은 `목표 상태`입니다.<br>
<br>

- 수열의 길이 `n`과 함께 두 정수 `p`, `q`가 주어집니다.
- 이후 `n`개의 정수로 이루어진 두 수열 `a`(현재 상태)와 `b`(목표 상태)가 입력됩니다.
- 각 항에 대해 정수 $$c_i$$를 설정했을 때, 다음과 같은 조건이 성립해야 합니다:
    $$ a_i + c_i \cdot p = b_i + c_i \cdot q $$

<br>
여기서 $$c_i$$는 각 항에서 수열 $$a$$의 값($$a_i$$)들을 $$b$$로 바꾸기 위해<br>
<br>
필요한 '조작의 횟수' 또는 '곱해야할 값', '나누어야할 값' 등입니다.<br>
<br>
(이 문제에서는 '더해야할 값'을 나타냅니다.)<br>
<br>
<br>
즉, $$c_i$$는 $$a_i$$와 $$b_i$$를 위의 식을 통해 연결하는 정수로,<br>
<br>
문제의 상황이나 조건 등에 따라서 **설정**해야 하는 값입니다.<br>


<br>
<br>
다시 다음의 수식을 살펴 보면 :<br>

$$
a_i + c_i \cdot p = b_i + c_i \cdot q
$$

이 식을 정리하면 다음과 같은 관계가 됩니다:

$$
a_i - b_i = c_i \cdot (q - p)
$$

따라서 $$c_i$$는 다음과 같이 계산할 수 있습니다:

$$
c_i = \frac{a_i - b_i}{q - p}
$$

<br>

여기서 주의해야 할 조건은 다음과 같습니다:

- `p`와 `q`가 같은 경우에는 $$c_i$$가 사라지므로 단순히 $$a_i = b_i$$ 여야만 합니다.
- `p`와 `q`가 같지 않은 경우에는 다음 두 가지 조건을 만족해야 합니다:
  - $$a_i - b_i$$가 $$q - p$$로 정확히 나누어떨어져야 합니다.
  - 그리고 계산된 $$c_i$$의 부호가 **변화의 방향과 일치해야** 합니다.


<br>
### 변화 방향이란 무엇인가?

- $$a_i - b_i$$는 현재 상태와 목표 상태의 차이,<br>
  즉, 현재 상태에서 목표상태로 **변화에 대한 방향성**을 가지고 있습니다.
  - 예: 현재 10, 목표 6이면 → 값을 줄이는 방향

- $$q - p$$는 연산(막대 꽂기)에 의해 **한 번에 얼마만큼 변화하는지를 나타내는 값**으로,<br>
  이 역시 **변화에 대한 방향성**을 가지고 있습니다.

<br>
이 두 값의 곱이 `음수` 또는 `0`이어야만, 현재 상태에서 목표 상태로 도달이 가능합니다. <br>
<br>

 **곱이 양수인 경우**: $$(a_i - b_i) \cdot (q - p) > 0$$
  - $$a_i - b_i$$와 $$q - p$$가 **같은 부호**일 때, <br>
    변화 방향과 연산 방향이 **반대**:
    - 예: 값을 줄여야 하는데 $$a_i - b_i > 0$$, <br>
      연산은 값을 증가시킴 $$(q - p > 0)$$.<br>
      연산이 목표와 반대 방향으로 작용해 도달 불가능. <br>


<br>
즉, 다음 조건이 핵심입니다:<br>

$$
(a_i - b_i) \cdot (q - p) \leq 0
$$


<br>
조건을 하나라도 만족하지 못하면 `"NO"`를 출력하고 종료합니다.<br>
<br>
모든 항이 조건을 만족하면 `"YES"`와 함께 각 항에 해당하는 $$c_i$$ 값을 출력합니다.<br>
<br>


---

## 접근법

1. 먼저 `n`, `p`, `q`를 입력받고, 두 수열 `a`, `b`를 읽습니다.
2. 각 항목에 대해 다음을 판별합니다:
   - `p = q`인 경우: $$a_i = b_i$$인지 확인.
   - `p \ne q`인 경우:
     - $$a_i - b_i$$가 $$q - p$$로 나누어떨어지는지 확인
     - $$c_i = \frac{a_i - b_i}{q - p}$$ 계산 후, 해당 값이 문제 조건에 맞는지 확인
3. 조건에 맞지 않으면 "NO"를 출력하고 종료.
   모두 통과하면 각 $$c_i$$를 출력.

시간 복잡도는 수열을 한 번씩 확인하므로 `O(n)`입니다.

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split().Select(long.Parse).ToArray();
    int n = (int)input[0];
    long p = input[1], q = input[2];

    var a = Console.ReadLine().Split().Select(long.Parse).ToArray();
    var b = Console.ReadLine().Split().Select(long.Parse).ToArray();

    var result = new long[n];

    for (int i = 0; i < n; i++) {
      long lhs = a[i], rhs = b[i];
      long diff = lhs - rhs;

      if (p == q) {
        if (lhs != rhs) {
          Console.WriteLine("NO");
          return;
        }
        result[i] = 0;
      } else {
        long d = p - q;
        if (diff % d != 0 || diff * d > 0) {
          Console.WriteLine("NO");
          return;
        }
        result[i] = -(diff / d);
      }
    }

    Console.WriteLine("YES");
    Console.WriteLine(string.Join(" ", result));
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
#define MAX 100

using namespace std;
typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll a[MAX + 1], b[MAX + 1];

  ll n, p, q; cin >> n >> p >> q;
  for (int i = 1; i <= n; i++)
    cin >> a[i];
  for (int i = 1; i <= n; i++)
    cin >> b[i];

  for (int i = 1; i <= n; i++) {
    ll diff = a[i] - b[i];
    if (p == q) {
      if (diff != 0) {
        cout << "NO\n";
        return 0;
      }
    } else if (diff % (p - q) != 0 || diff * (p - q) > 0) {
      cout << "NO\n";
      return 0;
    }
  }

  cout << "YES\n";
  for (int i = 1; i <= n; i++)
    cout << (p == q ? 0 : -(a[i] - b[i]) / (p - q)) << ' ';
  cout << "\n";

  return 0;
}
```
