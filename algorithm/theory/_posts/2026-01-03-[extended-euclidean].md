---
layout: single
title: "확장 유클리드 알고리듬(Extended Euclidean Algorithm)의 원리와 구현 - soo:bak"
date: "2026-01-03 16:00:00 +0900"
description: GCD를 구하면서 베주 항등식의 계수를 함께 찾는 확장 유클리드 알고리듬의 원리와 활용을 다룹니다
tags:
  - 수학
  - 정수론
  - 확장유클리드
---

## 확장 유클리드 알고리듬이란?

유클리드 호제법으로 두 수의 최대공약수를 구할 수 있다는 것은 잘 알려져 있습니다.

**확장 유클리드 알고리듬(Extended Euclidean Algorithm)**은 여기서 한 걸음 더 나아가,

최대공약수를 구하면서 동시에 다음을 만족하는 정수 $$x$$, $$y$$를 찾습니다:

$$
ax + by = \gcd(a, b)
$$

<br>

이 식을 **베주 항등식(Bézout's Identity)**이라고 합니다.

예를 들어, $$a = 30$$, $$b = 21$$일 때 $$\gcd(30, 21) = 3$$이고,

$$30 \times (-2) + 21 \times 3 = 3$$이므로 $$x = -2$$, $$y = 3$$입니다.

> 참고 : [유클리드 호제법(Euclidean Algorithm)과 최대공약수 - soo:bak](https://soo-bak.github.io/algorithm/theory/gcd-euclidean-explained/)

---

## 알고리듬의 원리

유클리드 호제법의 핵심 성질을 다시 떠올려 보겠습니다:

$$
\gcd(a, b) = \gcd(b, a \bmod b)
$$

이 과정을 $$b = 0$$이 될 때까지 반복하면 최대공약수를 얻습니다.

<br>

확장 유클리드 알고리듬은 이 과정을 **역추적**하여 베주 계수를 구합니다.

<br>

### 기저 조건

$$b = 0$$일 때:

$$
a \times 1 + 0 \times 0 = a = \gcd(a, 0)
$$

따라서 $$x = 1$$, $$y = 0$$입니다.

<br>

### 재귀 단계

$$\gcd(b, a \bmod b) = bx_1 + (a \bmod b)y_1$$을 이미 알고 있다고 가정합니다.

$$a \bmod b = a - \lfloor a/b \rfloor \times b$$이므로:

$$
\begin{align}
\gcd(a, b) &= bx_1 + (a - \lfloor a/b \rfloor b)y_1 \\
&= ay_1 + b(x_1 - \lfloor a/b \rfloor y_1)
\end{align}
$$

따라서:
- $$x = y_1$$
- $$y = x_1 - \lfloor a/b \rfloor y_1$$

---

## 단계별 예시

$$\gcd(35, 15)$$의 베주 계수를 찾는 과정입니다.

<br>

**유클리드 호제법 진행:**

1. $$\gcd(35, 15)$$
   - $$35 = 15 \times 2 + 5$$
   - $$\gcd(35, 15) = \gcd(15, 5)$$

2. $$\gcd(15, 5)$$
   - $$15 = 5 \times 3 + 0$$
   - $$\gcd(15, 5) = \gcd(5, 0) = 5$$

<br>

**역추적:**

1. 기저: $$\gcd(5, 0) = 5$$
   - $$x = 1$$, $$y = 0$$
   - $$5 \times 1 + 0 \times 0 = 5$$ (확인)

2. $$\gcd(15, 5)$$로 역추적
   - $$x = 0$$, $$y = 1 - 3 \times 0 = 1$$
   - $$15 \times 0 + 5 \times 1 = 5$$ (확인)

3. $$\gcd(35, 15)$$로 역추적
   - $$x = 1$$, $$y = 0 - 2 \times 1 = -2$$
   - $$35 \times 1 + 15 \times (-2) = 5$$ (확인)

<br>

따라서 $$35 \times 1 + 15 \times (-2) = 5$$입니다.

---

## 구현

### 재귀 구현

수학적 정의를 그대로 코드로 옮긴 형태입니다.

```cpp
#include <bits/stdc++.h>
using namespace std;

long long extGcd(long long a, long long b, long long& x, long long& y) {
  // 기저 조건: b가 0이면 x=1, y=0
  if (b == 0) {
    x = 1;
    y = 0;
    return a;
  }

  long long x1, y1;
  long long g = extGcd(b, a % b, x1, y1);

  // 역추적하여 계수 계산
  x = y1;
  y = x1 - (a / b) * y1;

  return g;
}

int main() {
  long long a = 30, b = 21;
  long long x, y;

  long long g = extGcd(a, b, x, y);

  cout << "gcd(" << a << ", " << b << ") = " << g << "\n";
  cout << a << " * " << x << " + " << b << " * " << y << " = " << g << "\n";

  return 0;
}
```

**출력**:
```
gcd(30, 21) = 3
30 * -2 + 21 * 3 = 3
```

<br>

### 반복 구현

재귀 호출 대신 반복문을 사용한 형태입니다.

```cpp
#include <bits/stdc++.h>
using namespace std;

long long extGcd(long long a, long long b, long long& x, long long& y) {
  x = 1; y = 0;
  long long x1 = 0, y1 = 1;

  while (b != 0) {
    long long q = a / b;

    tie(x, x1) = make_tuple(x1, x - q * x1);
    tie(y, y1) = make_tuple(y1, y - q * y1);
    tie(a, b) = make_tuple(b, a - q * b);
  }

  return a;
}

int main() {
  long long a = 30, b = 21;
  long long x, y;

  long long g = extGcd(a, b, x, y);

  cout << "gcd(" << a << ", " << b << ") = " << g << "\n";
  cout << a << " * " << x << " + " << b << " * " << y << " = " << g << "\n";

  return 0;
}
```

**장점**:
- 함수 호출 오버헤드가 없어 미세하게 더 빠름
- 스택 오버플로우 걱정 없음

**단점**:
- 재귀 버전에 비해 코드가 약간 더 김

<br>

실전에서는 두 방법 모두 충분히 빠르므로, 선호하는 스타일에 따라 선택하면 됩니다.

---

## 시간 복잡도

확장 유클리드 알고리듬의 시간 복잡도는 기본 유클리드 호제법과 동일합니다:

$$
O(\log \min(a, b))
$$

<br>

### 공간 복잡도

- 재귀 구현: $$O(\log \min(a, b))$$ (재귀 스택)
- 반복 구현: $$O(1)$$

---

## 확장 유클리드 알고리듬의 활용

### 1) 모듈러 역원 계산

$$a$$의 모듈러 $$m$$에 대한 역원, 즉 $$ax \equiv 1 \pmod{m}$$을 만족하는 $$x$$를 구하는 문제는

$$ax + my = 1$$을 만족하는 $$x$$를 찾는 문제와 같습니다.

단, $$\gcd(a, m) = 1$$이어야 역원이 존재합니다.

```cpp
long long modInverse(long long a, long long m) {
  long long x, y;
  long long g = extGcd(a, m, x, y);

  if (g != 1) {
    return -1;  // 역원 없음 (a와 m이 서로소가 아님)
  }

  return (x % m + m) % m;  // 양수로 변환
}
```

<br>

### 2) 선형 디오판틴 방정식

$$ax + by = c$$의 정수해를 구하는 문제입니다.

해가 존재하려면 $$\gcd(a, b)$$가 $$c$$를 나누어야 합니다.

```cpp
bool solveDiophantine(long long a, long long b, long long c,
                      long long& x, long long& y) {
  long long g = extGcd(a, b, x, y);

  if (c % g != 0) {
    return false;  // 해 없음
  }

  // 특수해
  x *= c / g;
  y *= c / g;

  return true;
}
```

특수해 $$(x_0, y_0)$$를 찾으면, 일반해는 다음과 같습니다:

$$
x = x_0 + \frac{b}{\gcd(a,b)} t, \quad y = y_0 - \frac{a}{\gcd(a,b)} t \quad (t \in \mathbb{Z})
$$

<br>

### 3) 중국인의 나머지 정리 (CRT)

연립 합동식을 푸는 데에도 확장 유클리드 알고리듬이 사용됩니다.

$$
\begin{cases}
x \equiv a_1 \pmod{m_1} \\
x \equiv a_2 \pmod{m_2}
\end{cases}
$$

```cpp
pair<long long, long long> crt(long long a1, long long m1,
                                long long a2, long long m2) {
  long long p, q;
  long long g = extGcd(m1, m2, p, q);

  if ((a2 - a1) % g != 0) {
    return {-1, -1};  // 해 없음
  }

  long long lcm = m1 / g * m2;
  long long ans = a1 + m1 * ((a2 - a1) / g * p % (m2 / g));
  ans = ((ans % lcm) + lcm) % lcm;

  return {ans, lcm};
}
```

---

## 주의사항

베주 계수는 유일하지 않습니다.

$$35 \times 1 + 15 \times (-2) = 5$$

$$35 \times (-2) + 15 \times 5 = 5$$

둘 다 올바른 해입니다. 확장 유클리드 알고리듬은 그 중 하나를 구해줍니다.

<br>

또한, 중간 계산에서 곱셈이 발생하므로 오버플로우에 주의해야 합니다.

입력 값이 큰 경우 `long long`을 사용하는 것이 안전합니다.

---

## 마무리

확장 유클리드 알고리듬은 최대공약수와 함께 베주 계수를 찾는 알고리듬입니다.

<br>

모듈러 역원 계산, 선형 디오판틴 방정식 해결, 중국인의 나머지 정리 등

정수론과 관련된 다양한 문제에서 활용됩니다.

<br>

알고리듬 문제에서 모듈러 연산이나 정수 방정식이 등장한다면,

확장 유클리드 알고리듬의 활용을 떠올려 보면 도움이 됩니다.

<br>

**관련 글**:
- [유클리드 호제법(Euclidean Algorithm)과 최대공약수 - soo:bak](https://soo-bak.github.io/algorithm/theory/gcd-euclidean-explained/)
- [기약 분수(irreducible fraction)의 알고리듬적 접근 - soo:bak](https://soo-bak.github.io/algorithm/theory/irreducible-fraction/)

<br>

**관련 문제**:
- [[백준 3955] 캔디 분배](https://www.acmicpc.net/problem/3955)
- [[백준 14565] 역원(Inverse) 구하기](https://www.acmicpc.net/problem/14565)
